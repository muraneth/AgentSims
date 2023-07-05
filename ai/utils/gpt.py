import requests
from config import Config

class GPTCaller(object):
    def __init__(self, config: Config) -> None:
        self.config = config

    def call(self, system: str, user: str, model: str) -> str:
        url = f"http://{self.config.gpt_host}:{self.config.gpt_port}/api/{model}"
        response = requests.post(url, json={"system": system, "user": user}).json()
        return response
