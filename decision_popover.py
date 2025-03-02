import streamlit as st
import time
from images import show_images,show_upload_images
from styling import decision_page_styling,image_container_styling
from icecream import ic


def decision():


    if 'button_clicked' not in st.session_state:
        st.session_state["button_clicked"] = None


#st.markdown('<div class="image-column">', unsafe_allow_html=True)

        #image = show_images()
    image_container=st.container()
    with image_container:
       
        image=show_upload_images() #new updated upload image module
        height,width=image.size
        height=250
        width=250
        resized_image = image.resize((height,width))
        #st.image(resized_image, caption="Uploaded Image", use_column_width=True)
        st.image(resized_image, caption="Hochgeladenes Bild",use_column_width=True)
        #st.markdown('</div>', unsafe_allow_html=True)

    button_tile=st.container()
    with button_tile.popover('Möchten Sie einen Termin vereinbaren?',use_container_width=True):
            st.button("Ja", key="btn1",
                            on_click=lambda: st.session_state.update(button_clicked="Termin vereinbaren"),use_container_width=True)
            st.button("Nein", key="btn2",
                            on_click=lambda: st.session_state.update(button_clicked="Keinen Termin vereinbaren"),use_container_width=True)



    #st.markdown(set_title_styling(), unsafe_allow_html=True)

    if st.session_state["button_clicked"]:
        print("Button Clicked")
        print(f"You decided for: {st.session_state['button_clicked']}")
        st.write(f"You decided for: {st.session_state['button_clicked']}")
        time.sleep(1)
        st.session_state["page"] = "thanks"
        # had to add rerun() to make the page change. Otherwise it only worked after clicking a button twice -> TODO: find out why and fix
        st.experimental_rerun()



