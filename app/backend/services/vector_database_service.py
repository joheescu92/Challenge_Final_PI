import chromadb
import os
from chromadb.config import Settings
from fastapi import HTTPException
from services.document_service import upload_document

# Configurar el directorio de persistencia
PERSIST_DIR = "./data/chromadb"

# Asegurarse de que el directorio exista
os.makedirs(PERSIST_DIR, exist_ok=True)


# Crear un cliente ChromaDB con persistencia
chroma_client = chromadb.Client(Settings(persist_directory=PERSIST_DIR, is_persistent=True))


collection = chroma_client.get_or_create_collection(name="UOCRA")

def document_in_db(document_name: str):

    cantidad_documentos = len(collection.get()["ids"]) #hay que cambiar esto validamos si esta en la db
    if cantidad_documentos == 0:

        return upload_document(document_name)
            

    raise HTTPException(status_code=409, detail="Los documentos ya están cargados.")
