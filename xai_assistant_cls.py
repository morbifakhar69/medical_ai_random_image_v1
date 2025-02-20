import openai
import base64

import requests

from config import OPENAI_API_KEY
from icecream import ic
import time
import json
from typing import List, Dict
import sys
from model_interface import predict, explain

class XAIAssistant:
    def __init__(self, assistant_id=None):
        '''
        Initializes the XAIAssistant object. If an assistant_id is provided, the assistant with that id is retrieved. Otherwise, a new assistant is created.
        '''
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        #self.img_ids = self._create_img_ids()
        self.thread = None
        self.messages = []

        if assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
        else:
            with open("instructions.txt", "r", encoding="utf-8") as f:
                instructions = f.read()
            self.assistant = self.client.beta.assistants.create(
                instructions=instructions,
                model="gpt-4o-mini",
                tools=[
                    # Add your tools or other configurations here
                ]
            )

    def initialize_assistant(self, image_path):
        # Encode the image to base64
        base64_image = self.encode_image(image_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        # This payload sends the image to the assistant but does not ask a direct question
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please consider this image for our ongoing conversation. Answer the user whats in the image and describe aspects like skin color..."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Store the assistant's response or any other relevant information as needed
        return response.json()

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def process_survey_data(self, survey_data):
        survey_summary = f"The user has the following characteristics based on the survey responses: "
        for key, value in survey_data.items():
            if key not in ['name', 'age']:
                survey_summary += f"\n- {key}: {value}"
        return survey_summary

    def initialize_thread(self):
        if self.thread is None:
            self.thread = self.client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Initializing conversation thread."}
                        ]
                    }
                ]
            )

    def frame_with_survey_data(self, survey_data):
        self.initialize_thread()
        name = survey_data.get("name", "User")
        age = survey_data.get("age", "unknown age")
        survey_summary = self.process_survey_data(survey_data)
        initial_message = f"The user's name is {name}, they are {age} years old. Here are their characteristics based on the survey:\n{survey_summary}"#erweitere berücksichtige bei folgender Kommunikation
        self._create_message("user", initial_message)

    def chat(self, msg):
        if self.thread is None or self.thread.id is None:
            raise ValueError("Conversation thread is not initialized properly.")
        message = self._create_message("user", msg)
        run = self._create_run()
        while not run.status == 'completed':
            if run.status == 'requires_action':
                tool_outputs = self.get_tool_outputs(run)
                if tool_outputs:
                    try:
                        run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                            thread_id=self.thread.id,
                            run_id=run.id,
                            tool_outputs=tool_outputs
                        )
                        print("Tool outputs submitted successfully.")
                    except Exception as e:
                        print("Failed to submit tool outputs:", e)
                else:
                    print("No tool outputs to submit.")
            else:
                time.sleep(1)
                print(run.status)
        return self._handle_run_completed(run)

    def _create_message(self, role, content):
        return self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=content
        )

    def _create_run(self):
        return self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

    def _handle_run_completed(self, run):
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        msgs = self.extract_messages(messages)
        self.messages.append({"role": "assistant", "content": messages.data[0].content[0].text.value})
        return messages.data[0].content[0].text.value

    def extract_messages(self, messages: List) -> List[Dict[str, str]]:
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
        cleaned_text = text.replace("\\(", "").replace("\\)", "")
        return cleaned_text