import streamlit as st
def welcome_page():
    st.title("Herzlich willkommen!")
    st.markdown("""
    Mit dieser App können Sie eine erste Einschätzung zu auffälligen Hautveränderungen erhalten und darauf basierend entscheiden, ob Sie einen Arzttermin vereinbaren möchten.

    **So funktioniert es:**
    1. **Fragebogen auf der folgenden Seite ausfüllen** – Damit die Interaktion mit dem künstlich intelligenten Assistenten besser auf Sie abgestimmt werden kann. 
    \n
    2. **Hochgeladenes Foto** -  Sehen Sie sich ein Bild einer auffälligen Hautstelle genau an 
    \n
    3. **Mit dem KI-Assistenten chatten** – Interagieren Sie mit dem künstlich intelligenten Assistenten und entscheiden Sie darauf basierend, ob Sie einen Arzttermin vereinbaren möchten.
    """)
    if st.button("Zum Fragebogen"):
        st.session_state["page"] = "survey"
        st.rerun()