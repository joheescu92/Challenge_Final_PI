import chromadb
import os
from fastapi import HTTPException
from chromadb.config import Settings
from models.metadata_document_model import Metadata_Document
from utils.vector_database_util import add, get_retrieve_context

# Configurar el directorio de persistencia
PERSIST_DIR = "./data/chromadb"

# Asegurarse de que el directorio exista
os.makedirs(PERSIST_DIR, exist_ok=True)


# Crear un cliente ChromaDB con persistencia
chroma_client = chromadb.Client(Settings(persist_directory=PERSIST_DIR, is_persistent=True))


collection = chroma_client.get_or_create_collection(name="UOCRA", 
                                                    metadata={"hnsw:space": "ip"},
                                               )  #calculo de distancia con producto punto

 

def document_in_db(document_name: str):

    results = collection.get(include=["metadatas"])

    file_names = list({metadata["file"] for metadata in results["metadatas"] if "file" in metadata})

    for file in file_names:
        if file == document_name:
            return True
    return False




def add_documents(chunks,embeddings, document : Metadata_Document):
    return add(chunks,embeddings,document,collection)
    


def consulta_db(document_name: str):
    
    results=collection.get(where={"file": {"$eq": document_name}})
    
    if not results['documents']:
        raise HTTPException(status_code=404, detail="Documento no encontrado en la base de datos vectorial")

    return results
    


def get_context(query_embedding):
    return get_retrieve_context(collection,query_embedding)