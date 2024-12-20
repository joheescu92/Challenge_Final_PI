from models.message_model import Message


def primera_instancia(co,query: str):
    system_prompt = """
    Te llamas UOCRAIA, chatbot creado a disposicion de los trabajadores de construccion para ayudar en sus dudas,
    Tu tarea es decidir si la consulta del usuario debe pasar por una Aplicacion RAG
    """

    prompt = f"""
    ####
    Instrucciones:
    -solo puedes contestar de dos maneras diferentes unicamente que son las siguientes:
    -si el usuario agradece, saluda, se despide sin preguntar nada o pide informacion sobre ti, debes de contestarle amigablemente y en torno entusiasta
    -si el usuario pregunta o consulta algo, debes contestar con una sola palabra que es "rag"
    ###
    Pregunta:
    {query}
    """
    #usé command-r-plus-08-2024 último modelo proporcionado por cohere, considero que tiene una
    #calidad de respuesta mejor que el resto y por eso opté por este
    check_response = co.chat(
        model="command-r-plus-08-2024", 
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": prompt}],
        temperature=0 #esto es para lograr que para la misma pregunta siempre conteste lo más similar posible

    )

    return check_response.message.content[0].text


def rerank_responses(co,query,responses):
    rerank_responses = co.rerank(
        query= query,
        documents= responses,
        top_n = 5,
        model = "rerank-v3.5" #modelo mas nuevo de cohere para rerank y ademas soporta multilenguajes
    ) # esto me da un objeto, me voy a quedar solo con los indices de los documentos mas precisos para la query en question
    
    lista_indices_reranking = [result.index for result in rerank_responses.results] #me quedo con una lista de los indices de la lista de contexto
    
    return lista_indices_reranking



def tercera_instancia_context(co,query,documentos_re_rank):
    system_prompt = """
    Actua como analizador de contexto, solo puedes responder con "si" o "no"
    """


    prompt = f"""
    La pregunta puede responderse utilizando el contexto?
    -Debes responder unicamente "si" o "no"
    ###
    CONTEXTO:
    {documentos_re_rank}
    ###
    Pregunta:
    {query}
    """
    check_response = co.chat(
        model="command-r-plus-08-2024", 
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": prompt}],
        temperature=0 #esto es para lograr que para la misma pregunta siempre conteste lo más similar posible

    )
    
    return check_response.message.content[0].text
    
def final_response(co,query,documentos_re_rank):

    

    system_prompt = """
    Tu tarea es responder las preguntas manera con las siguientes instrucciones:
    -debes responder de manera entusiasta
    -debes utilizar solamente el contexto como base de tu informacion unicamente
    """

    prompt = f"""
    ####
    Instrucciones:
    -Tienes que contestar en no mas de 3 oraciones
    -siempre debes contestar en español
    ###
    Contexto:
    {documentos_re_rank}
    ###
    Pregunta:
    {query}
    """
    check_response = co.chat(
        model="command-r-plus-08-2024", 
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": prompt}],
        temperature=0 
    )

    response = Message(message=check_response.message.content[0].text)
    return response