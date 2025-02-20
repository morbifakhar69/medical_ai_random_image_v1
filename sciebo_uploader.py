import os
import json
import requests
import streamlit as st
from config import UPLOAD_FOLDER,SCIEBO_USERNAME,SCIEBO_PASSWORD,SCIEBO_APPNAME,SCIEBO_IMAGE_BASEURL,SCIEBO_STATE_BASEURL,STATE_FOLDER     # Import upload directory from config


class Sciebo:
    """
    Sciebo WebDAV Handler Class to upload images and session state data.
    """

    # Sciebo WebDAV Credentials
    SCIEBO_USERNAME =SCIEBO_USERNAME
    SCIEBO_PASSWORD = SCIEBO_PASSWORD # this is app password
    SCIEBO_APPNAME = SCIEBO_APPNAME
    SCIEBO_IMAGE_BASEURL = SCIEBO_IMAGE_BASEURL
    SCIEBO_STATE_BASEURL = SCIEBO_STATE_BASEURL

    @classmethod
    def upload_image(cls, file_path,uuid):
        """
        Uploads an image to the Sciebo directory 'medical_ai/images/'.

        :param file_path: Local path of the image to be uploaded.
        """
        if not os.path.exists(file_path):
            st.error("❌ File not found: " + file_path)
            return

        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_path)[1]
        sciebo_url = f"{cls.SCIEBO_IMAGE_BASEURL}{uuid}{file_extension}"

        try:
            print('Trying to upload image in Sciebo.')
            with open(file_path, "rb") as file:
                response = requests.put(sciebo_url, data=file, auth=(cls.SCIEBO_USERNAME, cls.SCIEBO_PASSWORD))

            if response.status_code in [201, 204]:
                st.success(f"✅ Image '{file_name}' uploaded successfully to Sciebo.")
            else:
                st.error(f"❌ Failed to upload image. Sciebo Response: {response.status_code}")
                print(response.text)

        except Exception as e:
            st.error(f"⚠️ Error uploading image: {str(e)}")

    @classmethod
    def upload_state_data(cls,uuid):

        if not uuid:
            st.error("❌ User UUID not found in session state.")
            return

        user_uuid = uuid
        json_file_name = f"{user_uuid}.json"
        json_file_path = os.path.join(STATE_FOLDER, json_file_name)

        try:
            # Convert session state to JSON
            print('Trying to upload state data in Sciebo.')
            # Upload to Sciebo
            sciebo_url = f"{cls.SCIEBO_STATE_BASEURL}{json_file_name}"
            with open(json_file_path, "rb") as file:
                print('State json file is found and ready to upload')
                response = requests.put(sciebo_url, data=file, auth=(cls.SCIEBO_USERNAME, cls.SCIEBO_PASSWORD))

            if response.status_code in [201, 204]:
                st.success(f"✅ Session state uploaded successfully as '{json_file_name}' to Sciebo.")
            else:
                st.error(f"❌ Failed to upload session state. Sciebo Response: {response.status_code}")

        except Exception as e:
            st.error(f"⚠️ Error saving/uploading session state: {str(e)}")
