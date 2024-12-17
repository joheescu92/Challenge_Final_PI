from fastapi import APIRouter
from services.vector_database_service import document_in_db

doc_router = APIRouter()

@doc_router.post('/chromadb/{document_name}')
async def upload_document_endpoint(document_name: str):
    return document_in_db(document_name)