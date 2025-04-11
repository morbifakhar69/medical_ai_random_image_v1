import openai
import time
import json
from typing import List, Dict
from config import OPENAI_API_KEY

class XAIAssistant:
    def __init__(self, assistant_id=None, image_path=None, survey_data=None):
        """
        Initializes the XAIAssistant object. If an assistant_id is provided, it retrieves the existing assistant.
        Otherwise, it creates a new assistant with predefined instructions.
        """
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.thread = None
        self.messages = []
        self.survey_data = survey_data if survey_data else {}

        if image_path:
            self.image_path = image_path
            self.image_file_id = self.upload_image(image_path)  #  Upload image and get file_id
        else:
            self.image_file_id = None

        if assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
        else:
            with open("instructions.txt", "r", encoding="utf-8") as f:
                instructions = f.read()

            self.assistant = self.client.beta.assistants.create(
                instructions=instructions,
                model="gpt-4o-mini",  
                tools=[]
            )

            self.initialize_thread_with_survey_and_image()

    def upload_image(self, image_path):
        """Uploads an image to OpenAI and returns the file ID."""
        with open(image_path, "rb") as image_file:
            response = self.client.files.create(
                file=image_file,
                purpose="vision"  #  Ensure the file is uploaded for vision tasks
            )
        return response.id  #  Returns file ID for later reference

    def process_survey_data(self):
        """Formats survey data as a readable string."""
        if not self.survey_data:
            return "No additional user survey data available."

        survey_summary = "The user has provided the following survey responses:\n"
        for key, value in self.survey_data.items():
            survey_summary += f"- {key}: {value}\n"

        name = self.survey_data.get("name", "User")
        age = self.survey_data.get("age", "unknown age")
        return f"The user's name is {name}, they are {age} years old.\n\n{survey_summary}"

    def initialize_thread_with_survey_and_image(self):
        """Initializes a conversation thread with survey data and an uploaded image file."""
        initial_message_content = [
            {
                "type": "text",
                "text": self.process_survey_data()
            }
        ]

        if self.image_file_id:
            initial_message_content.append({
                "type": "image_file",
                "image_file": {
                    "file_id": self.image_file_id  # way to reference an uploaded file
                }
            })

        if self.thread is None:
            self.thread = self.client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": initial_message_content
                    }
                ]
            )

    def chat(self, msg):
        """Sends a message to the assistant using the Assistants API and retrieves the response."""
        if self.thread is None or self.thread.id is None:
            raise ValueError("Conversation thread is not initialized properly.")

        self._create_message("user", msg)
        run = self._create_run()

        while not run.status == 'completed':
            time.sleep(1)
            print(run.status)

        return self._handle_run_completed(run)

    def _create_message(self, role, content):
        """Sends a message using OpenAI's Assistants API."""
        return self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=[{"type": "text", "text": content}]
        )

    def _create_run(self):
        """Starts and polls the assistant's response process."""
        return self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

    def _handle_run_completed(self, run):
        """Handles the assistant's response after completing the conversation cycle."""
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        #self.messages.append({"role": "assistant", "content": messages.data[0].content[0].text.value})
        return messages.data[0].content[0].text.value

    def extract_messages(self, messages: List) -> List[Dict[str, str]]:
        """Extracts and cleans messages from the assistant's responses."""
        result = []
        for msg in messages:
            content_text = " ".join(block.text.value for block in msg.content if block.type == "text")
            cleaned_content = self.clean_latex_formatting(content_text)
            result.append({
                "role": msg.role,
                "content": cleaned_content
            })
        return result

    def clean_latex_formatting(self, text: str) -> str:
        """Removes LaTeX formatting from the text output."""
        return text.replace("\\(", "").replace("\\)", "")
