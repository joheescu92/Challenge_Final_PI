from fastapi import APIRouter
from services.orquestador_service import upload_document

doc_router = APIRouter()

@doc_router.post('/chromadb/{document_name}')
async def upload_document_endpoint(document_name: str):
    return upload_document(document_name)