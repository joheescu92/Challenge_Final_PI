from fastapi import HTTPException
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_path_document(document_name : str):
    ruta = './documents'

    if os.path.exists(ruta) and os.path.isdir(ruta):
        for archivo in os.listdir(ruta):
            if archivo == document_name:
                ruta_completa = os.path.join(ruta, archivo)
                return ruta_completa
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    

def get_chunks(content_document: str):
    
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 307,
    chunk_overlap = 50,
    length_function = len,
    )

    chunks = text_splitter.split_text(content_document)
    return chunks