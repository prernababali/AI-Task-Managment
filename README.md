🤖 AI-Powered Task & Knowledge Management System
Show Image
Show Image
Show Image
Show Image
Show Image

📌 Overview
A fully functional AI-Powered Task & Knowledge Management System built with FastAPI and MySQL. The system allows Admins to upload documents and assign tasks, while Users can search documents using AI-powered semantic search (FAISS + Sentence Transformers) and complete their assigned tasks.

🏗️ System Architecture
┌─────────────────────────────────────────┐
│           FastAPI Application            │
├──────────┬──────────┬────────┬──────────┤
│   Auth   │  Tasks   │  Docs  │  Search  │
├──────────┴──────────┴────────┴──────────┤
│              MySQL Database              │
│  users | roles | tasks | documents |    │
│              activity_logs              │
├─────────────────────────────────────────┤
│         FAISS Vector Database           │
│   Sentence Transformers Embeddings      │
└─────────────────────────────────────────┘

🚀 Tech Stack
ComponentTechnologyBackend FrameworkFastAPI (Python 3.14)DatabaseMySQL 8.0ORMSQLAlchemyAuthenticationJWT (JSON Web Tokens)Password HashingBcrypt (Passlib)AI SearchSentence Transformers + FAISSAI Modelall-MiniLM-L6-v2ServerUvicornAPI DocsSwagger UI (Auto-generated)

📁 Project Structure
ai_task_manager/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # MySQL connection setup
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py           # SQLAlchemy DB models
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic request/response schemas
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py             # Register & Login APIs
│   │   ├── tasks.py            # Task management APIs
│   │   ├── documents.py        # Document upload APIs
│   │   ├── search.py           # AI search API
│   │   └── analytics.py        # Analytics API
│   │
│   └── utils/
│       ├── __init__.py
│       ├── auth.py             # JWT & RBAC utilities
│       └── ai_search.py        # FAISS embedding logic
│
├── uploads/                    # Uploaded documents stored here
├── .env                        # Environment variables
└── README.md

🗄️ Database Schema
sqlroles          users           tasks
──────         ──────          ──────
id (PK)        id (PK)         id (PK)
name           username        title
               email           description
               password        status (pending/completed)
               role_id (FK)    assigned_to (FK → users)
               created_at      created_by (FK → users)
                               created_at

documents                activity_logs
──────────               ─────────────
id (PK)                  id (PK)
filename                 user_id (FK → users)
filepath                 action
uploaded_by (FK)         details
uploaded_at              created_at

🔐 RBAC - Role Based Access Control
API EndpointAdminUserPOST /auth/register✅✅POST /auth/login✅✅POST /tasks/✅❌GET /tasks/✅✅PATCH /tasks/{id}❌✅POST /documents/upload✅❌GET /documents/✅✅POST /search/✅✅GET /analytics/✅❌

🤖 AI Search — How it Works
1. Admin uploads .txt document
         ↓
2. Document text is extracted
         ↓
3. Text converted to embeddings using
   Sentence Transformers (all-MiniLM-L6-v2)
         ↓
4. Embeddings stored in FAISS vector index
         ↓
5. User sends search query
         ↓
6. Query converted to embedding
         ↓
7. FAISS finds most similar documents
         ↓
8. Relevant documents returned to user

⚙️ Setup & Installation
Prerequisites

Python 3.11+
MySQL 8.0
Git

Step 1 — Clone the Repository
bashgit clone https://github.com/yourusername/ai_task_manager.git
cd ai_task_manager
Step 2 — Install Dependencies
bashpip install fastapi uvicorn sqlalchemy pymysql python-jose passlib python-multipart sentence-transformers faiss-cpu python-dotenv
Step 3 — Setup MySQL Database
sqlmysql -u root -p
CREATE DATABASE ai_task_manager;
USE ai_task_manager;
INSERT INTO roles (name) VALUES ('admin');
INSERT INTO roles (name) VALUES ('user');
exit
Step 4 — Configure Database
Open app/database.py and update:
pythonDATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/ai_task_manager"
Step 5 — Run the Server
bashpython -m uvicorn app.main:app --reload
Step 6 — Access API Docs
Open browser and go to:
http://127.0.0.1:8000/docs

📡 API Endpoints
Authentication
POST /auth/register   → Register new user
POST /auth/login      → Login and get JWT token
Tasks
POST   /tasks/              → Create task (Admin only)
GET    /tasks/              → Get all tasks (with filters)
PATCH  /tasks/{task_id}     → Update task status (User only)

Filtering:
GET /tasks?status=pending
GET /tasks?status=completed
GET /tasks?assigned_to=2
Documents
POST /documents/upload   → Upload .txt file (Admin only)
GET  /documents/         → Get all documents
Search (AI-Powered)
POST /search/   → Semantic search using FAISS embeddings
Analytics
GET /analytics/   → Get system stats (Admin only)

📊 Analytics Response Example
json{
  "total_tasks": 3,
  "completed_tasks": 2,
  "pending_tasks": 1,
  "total_documents": 2,
  "total_searches": 5
}

📝 Activity Logging
Every key action is automatically logged:
ActionWhenloginUser/Admin logs indocument_uploadAdmin uploads a documenttask_createdAdmin creates a tasktask_updatedUser updates task statussearchAny user searches documents

🧪 Testing Flow
Admin Flow:

Register as Admin (role_id: 1)
Login → get JWT token
Authorize in Swagger UI
Upload documents
Create and assign tasks
View analytics

User Flow:

Register as User (role_id: 2)
Login → get JWT token
Authorize in Swagger UI
View assigned tasks
Search documents using AI
Update task status to completed


👩‍💻 Author
Prerana

Assignment: AI-Powered Task & Knowledge Management System
Duration: 2-3 Days
Stack: Python, FastAPI, MySQL, FAISS, JWT