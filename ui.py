# streamlit run .\ui.py --theme.base="light" --server.port=11434 --server.address=0.0.0.0 --server.headless=true

import streamlit as st
import uuid
from askingIA import askingIA
from prompt import general, python, manon
from PIL import Image

favicon = Image.open("./logo.png")

st.set_page_config(
    page_title= "Ollama chat", 
    layout="wide",
    page_icon = favicon,
    initial_sidebar_state="auto",
)

url = 'http://localhost:11434/api/chat'
model = "llama3:8b"


padding_top=5
hide_streamlit_style = f"""
<style>
#MainMenu {{visibility: hidden;}}
.appview-container .main .block-container{{padding-top: {padding_top}rem;}}
footer {{visibility: hidden;}}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


def generate_unique_id():
    return str(uuid.uuid4())

@st.cache_resource(ttl=3600)
def load_data():
    history = {

        "General" : [
            {
                "role": "user",
                "content" : general
            }
        ],

        "Developpement Python" : [
            {
                "role": "user",
                "content" : python
            }
        ],
        "Manon" : [
            {
                "role": "user",
                "content" : manon
            }
        ]
    }
    return history

history = load_data()

def add_object(json, domain):
    for key in history:
        if key == domain:
            history[key].append(json)

def get_history(domain):
    for key in history:
        if key == domain:
            return history[key]

categories = ["General","Developpement Python", "Manon"]
selected_categories = st.sidebar.selectbox("Select a specific domain", categories)
user_input = st.chat_input("Say something")


messages_container = st.container(height=650)


if user_input:

    message = user_input
    user_unique_id = generate_unique_id()
    user_object = {
        "id": user_unique_id,
        "role": "user",
        "content": message
    }
    add_object(user_object, selected_categories)
    messages = get_history(selected_categories)

    IA_response = askingIA(url, model, messages)

    print("-------------")
    print(IA_response)

    ia_unique_id = generate_unique_id()
    IA_object = {
        "id" : ia_unique_id,
        "role": "assistant",
        "content": IA_response
    }
    add_object(IA_object, selected_categories)

    messages = get_history(selected_categories)

    for message in messages[1:]:
        if message["role"] == "assistant":
            messages_container.chat_message("assistant").write(f"Echo: {message["content"]}")
        else:
            messages_container.chat_message("user").write(f"Echo: {message["content"]}")
else:
    messages = get_history(selected_categories)

    for message in messages[1:]:
        if message["role"] == "assistant":
            messages_container.chat_message("assistant").write(f"Echo: {message["content"]}")
        else:
            messages_container.chat_message("user").write(f"Echo: {message["content"]}")