from fastapi import APIRouter
from services.vector_database_service import consulta_db


query_db_router = APIRouter()

@query_db_router.get('/chromadb/{document_name}')
def query_document(document_name: str):
    return consulta_db(document_name)