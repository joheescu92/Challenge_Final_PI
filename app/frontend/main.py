import streamlit as st
import requests

st.set_page_config("UOCRAIA") # titulo de la pag web
st.markdown(
    """
    <h1 style='text-align: center;'>
        UOCRA<span style='color: yellow;'>IA</span>
    </h1>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.title("¡Bienvenido a UOCRAIA!")
    st.write(
        """
        UOCRAIA es un chatbot diseñado para ayudar a los trabajadores
        proporcionándoles información basada en:
        - Convenio Colectivo de Trabajo 76/75
        - CCT Yacimientos Petroliferos y Gasiferos
        """
    )


# Mostrar el mensaje de bienvenida solo una vez si no hay mensajes en el historial
if 'messages' not in st.session_state or len(st.session_state["messages"]) == 0:
    st.session_state["messages"] = [{"role": 'UOCRAIA', 
                                     "message": "Hola! Soy UOCRAIA, chatbot a disposición de los trabajadores para despejar sus dudas. ¿En qué te puedo ayudar?"}]

# Caja de texto para que el usuario escriba su mensaje
user_message = st.chat_input("Escribe tu mensaje aquí...")

# Si el usuario escribe algo, procesamos su mensaje
if user_message:
    # Agregar el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "message": user_message})

    input_data = {"message": user_message}

    response = requests.post('http://backend:8000/POST/query', json=input_data)

    if response.status_code == 200: # si backend responde con codigo 200, nos guardamos la respuesta en respose_data
        response_data = response.json()
        bot_reply = response_data.get('message', 'No se recibió un mensaje válido')
    else:
        st.write(f"Error: {response.status_code}")
        bot_reply = "Hubo un error al comunicarme con el backend."

    # Agregar la respuesta del bot al historial
    st.session_state.messages.append({"role": "UOCRAIA", "message": bot_reply})

# Mostrar los mensajes de la conversación
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["message"])