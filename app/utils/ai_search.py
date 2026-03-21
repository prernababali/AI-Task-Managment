from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

document_store = []
index = None

def build_index(documents: list):
    global index, document_store
    document_store = documents
    embeddings = model.encode([doc["content"] for doc in documents])
    embeddings = np.array(embeddings).astype("float32")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

def search_documents(query: str, top_k: int = 3):
    global index, document_store
    if index is None or len(document_store) == 0:
        return []
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i in indices[0]:
        if i < len(document_store):
            results.append(document_store[i])
    return results