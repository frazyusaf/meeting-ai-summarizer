from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from api.routes import upload, transcribe, summarize, export, auth
from database.connection import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    os.makedirs("uploads", exist_ok=True)
    yield


app = FastAPI(
    title="AI Meeting Notes Summarizer",
    description="Upload meeting recordings and get structured AI-generated notes instantly.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(transcribe.router, prefix="/api", tags=["Transcription"])
app.include_router(summarize.router, prefix="/api", tags=["Summarization"])
app.include_router(export.router, prefix="/api", tags=["Export"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "AI Meeting Notes Summarizer API"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
