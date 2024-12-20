from models.metadata_document_model import Metadata_Document
from fastapi import HTTPException


def add(chunks,embeddings,document: Metadata_Document,collection):
    #Primero vamos a hacer una validacion, si existen documentos cargados, vamos a tomar el ultimo id para que a
    #partir de ese numero vaya generando nuevos, si es la primera vez que se carga un documento, no va a haber problema
    #porque el resultado de cant_ids va a ser 0

    results = collection.get(include=['documents'])
    cant_ids  = len(results['ids']) # va dar el resultados de cuantos id hay cargados

    lista_ids = [f"id{cant_ids+i+1}" for i in range(len(chunks))] #se va a generar tantos ids como chunks haya y además unicos 
    collection.add(
        documents = chunks, 
        ids= lista_ids,
        embeddings=embeddings,
        metadatas=[{"file": document.get("file"), "title": document.get("title") ,"description": document.get("description")} for _ in chunks]
    )
    raise HTTPException(status_code=200, detail="Documento cargado en la base de datos!")


def get_retrieve_context(collection,query_embedding):  
    #Recupera los documentos mas relevantes (en este caso 10) para mi contexto

    context_data = collection.query(
            query_embeddings= query_embedding,
            n_results=10
            )
    return context_data #diccionario 
    