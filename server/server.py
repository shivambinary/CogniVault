from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from cognivault.ai.retrieval.retriever import SemanticRetriever


# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INDEX_PATH = BASE_DIR / "storage" / "vector_store" / "index.faiss"

METADATA_PATH = (
    BASE_DIR
    / "storage"
    / "vector_store"
    / "chunks_metadata.json"
)


# API
# --------------------------------------------------

app = FastAPI(
    title="CogniVault API",
    description="Semantic search API for the CogniVault knowledge base.",
    version="0.1.0",
)


# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://cognivault1.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request / Response Models
# --------------------------------------------------

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)


class SearchResult(BaseModel):
    chunk_id: str | None = None
    source: str | None = None
    chunk_index: int | None = None
    text: str
    similarity_score: float


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResult]


# Retriever
# --------------------------------------------------

retriever: SemanticRetriever | None = None


def get_retriever() -> SemanticRetriever:
    global retriever

    if retriever is None:
        retriever = SemanticRetriever(
            index_path=INDEX_PATH,
            metadata_path=METADATA_PATH,
        )

    return retriever


# Endpoints
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "CogniVault API is running",
        "status": "healthy",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CogniVault",
    }


@app.post("/api/search", response_model=SearchResponse)
def search_knowledge_base(request: SearchRequest):

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty.",
        )

    try:
        knowledge_retriever = get_retriever()

        results = knowledge_retriever.search(
            query=request.query.strip(),
            top_k=request.top_k,
        )

        return SearchResponse(
            query=request.query,
            total_results=len(results),
            results=results,
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Knowledge base files are missing: {error}",
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {error}",
        ) from error