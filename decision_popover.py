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
        st.image(resized_image, caption="Hochgeladenes Foto",use_column_width=True)
        #st.markdown('</div>', unsafe_allow_html=True)

