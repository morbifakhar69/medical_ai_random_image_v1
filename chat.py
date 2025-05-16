import streamlit as st    
import time 

#@st.dialog("Sind Sie sicher?")
def appointment_dialog():
    
 with st.popover("Chat beenden"):
    st.markdown("Sind Sie sicher?")
    if st.button("Ja"):
        st.session_state["button_clicked"]="Ja"
        print("Button Clicked")
        st.write(f"You decided for: {st.session_state['button_clicked']}")
        st.session_state["page"] = "thanks"
        st.rerun()
    
    if st.button("Nein"):
        st.session_state["button_clicked"]="Nein"
        st.rerun()


def create_appointment_bttns(): 
    with st.popover('Möchten Sie einen Arzttermin vereinbaren?', use_container_width=True):
        st.button("Ja", key="btn1",
                  on_click=lambda: st.session_state.update(button_clicked="Termin vereinbaren"), use_container_width=True)
        st.button("Nein", key="btn2",
                  on_click=lambda: st.session_state.update(button_clicked="Do not make appointment"), use_container_width=True)

def get_assistant_response():
    msg = st.session_state.assistant.messages[-1]
    response = st.session_state.assistant.chat(msg["content"])
    return response

def chat_page(): 
    if "messages" not in st.session_state:
        st.session_state.messages = st.session_state.assistant.messages
    
    st.subheader("Chat", divider="gray")
    st.markdown("Bei den Antworten des künstlich intelligenten Assistenten kann es zu zeitlichen Verzögerungen kommen")
   # st.markdown("Schildern Sie dem Assistenten Ihre Situation. Sie können auch einen Termin bei unserem Arzt buchen")

    with st.chat_message("assistant"): 
        st.markdown("Hallo! Wie kann ich Ihnen helfen?")


    # ✅ Display chat messages from session state
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Stellen Sie eine Frage"):
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # ✅ Append user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # ✅ Get assistant response and store it (prevent duplicate display)
        with st.spinner("Einen Moment bitte"):
            assistant_response = get_assistant_response()
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    with st.container():
        if st.session_state.messages: 
                appointment_dialog()
            #create_appointment_bttns()

