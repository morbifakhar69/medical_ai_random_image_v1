import streamlit as st
from tipi import calculate_scores
import json

def submit_survey():
    st.session_state["survey_completed"] = True
    st.session_state["tipi_scores"] = calculate_scores(st.session_state["survey"])
    st.session_state["page"] = "chat"

def survey():
    if "survey" not in st.session_state:
        st.session_state["survey"] = {}

    file_path = "questionarre/deutsch_questionarre_slider.json"

    st.title("📋 Umfrage")
    st.subheader("Demografische Daten", divider='gray')

    # Apply custom CSS for borders
    # User Inputs
    st.text("Bitte geben Sie Ihren Namen ein")
    name = st.text_input("Name", value=st.session_state["survey"].get("name", ""))
    st.text("Bitte wählen Sie Ihr Alter aus dem Dropdown-Menü")

    age = st.number_input("Alter", value=st.session_state["survey"].get("Alter", 18), min_value=0, max_value=100)

    st.text("Bitte wählen Sie das Geschlecht")
    gender = st.radio("Geschlecht", ["Männlich", "Weiblich"],
                      index=0 if st.session_state["survey"].get("gender", "Männlich") == "Männlich" else 1)

    skin_color = st.radio("Hautfarbe", ["Weiß", "Schwarz"],
                          index=0 if st.session_state["survey"].get("skin_color", "Weiß") == "Weiß" else 1)

    # Load questions from JSON
    questions = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            questions = json.load(file)  # Read JSON file
    except FileNotFoundError:
        st.error("❌ Die Datei wurde nicht gefunden. Bitte überprüfen Sie den Pfad.")
        return
    except json.JSONDecodeError:
        st.error("❌ Fehler beim Laden der JSON-Datei. Bitte überprüfen Sie das Format.")
        return

    # Store responses
    if "responses" not in st.session_state:
        st.session_state["survey"]["responses"] = {}

    options = [
      "stimme überhaupt nicht zu",
        "stimme mäßig zu",
        "stimme nicht zu", 
        "stimme wenig zu",
        "stimme weder zu noch widerspreche ich",
        "stimme ein wenig zu",
        "stimme mäßig zu",
        "stimme stark zu"
             ]

    st.subheader("Fragebogen", divider='gray')
    st.text("Im Folgenden finden Sie 14 Fragen mit jeweils 4 Optionen, die für Sie geeignet sind. \nBitte wählen Sie aus, was für Sie am besten geeignet ist")
    
    responses= {}
    with st.form(key="my_form"):
        for idx, q in enumerate(questions):
            q_key = f"q{idx + 1}"
            selected_option = st.select_slider( q["question"], options = options, key= q_key, value = st.session_state["survey"].get(q_key,options[3]))
            st.session_state["survey"]["responses"][q_key] = selected_option
            st.subheader("",divider='gray')
            responses[q_key]=selected_option

        # Submit button
        submit_button = st.form_submit_button("Absenden ✉️")

    if submit_button:
        st.session_state["survey"]["name"] = name
        st.session_state["survey"]["age"] = age
        st.session_state["survey"]["gender"] = gender
        st.session_state["survey"]["skin_color"] = skin_color

        st.success("🎉 Vielen Dank für Ihre Antworten!")
        st.write("### Ihre Auswahl:")

        for idx, q in enumerate(questions):
            selected_options = st.session_state["survey"]["responses"].get(f"q{idx + 1}", [])
            st.write(f"**Q{idx + 1}:** {', '.join(selected_options) if selected_options else 'Keine Auswahl'}")

        st.session_state["page"] = "chat"
        print('Survey Data: ',st.session_state["survey"] )
        st.rerun()
