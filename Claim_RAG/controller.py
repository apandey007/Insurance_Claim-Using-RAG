from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ClaimAI RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _uploaded_file_size(file: UploadFile) -> int | None:
    stream = file.file

    try:
        current_position = stream.tell()
        stream.seek(0, 2)
        size = stream.tell()
        stream.seek(current_position)
        return size
    except (AttributeError, OSError):
        return None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat")
def chat(
    message: Annotated[str, Form()],
    files: Annotated[list[UploadFile], File()] = [],
) -> dict[str, object]:
    uploaded_files = [
        {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": _uploaded_file_size(file),
        }
        for file in files
    ]

    return {
        "message": message,
        "files": uploaded_files,
        "answer": "RAG pipeline is connected. Add retrieval and generation logic here.",
    }
