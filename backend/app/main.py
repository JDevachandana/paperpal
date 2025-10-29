from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest, ChatResponse, UploadResponse
from app.services.document_processor import DocumentProcessor
from app.services.rag import RAGPipeline


app = FastAPI(title="Paperpal RAG API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

doc_processor = DocumentProcessor()
rag_pipeline = RAGPipeline()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    try:
        stats = doc_processor.process_upload(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return UploadResponse(
        session_id=stats["session_id"],
        filename=stats.get("filename"),
        chunk_count=stats["chunk_count"],
        character_count=stats["character_count"],
    )


@app.post("/chat/{session_id}", response_model=ChatResponse)
async def chat_with_paper(session_id: str, payload: ChatRequest):
    try:
        result = rag_pipeline.chat(
            session_id=session_id,
            question=payload.question,
            mode=payload.mode.value,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ChatResponse(**result)
