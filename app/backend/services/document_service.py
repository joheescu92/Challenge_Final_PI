import os
from fastapi import HTTPException
from utils.document_util import get_path_document, get_chunks
from langchain_community.document_loaders import PyPDFLoader

#opté por esta forma de carga de pdf recomendada en la documentación de Langchain
#https://python.langchain.com/docs/how_to/document_loader_pdf/
#pero con una breve modificación para guardarme en la variable document solamente el contenido de cada página


def upload_document(document_name: str):

    path = get_path_document(document_name) #ruta cargada

    loader = PyPDFLoader(path)

    content_document = ""

    for page in loader.lazy_load():
        content_document += page.page_content

    return content_document
    
    #chunks = get_chunks(content_document)

    





    

    