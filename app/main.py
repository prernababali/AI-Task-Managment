from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, tasks, documents, search, analytics
from app.models import models

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Task & Knowledge Management System")

# Include all routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "AI Task Management System is running!"}
