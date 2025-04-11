import streamlit as st
import time
from images import show_images,show_upload_images
from styling import decision_page_styling
from icecream import ic



@st.dialog("Cast your vote")
def make_appointment():
    st.write(" Do you really wish to take an appointment?")
    col1, col2 = st.columns([1, 1])
    with col1.button("Yes"):
        st.session_state['button_clicked'] = "Make appointment"
    with col1.button("Yes"):
        st.session_state['button_clicked'] = "Make appointment"

def decision():
    # TODO: Format that buttons are "more beautiful"
    IMAGE_WIDTH = 300
    IMAGE_HEIGHT = 300

    # CSS styles for button-17 and layout
    styles = decision_page_styling()
    # Inject CSS styles
    main_container=st.container()
    main_container.markdown(styles, unsafe_allow_html=True)

    button_container=st.container()
    col1, col2 = button_container.columns([0.7,0.4])

    # Check if 'button_clicked' is in session_state, if not, initialize it to None
    if 'button_clicked' not in st.session_state:
        st.session_state["button_clicked"] = None


    with col1:

        image=show_upload_images() #new updated upload image module
        resized_image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        st.image(resized_image, caption="Uploaded Image", use_column_width=True)
    with col2:
        if not st.session_state["button_clicked"]:
            make_appointment()


    #st.markdown(set_title_styling(), unsafe_allow_html=True)

    if st.session_state["button_clicked"]:
        print("Button Clicked")
        print(f"You decided for: {st.session_state['button_clicked']}")
        st.write(f"You decided for: {st.session_state['button_clicked']}")
        time.sleep(1)
        st.session_state["page"] = "thanks"
        # had to add rerun() to make the page change. Otherwise it only worked after clicking a button twice -> TODO: find out why and fix
        st.experimental_rerun()



