from fastapi import HTTPException
import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.metadata_document_model import Metadata_Document

def get_path_document(document_name : str):
    ruta = './documents'

    if os.path.exists(ruta) and os.path.isdir(ruta):
        for archivo in os.listdir(ruta):
            if archivo == document_name:
                ruta_completa = os.path.join(ruta, archivo)
                return ruta_completa
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    

def get_chunks(content_document: str, document: Metadata_Document ):
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = document.get("chunks"),
        chunk_overlap = document.get("overlap"),
        length_function = len,
        )
        chunks = text_splitter.split_text(content_document)
        return chunks
        
    