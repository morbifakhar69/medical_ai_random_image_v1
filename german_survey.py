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

    st.title("Umfrage")


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

    options_final = [
      "Starke Ablehnung",  "Ablehnung", "Neutral",  "Zustimmung", "Starke Zustimmung"

             ]

    #st.subheader("Fragebogen", divider='gray')
    
    responses= {}
    # with st.form(key="my_form"):
    #     for idx, q in enumerate(questions):
    #         q_key = f"q{idx + 1}"
    #         selected_option = st.select_slider( q["question"], options = options_final, key= q_key, value = "Neutral")
    #         st.session_state["survey"]["responses"][q_key] = selected_option
    #         st.subheader("",divider='gray')
    #         responses[q_key]=selected_option

    with st.form(key="my_form"):
        st.markdown("Bitte geben Sie Ihre ID ein")
        uuid = st.text_input("ID", value=st.session_state["survey"].get("ID", ""))
        #age = st.number_input("Alter", value=st.session_state["survey"].get("age", 18), min_value=0, max_value=100)
       # age = st.number_input("Alter", value=st.session_state["survey"].get("age", 18), min_value=0, max_value=100)

        
        st.subheader("",divider='gray')
        st.markdown("Lesen Sie bitte jede dieser Aussagen aufmerksam durch und überlegen Sie, ob diese Aussage auf Sie persönlich für die letzten 6 Monate zutrifft oder nicht.")
        st.markdown("")
        #st.subheader("",divider='gray')

        for idx, q in enumerate(questions):
            q_key = f"q{idx + 1}"
            st.markdown(q["question"])
            selected_option = st.radio( q["question"],  options_final,index=None, label_visibility="collapsed")
            st.session_state["survey"]["responses"][q_key] = selected_option
            st.subheader("",divider='gray')
            responses[q_key]=selected_option

        # Submit button
        submit_button = st.form_submit_button("Absenden")

    if submit_button:
        
        if uuid == "":
            st.error("Bitte geben Sie Ihre ID ein.")

        
        else:
            st.session_state['uuid']=uuid
            st.session_state["survey"]["uuid"] = uuid
            #st.session_state["survey"]["gender"] = gender
            #st.session_state["survey"]["skin_color"] = skin_color
            st.session_state["survey"].update(responses)
            st.session_state["page"] = "chat"
            st.success("Vielen Dank für Ihre Antworten!")
            #st.write("### Ihre Auswahl:")
        

       

            for idx, q in enumerate(questions):
                selected_options = st.session_state["survey"]["responses"].get(f"q{idx}", [])
                st.write(f"**Q{idx}:** {', '.join(selected_options) if selected_options else 'Keine Auswahl'}")

            st.session_state["page"] = "chat"
            print('Survey Data: ',st.session_state["survey"] )
            st.rerun()
