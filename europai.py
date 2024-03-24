from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import streamlit as st
import os
import yaml

api_key = st.secrets["MISTRAL_API_KEY"]

model = "mistral-small-latest"
# Function to reset the state
def reset_state():
    for key in st.session_state:
        del st.session_state[key]

def load_config(config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)



def main():
    st.set_page_config(
        page_title="EuropAI: Votre Assistant pour les élections européennes de 2024", page_icon="🇪🇺")
    st.image('Euroailogo.png')
   

    st.title("🇪🇺 EuropAI: Votre Assistant pour les élections européennes de 2024")
    multiline_text = """
    EuropAI est une intelligence artificielle créé par la société <span style="color: #007bff;">ALP</span><span style="color: #eb0a14;">AI</span>
    <br>
    Développé uniquement à partir de technologies open source et basé sur Mistral un modèle de langage français.
    Le but d'Europai  et d'apporter le maximum d'informations possibles aux citoyens français à propos des élections européennes 2024  et du fonctionnement de l'union européenne, pour leur permettre de faire un choix dans l'isoloir.
    <br>Bien entendu,comme toutes les intelligences artificielles actuellement sur le marché, Europai peut faire des erreurs. 
    Envisagez de vérifier les informations importantes.
    """
    

    st.markdown(multiline_text, unsafe_allow_html=True)
    client = MistralClient(api_key=api_key)

    # Initialize the model in session state if it's not already set
    if "mistral_model" not in st.session_state:
        st.session_state["mistral_model"] = "mistral-small-latest"

    
    #definition avatars chat
    avatars = {"human": "📩", "user": "📩","ai": "🇪🇺",'assistant':"🇪🇺"}
    config_path='config/config.yaml'
    config=load_config(config_path)
   # Add system prompt input
    
    if "system_prompt" not in st.session_state:
        file=open("Europai.txt",'r')
        context=file.read()
        st.session_state["system_prompt"] = context

    if "messages" not in st.session_state:
      st.session_state.messages = []

    # Add system prompt as a ChatMessage if it doesn't exist
    if st.session_state["system_prompt"] and not any(message.role == "system" for message in st.session_state.messages):
        st.session_state.messages.insert(0, ChatMessage(role="system", content=st.session_state["system_prompt"]))

    for message in st.session_state.messages:
        if message.role != "system":  # Skip system messages for UI
            with st.chat_message(avatars[message.role]):  # Use dot notation here
                st.markdown(message.content)  # And here

    if prompt := st.chat_input("Quelle est votre question à propos des élections européenne?"): 
        new_message = ChatMessage(role="user", content=prompt)
        st.session_state.messages.append(new_message)
        with st.chat_message(avatars["user"]):
            st.markdown(prompt)

        with st.chat_message(avatars["assistant"]):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat_stream(
                model=st.session_state["mistral_model"],
                temperature=0,
                messages=st.session_state.messages,  # Pass the entire messages list
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append(ChatMessage(role="assistant", content=full_response))
    
        # Display the Groq logo
    col, col2, col3 = st.columns([1,1,1])
    with col:
        multidesc="""
        <div style="background-color: rgb(14, 17, 23); color: white; font-size: 22px; display: inline-flex;"><a href="https://alpai.eu">
        <span style="color: #0091cc;">ALP</span><span style="color: #eb0a14;">AI</span>
        """
        st.markdown(multidesc, unsafe_allow_html=True)
        st.image('Alpai-logo-petit-large.png'); 
        st.markdown("</a></div>",unsafe_allow_html=True)

    with col2:
        multidesc3="""
        
        """
        st.markdown(multidesc3, unsafe_allow_html=True)
        
    with col3:
        multidesc3="""
        <div style="background-color: rgb(14, 17, 23); color: white; font-size: 22px; display: inline-flex;"><a href="https://mistral.ai">
        Mist<span style="color: #fe4900;">ralAI</span>
        """
        st.markdown(multidesc3, unsafe_allow_html=True)
        st.image('mistralai-logo.png')
        st.markdown("</a></div>",unsafe_allow_html=True)
    
   

if __name__ == "__main__":
    main()
