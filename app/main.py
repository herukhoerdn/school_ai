from fastapi import FastAPI
from app.config.database import engine, Base, check_connection
from app.models import user, chat, jurusan
from app.routes.chat_routes import router as chat_router
from app.routes.auth_routes import router as auth_router  
from app.routes.assessment_routes import router as assessment_router
from app.routes.tryout_routes import router as tryout_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI School Future",
    description="API rekomendasi jurusan berbasis AI untuk siswa SMA/SMK",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

@app.on_event("startup")
def startup_event():
    print("[SERVER] AI School Future API starting...")
    check_connection()

@app.get("/")
def root():
    return {
        "app": "AI School Future",
        "status": "running",
        "docs": "/docs"
    }

app.include_router(assessment_router, prefix="/api")
app.include_router(tryout_router, prefix="/api")