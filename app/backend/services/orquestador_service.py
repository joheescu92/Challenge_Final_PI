from dotenv import load_dotenv
import cohere
import os
from fastapi import HTTPException
from models.input_message_model import Message
from services.vector_database_service import get_context, document_in_db, add_documents
from services.document_service import get_content_document, get_chunks_document


load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

co = cohere.ClientV2()


def orquestador_llm(queryJSON: Message):
    print(queryJSON)
    query = queryJSON.message
    print(query)
    print("#################################")

    query_embedding = get_embeddings_query(query)

    context = get_context(query_embedding)

    #reranking?

    system_prompt = """
    Tu tarea es responder las preguntas manera con las siguientes instrucciones:
    -debes responder de manera entusiasta
    -debes utilizar solamente el contexto como base de tu informacion unicamente
    """

    #prompt final con instrucciones, pregunta del usuario y contexto recuperado de nuestra db

    prompt = f"""
    ####
    Instrucciones:
    -Tienes que contestar en no mas de 3 oraciones
    -siempre debes contestar en español
    ###
    Contexto:
    {context}
    ###
    Pregunta:
    {query}
    """
    #usé command-r-plus-08-2024 último modelo proporcionado por cohere, considero que tiene una
    #calidad de respuesta mejor que el resto y por eso opté por este
    check_response = co.chat(
        model="command-r-plus-08-2024", 
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": prompt}],
        temperature=0 #esto es para lograr que para la misma pregunta siempre conteste lo más similar posible

    )

    response = Message(message=check_response.message.content[0].text)
    return response




def get_embeddings_documents(chunks):
    response = co.embed(
    texts=chunks,
    model="embed-multilingual-v3.0",
    input_type="search_document",
    embedding_types=["float"],
    )
    return response.embeddings.float_


    
def get_embeddings_query(chunks: str):

    list_chunk = [chunks]

    response = co.embed(
    texts=list_chunk,
    model="embed-multilingual-v3.0",
    input_type="search_query",
    embedding_types=["float"],
    )
    return response.embeddings.float_


def upload_document(document_name: str):

    if document_in_db(document_name):
        raise HTTPException(status_code=409, detail="El documento ya se encuentra cargado en la base")
    
    results = get_content_document(document_name)

    content_document = results['content']
    document = results['document']
    
    chunks = get_chunks_document(content_document,document)

    embeddings = get_embeddings_documents(chunks)

    return add_documents(chunks,embeddings,document)
 
    
    