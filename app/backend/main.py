from fastapi import FastAPI
from routers.document_router import doc_router
from routers.orquestador_router import orq_router
from routers.query_db_router import query_db_router


app = FastAPI(
    title= "Challenge Final",
    description="Challenge Final"
)


@app.get('/', tags=['Home'])
def home():
    return "Hola mundo"


app.include_router(prefix='/POST' ,router= doc_router, tags=['Input Documents'])

app.include_router(prefix='/POST',router=orq_router, tags=['Query'])

app.include_router(prefix='/GET', router=query_db_router, tags=['Query Vector Database'])
