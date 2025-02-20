import streamlit as st
import time
from images import show_images,show_upload_images
from styling import decision_page_styling,image_container_styling
from icecream import ic


def decision():
    # TODO: Format that buttons are "more beautiful"
    IMAGE_WIDTH = 75
    IMAGE_HEIGHT = 150

    if 'button_clicked' not in st.session_state:
        st.session_state["button_clicked"] = None


#st.markdown('<div class="image-column">', unsafe_allow_html=True)

        #image = show_images()
    image_container=st.container()
    with image_container:
        #image_container.markdown(image_container_styling, unsafe_allow_html=True)
        image=show_upload_images() #new updated upload image module
        height,width=image.size
        height=150
        width=150
        resized_image = image.resize((height,width))
        #st.image(resized_image, caption="Uploaded Image", use_column_width=True)
        st.image(resized_image, caption="Uploaded Image")
        #st.markdown('</div>', unsafe_allow_html=True)

    button_tile=st.container()
    with button_tile.popover('Do you wish to take an appointment?',use_container_width=True):
            st.button("Yes", key="btn1",
                            on_click=lambda: st.session_state.update(button_clicked="Make appointment"),use_container_width=True)
            st.button("No", key="btn2",
                            on_click=lambda: st.session_state.update(button_clicked="Do not make appointment"),use_container_width=True)



    #st.markdown(set_title_styling(), unsafe_allow_html=True)

    if st.session_state["button_clicked"]:
        print("Button Clicked")
        print(f"You decided for: {st.session_state['button_clicked']}")
        st.write(f"You decided for: {st.session_state['button_clicked']}")
        time.sleep(1)
        st.session_state["page"] = "thanks"
        # had to add rerun() to make the page change. Otherwise it only worked after clicking a button twice -> TODO: find out why and fix
        st.experimental_rerun()



