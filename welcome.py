import streamlit as st
def welcome_page():
    st.title("Willkommen bei unserer App")
    st.write("Dies ist eine Einführungsseite. Klicken Sie auf die Schaltfläche unten, um die Umfrage zu starten.")
    if st.button("Umfrage starten"):
        st.session_state["page"] = "survey"
        st.rerun()