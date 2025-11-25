from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from pipeline.processor import process_document, get_process_status
from models.document import Document

app = FastAPI(
    title="YOUVISA Sprint 2 - Backend",
    description="API básica para receber arquivos e expor status do processo.",
    version="0.1.0",
)

# CORS liberado para facilitar testes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload", response_model=Document)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """
    Endpoint para upload de documentos.
    Encaminha o arquivo para o pipeline de automação.
    """
    return await process_document(file, background_tasks)


@app.get("/status")
def status():
    """
    Endpoint para consulta de status global e lista de documentos.
    """
    return get_process_status()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
