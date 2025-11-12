import os
import io
import config
from config import *


class HuggingFaceClient:
    def __init__(self, token):
        self.token = token
        self.client = InferenceClient(token=self.token)

    def send_query(self, model, query):
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ],
        )
        return completion.choices[0].message.content

    def analyze_feedback(self, feedback_text):
        return self.send_query("openai/gpt-oss-120b", feedback_text)