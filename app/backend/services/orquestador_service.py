from dotenv import load_dotenv
import cohere
import os
from fastapi import HTTPException
from models.message_model import Message
from services.vector_database_service import get_context, document_in_db, add_documents
from services.document_service import get_content_document, get_chunks_document
from utils.orquestador_util import primera_instancia, rerank_responses, tercera_instancia_context, final_response

#Archivo que se encarga de la logica de negocios y tambien del orquestador

#Inicializo el cliente de Cohere cargando mi API_KEY del .env

############################################################

load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

co = cohere.ClientV2()

############################################################


def orquestador_llm(query: Message):
    
    query = query.message  # me  quedo con el mensaje en string


    #Primera instancia de validacion, el orquestador decide si la query debe pasar por RAG o no

    response_primera_instancia = primera_instancia(co,query)

    if response_primera_instancia != "rag":
        return Message(message=response_primera_instancia) #Retorno la respuesta como una instancia de Mensaje
    
    #Pasado la primera instancia, se sigue con el proc de embedding y retrieve a la base de datos
     
    # hace proceso de embedding de la query
    query_embedding = get_embeddings_query(query) 

    context = get_context(query_embedding) # hace retrive
    
    context_data = context["documents"] # contexto
   
    documents_list = [doc for sublist in context_data for doc in sublist] #me quedo con el contexto pero en lista
    
    #"Segunda instancia, reranking

    lista_indices_rerank = rerank_responses(co,query,documents_list) # esto me devuelve los indices de los documentos importantes

    lista_documentos_rerank = [documents_list[i] for i in lista_indices_rerank]

    documentos_re_rank = ''.join(lista_documentos_rerank) #contexto rerank en un solo string

    #Tercera instancia: validar si la query puede ser respondida por el contexto

    if tercera_instancia_context(co,query,documentos_re_rank) == "no":
        return Message(message="""Lo lamento, solo puedo responder preguntas que esten relacionadas
                        con los convenios colectivos de trabajo ¿tienes alguna otra pregunta en mente?""")
    
    #Ultima instancia: generar response final

    return final_response(co,query,documentos_re_rank)





def get_embeddings_documents(chunks):
    response = co.embed( # voy a guardar la respuesta de la función embd de Cohere
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

#Carga de documento
def upload_document(document_name: str):

    #Primera validacion

    if document_in_db(document_name):
        raise HTTPException(status_code=409, detail="No es posible cargar este documento porque ya se encuentra cargado en la base de datos")
    


    results = get_content_document(document_name) #obtengo contenido y instancia de la clase metadata_document_model

    content_document = results['content']
    document = results['document']
    
    chunks = get_chunks_document(content_document,document)

    embeddings = get_embeddings_documents(chunks)

    return add_documents(chunks,embeddings,document)# Agregar a la base de datos vectorial
 
    
    