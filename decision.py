import streamlit as st
import time
from images import show_images,show_upload_images
from styling import decision_page_styling
from icecream import ic


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
    col1, col2 = button_container.columns([0.4,0.6])

    if 'button_clicked' not in st.session_state:
        st.session_state["button_clicked"] = None

    #Create buttons in each column

    with col1:
        button_tile=col1.container()
        button_tile.markdown('<div class="question-title">Do you want to take an appointment?</div> <div style="display: flex; flex-direction: column; align-items: center;">', unsafe_allow_html=True)
        col1_btn1, col1_btn2 = button_tile.columns([1, 1])  # Two buttons in one row

        col1_btn1.button("Yes", key="btn1",
                        on_click=lambda: st.session_state.update(button_clicked="Make appointment"),use_container_width=True)
        col1_btn2.button("No", key="btn2",
                           on_click=lambda: st.session_state.update(button_clicked="Do not make appointment"),use_container_width=True)
        button_tile .markdown('</div>', unsafe_allow_html=True)

    with col2:

        image=show_upload_images() #new updated upload image module
        resized_image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        st.image(resized_image, caption="Uploaded Image", use_column_width=True)


    if st.session_state["button_clicked"]:
        print("Button Clicked")
        print(f"You decided for: {st.session_state['button_clicked']}")
        st.write(f"You decided for: {st.session_state['button_clicked']}")
        time.sleep(1)
        st.session_state["page"] = "thanks"
        # had to add rerun() to make the page change. Otherwise it only worked after clicking a button twice -> TODO: find out why and fix
        st.experimental_rerun()



