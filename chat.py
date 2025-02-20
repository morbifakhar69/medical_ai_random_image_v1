import streamlit as st    
from icecream import ic
def get_assistant_response():
    msg = st.session_state.assistant.messages[-1]
    response = st.session_state.assistant.chat(msg["content"])
    return response
def chat_page(): 

    if "messages" not in st.session_state:
        # st.session_state.assistant = XAIAssistant()
        st.session_state.messages = st.session_state.assistant.messages

    # Display chat messages
    for msg in st.session_state.assistant.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Wie kann ich helfen?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.assistant.messages.append({"role": "user", "content": prompt})

        # Add user message to chat history
        # Get assistant's response
        with st.spinner("Bin gleich wieder da..."):
            response = get_assistant_response()
            st.session_state.assistant.messages.append({"role": "assistant", "content": prompt})

        # Display assistant's response in chat message container
        with st.chat_message("assistant"):
            message_placeholder=st.empty()
            message_placeholder.markdown(response)
            #st.markdown(response)