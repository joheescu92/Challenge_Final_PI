from fastapi import APIRouter
from services.orquestador_llm_service import orquestador_llm
from models.input_query_model import Query

orq_router = APIRouter()

@orq_router.post('/query')
def orquestador_llm_endpoint(query: Query):
    return orquestador_llm(query)