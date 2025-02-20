def set_image_styling():
    image_style="""
    <style>
        .stImage img {
           
            height: 300px; /* Fixed height for the image container */
            width: 300px;
            object-fit: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden; /* Prevent overflow of the image */
            margin: auto;
        }
    </style>
    """
    return  image_style

# Styling for the buttons
def set_button_styling():
    button_style="""
    <style>
    /* Align buttons below the image */
    .button-container {
        
        display: flex;
        flex-direction: column;
        align-items: center;
    }
            .stButton > button {

        }

    /* Button hover effect */
    .stButton button:hover {
        background-color: #45a049;
        width: 200px; /* Fixed button width */
        height: 100px
        margin-bottom: 10px; /* Spacing between buttons */
    }
    </style>
    """
    return button_style

def set_title_styling():
    title_style="""<h1 style='text-align: center;'>XAI Bot</h1>"""
    return title_style

def set_chat_page_styling():
    chat_style="""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* Apply Roboto font */
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background-color: #121212; /* Match the dark theme background */
        color: white; /* Ensure text is readable */
    }

    /* Center the title and adjust spacing */
    h1 {
        text-align: center;
        font-weight: 700;
        font-size:   4rem;
      
        margin-bottom: 1rem; /* Add small space between title and input */
    }

    /* Chat input adjustments */
    div.st-chat-input {
        margin-top: 0; /* Remove extra space */
        text-align: center; /* Center-align */
    }

    /* Hide the top padding */
    .block-container {
        padding-top: 0;
        padding-bottom: 0;
    }
    </style>
    
    """
    return chat_style

def set_page_styling():
    page_style="""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }

    .stTextInput, .stNumberInput, .stSelectSlider {
        margin-bottom: 10px;
    }
      div.st-chat-input {
        margin-top: -700px; /* Pull chat input closer to the previous element */
    }

    .stTextInput input, .stNumberInput input {
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    .stSelectSlider {
        padding: 10px 0;
    }
    .StyledThumbValue.st-emotion-cache-132r2mp.ew7r33m2 {
        font-family: 'Roboto', sans-serif;
        color: darkgrey;
    }
    .st-emotion-cache-1inwz65.ew7r33m0 {
        font-family: 'Roboto', sans-serif;
        color: darkgrey.
    }

    .st-emotion-cache-1s3l9q9.e1nzilvr5 {
        font-family: 'Roboto', sans-serif;
        color: black.
    }

    .stButton button:hover {
        background-color: #45a049.
    }

    h1 {
        font-weight: 700.
    }

    label {
        font-weight: 400.
        color: #333.
    }
    </style>
    """
    return page_style

def decision_page_styling():
    style="""<style>
    /* Global Styles */
    body {
        background-color: #1e1e2f;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
    }

    /* Responsive Container */
    .container {
        width: 90%;
        max-width: 1200px;
        margin: auto;
        text-align: center;
    }

    /* Question Title with Responsive Font */
    .question-title {
        font-size: 1.5em;
        font-weight: 600;
        text-align: center;
        padding: 10px;
        margin-bottom: 20px;
        color: #000000;
        border: 3px solid #FFFFFF;
        border-radius: 10px;
        background-color: #d9ead3;
    }

    /* Buttons Container (Flexbox for Responsive Layout) */
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        flex-wrap: wrap; /* Ensures buttons wrap on small screens */
    }

    /* Streamlit Button Styling */
    div.stButton > button {
        align-items: center;
        appearance: none;
        background-color: #fff;
        border-radius: 24px;
        border-style: none;
        box-shadow: rgba(0, 0, 0, .2) 0 3px 5px -1px, rgba(0, 0, 0, .14) 0 6px 10px 0, rgba(0, 0, 0, .12) 0 1px 18px 0;
        box-sizing: border-box;
        color: #3c4043;
        cursor: pointer;
        display: inline-flex;
        fill: currentcolor;
        font-family: "Google Sans", Roboto, Arial, sans-serif;
        font-size: 16px;
        font-weight: 500;
        height: 50px;
        justify-content: center;
        letter-spacing: .25px;
        line-height: normal;
        max-width: 100%;
        overflow: hidden;
        padding: 10px 30px;
        position: relative;
        text-align: center;
        text-transform: none;
        transition: all 0.3s ease-in-out;
        user-select: none;
        width: auto;
        min-width: 120px;
    }

    div.stButton > button:hover {
        background: #F6F9FE;
        color: #174ea6;
    }

    div.stButton > button:active {
        box-shadow: 0 4px 4px 0 rgb(60 64 67 / 30%), 0 8px 12px 6px rgb(60 64 67 / 15%);
        outline: none;
    }

    div.stButton > button:focus {
        outline: none;
        border: 2px solid #4285f4;
    }

    /* Media Query for Smaller Screens */
    @media screen and (max-width: 768px) {
        .question-title {
            font-size: 1.2em; /* Reduce font size for small screens */
        }

        .button-container {
            flex-direction: column; /* Stack buttons vertically on small screens */
        }

        div.stButton > button {
            width: 100%; /* Make buttons full width on mobile */
            min-width: auto;
        }
    }
</style>
    """
    return style

def image_container_styling():
    style="""
    <style>
    /* Image Container */
    .st-key-image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }

    /* Image Styling */
    .st-key-image-container img {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 100%;
        height: auto;
    } 
    </style> """

    return style