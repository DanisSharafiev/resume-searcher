from config.config import LLMConfig
from config.prompts import LLMPrompts
import requests

class LLMModel:
    def __init__(self):
        self.connection_string = LLMConfig.get_connection_string()
    
    def get_response(self, request_text):
        request = requests.post(
            f"{self.connection_string}/generate",
            json={
                "query": LLMPrompts.response_prompt + request_text
            }
        )
        return {
            "prompt": LLMPrompts.response_prompt + request_text,
            "data": request.json()
        }
    