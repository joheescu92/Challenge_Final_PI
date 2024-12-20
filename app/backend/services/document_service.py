import json
from fastapi import HTTPException
from utils.document_util import get_path_document, get_chunks
from langchain_community.document_loaders import PyPDFLoader
from utils.vector_database_util import add
#from services.orquestador_service import get_embeddings_documents

#opté por esta forma de carga de pdf recomendada en la documentación de Langchain
#https://python.langchain.com/docs/how_to/document_loader_pdf/
#pero con una breve modificación para guardarme en la variable document solamente el contenido de cada página

#Logica de negocio del documento

def get_content_document(document_name: str):

    ruta = './metadatas/metadata_documents.json' 

    with open(ruta, "r") as json_file:
        data = json.load(json_file)   #nos traemos la metadata precargada desde el archivo json

    for document in data:

        if document.get("file") == document_name:

            path = get_path_document(document_name) #ruta cargada

            loader = PyPDFLoader(path) #con esta funcion cargamos el documento

            content_document = ""

            for page in loader.lazy_load():
                content_document += page.page_content
            
            return {"document": document, "content": content_document}
        
    raise HTTPException(status_code=404, detail="Documento no encontrado en el fichero metadata")



def get_chunks_document(content_document,document):
    chunks = get_chunks(content_document,document)
    return chunks


        



    





    

    