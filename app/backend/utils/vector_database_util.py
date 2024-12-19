from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.metadata_document_model import Metadata_Document
import os
from fastapi import HTTPException


def add(chunks,embeddings,document: Metadata_Document,collection):
    lista_ids = [f"id{i+1}" for i in range(len(chunks))] #se va a generar tantos ids como chunks 
    collection.add(
        documents = chunks, 
        ids= lista_ids,
        embeddings=embeddings,
        metadatas=[{"file": document.get("file"), "title": document.get("title") ,"description": document.get("description")} for _ in chunks]
    )
    raise HTTPException(status_code=200, detail="Documento cargado en la base de datos!")


def get_retrieve_context(collection,query_embedding):  

    context_data = collection.query(
            query_embeddings= query_embedding,
            n_results=10
            )
    return context_data #diccionario 
    