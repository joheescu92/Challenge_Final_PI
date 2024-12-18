from fastapi import APIRouter
from services.orquestador_service import orquestador_llm
from models.input_message_model import Message

orq_router = APIRouter()

@orq_router.post('/query')
def orquestador_llm_endpoint(query: Message):
    return orquestador_llm(query)