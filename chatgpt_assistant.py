from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


class ChatGPTAssistant:
    def __init__(self):
        pass

    def process_data(self, data):
        response = client.chat.completions.create(model="gpt-4-turbo",
        messages=[
            #{"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please return the following text exactly as it is: {data}"}])
        return response.choices[0].message.content.strip()

    def send_data(self, data):
        processed_data = self.process_data(data)
        print(f"Dies ist dir Rückgabe von ChatGPT: {processed_data}")
