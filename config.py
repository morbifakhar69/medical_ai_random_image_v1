import streamlit as st

OPENAI_API_KEY = st.secrets["openai"]["SECRET_KEY"]
ASSISTANT_ID = None
UPLOAD_FOLDER=st.secrets["server"]["UPLOAD_FOLDER"]
STATE_FOLDER=st.secrets["server"]["STATE_FOLDER"]
SCIEBO_USERNAME=st.secrets["sciebo"]["SCIEBO_USERNAME"]
SCIEBO_PASSWORD=st.secrets["sciebo"]["SCIEBO_PASSWORD"] #this is app password
SCIEBO_APPNAME=st.secrets["sciebo"]["SCIEBO_APPNAME"]
SCIEBO_IMAGE_BASEURL= st.secrets["sciebo"]["SCIEBO_IMAGE_BASEURL"]
SCIEBO_STATE_BASEURL= st.secrets["sciebo"]["SCIEBO_STATE_BASEURL"]