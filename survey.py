import streamlit as st
from tipi import calculate_scores
from icecream import ic


def submit_survey():
    st.session_state["survey_completed"] = True
    st.session_state["tipi_scores"] = calculate_scores(st.session_state)
    st.session_state["page"] = "chat"


def survey():
    if "survey" not in st.session_state:
        st.session_state["survey"] = {}

    st.title("Survey")
    st.write("Please fill out the survey below:")

    # Likert scale options
    options = [
        "Disagree strongly",
        "Disagree moderately",
        "Disagree a little",
        "Neither agree nor disagree",
        "Agree a little",
        "Agree moderately",
        "Agree strongly"
    ]

    questions = [
        "I see myself as extraverted, enthusiastic.",
        "I see myself as critical, quarrelsome.",
        "I see myself as dependable, self-disciplined.",
        "I see myself as anxious, easily upset.",
        "I see myself as open to new experiences, complex.",
        "I see myself as reserved, quiet.",
        "I see myself as sympathetic, warm.",
        "I see myself as disorganized, careless.",
        "I see myself as calm, emotionally stable.",
        "I see myself as conventional, uncreative."
    ]

    with st.form(key='my_form'):
        name = st.text_input("Name", value=st.session_state["survey"].get("name", ""))
        age = st.number_input("Age", value=st.session_state["survey"].get("age", 18), min_value=0, max_value=100)

        # Abfrage nach Geschlecht
        gender = st.radio("Gender", ["Male", "Female"],
                          index=0 if st.session_state["survey"].get("gender", "Male") == "Male" else 1)

        # Abfrage nach Hautfarbe
        skin_color = st.radio("Skin Color", ["White", "Black"],
                              index=0 if st.session_state["survey"].get("skin_color", "White") == "White" else 1)

        responses = {}
        for i, question in enumerate(questions):
            q_key = f"q{i + 1}"
            response = st.select_slider(question, options=options, key=q_key,
                                        value=st.session_state["survey"].get(q_key, options[3]))
            responses[q_key] = response

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            st.session_state["survey"]["name"] = name
            st.session_state["survey"]["age"] = age
            st.session_state["survey"]["gender"] = gender
            st.session_state["survey"]["skin_color"] = skin_color
            st.session_state["survey"].update(responses)
            st.session_state["page"] = "chat"
            st.rerun()
