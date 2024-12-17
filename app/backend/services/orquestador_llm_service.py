from dotenv import load_dotenv
import cohere
import os
from models.input_query_model import Query


load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

co = cohere.ClientV2()


def orquestador_llm(query : Query):

    prompt = f"""
    ###
    Instrucciones:
    -Responder en no mas de 70 palabras.
    -Responder de manera positiva, con un tono entusiasta
    ###
    Consulta:
    {query}
    """
    
    response = co.chat(
        model="command-r-plus-08-2024",
        messages=[
            {"role": "system", "content":"Responde consejos utiles, como si fueras un tutor"},
            {"role": "user", "content": prompt}
        ],
    )
    return {"message": response.message.content[0].text}