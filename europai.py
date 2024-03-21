import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_groq import ChatGroq
import os
import json

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
    
        
   

    if 'chat_message' not in st.session_state:
     st.session_state['chat_history']=[]
    test=StreamlitChatMessageHistory()
    msgs = test
   
    if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
        msgs.clear()
        msgs.add_ai_message("comment puis je vous aider?")
        st.session_state.chat_history = {}

    avatars = {"human": "📩", "user": "📩","ai": "🇪🇺",'assistant':"🇪🇺"}
    for idx, msg in enumerate(msgs.messages):
        with st.chat_message(avatars[msg.type]):
            st.markdown(msg.content)

    if prompt := st.chat_input(placeholder="Quel est votre question concernant les elections 2024?"):
        st.chat_message(avatars["user"]).markdown(prompt)
        msgs.add_user_message(prompt)
        model = 'mixtral-8x7b-32768'

        llm = ChatGroq(
                temperature=0,
                groq_api_key=st.secrets["GROQ_API_KEY"],
                model_name=model,
                streaming=True,
                
            )
        file=open("Europai.txt",'r')
        context=file.read()

        final_prompt=f"""utilises les consignes et informations du contexte pour répondre EN FRANCAIS a la demande de l'utilisateur:
        
        <context>
            {context}
        </context>

        question de l'utilisateur : {prompt}
        
        \n\n
        répond en francais
        \n\n
        you use a lot of emoji in your answer
        assistant:

        """
        response2 = llm.invoke(final_prompt)
        
        with st.chat_message(avatars["ai"]):
            chat_box = st.empty()
            chat_box.markdown(response2.content)

            msgs.add_ai_message(response2.content)
        #sauvegarde l'état de la session historique du chat et param llm
        
    # Display the Groq logo
    col, col1, col2, col3 = st.columns([1,1,1,1])
    with col:
        multidesc="""
        <div style="background-color: rgb(14, 17, 23); color: white; font-size: 22px; display: inline-flex;">
        <span style="color: #0091cc;">ALP</span><span style="color: #eb0a14;">AI</span>
        """
        st.markdown(multidesc, unsafe_allow_html=True)
        st.image('Alpai-logo-petit-large.png'); 
        st.markdown("</div>",unsafe_allow_html=True)
    with col1:
        multidesc2="""
        <div style="background-color: rgb(14, 17, 23); color: white; font-size: 22px; display: inline-flex;">
        GROQ<span style="color: #f55036;">CLOUD</span>
        """
        st.markdown(multidesc2, unsafe_allow_html=True)
        st.image('groqcloud_darkmode90.png')
        st.markdown("</div>",unsafe_allow_html=True)

    with col2:
        multidesc3="""
        <div style="background-color: rgb(14, 17, 23); color: white; font-size: 22px; display: inline-flex;">
        stream<span style="color: #ff4b4b;">lit</span>
        """
        st.markdown(multidesc3, unsafe_allow_html=True)
        st.image('streamlit-logo.png')
        st.markdown("</div>",unsafe_allow_html=True)
    with col3:
        multidesc3="""
        <div style="background-color: rgb(14, 17, 23); color: white; font-size: 22px; display: inline-flex;">
        Mist<span style="color: #fe4900;">ralAI</span>
        """
        st.markdown(multidesc3, unsafe_allow_html=True)
        st.image('mistralai-logo.png')
        st.markdown("</div>",unsafe_allow_html=True)


if __name__ == "__main__":
    main()
