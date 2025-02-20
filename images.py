import streamlit as st
from PIL import Image
import os
import random
import csv
from config import UPLOAD_FOLDER



def save_upload_images(image_file):
    if image_file:
        # Save Image
        file_path = os.path.join(UPLOAD_FOLDER, image_file.name)
        with open(file_path, "wb") as f:
            f.write(image_file.getbuffer())
        st.success(f"✅ Image uploaded successfully")
        st.session_state["saved_image"] = file_path


def load_skin_data():
    skin_data = {}
    with open("skinData.csv", mode='r') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        for row in reader:
            key = row.pop(next(iter(row)))  # Take the first column as the key
            skin_data[key] = row  # Store the remaining columns as a dictionary
    return skin_data



def normalize_skin_color(skin_color):
    # Normalize the skin color to ensure matching between 'Black'/'b' and 'White'/'w'
    if skin_color in ['Black', 'b']:
        return 'b'
    elif skin_color in ['White', 'w']:
        return 'w'
    else:
        return skin_color

def get_images(skin_color):
    if "skin_data" not in st.session_state:
        st.session_state["skin_data"] = load_skin_data()

    if "selected_image_path" not in st.session_state:
        # Normalize the skin color
        normalized_skin_color = normalize_skin_color(skin_color)

        # Filter keys based on normalized skin color
        matching_keys = [key for key, attributes in st.session_state["skin_data"].items() if attributes.get("skin") == normalized_skin_color]

        # Choose a random key from the matching keys
        if matching_keys.__len__()!=0:
            selected_image_key = random.choice(matching_keys)
            image_path=os.path.join("skin_images", selected_image_key)
            st.session_state.selected_image_path = image_path
        print(f'Selected Image path: {image_path}')
    return st.session_state.selected_image_path  # Return the path of the selected image


def show_upload_images():
    if st.session_state.saved_image:
        print(f'Selected Image path in Markdown: {st.session_state.saved_image}')
        image = Image.open(st.session_state.saved_image)
        return image
    else: print('No image in session state found')
def show_images():
    # Überprüfen, ob das Bild bereits ausgewählt wurde

    # Bild öffnen und anzeigen
    if st.session_state.selected_image_path:
        print(f'Selected Image path in Markdown: {st.session_state.selected_image_path}')
        image = Image.open(st.session_state.selected_image_path)
        return image
    else: print('No image in session state found')