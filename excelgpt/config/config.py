import os

from excelgpt.config.singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self) -> None:
        self.openai_key = os.environ.get("OPENAI_API_KEY", "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")
        self.openai_base = os.environ.get("OPENAI_API_BASE", "http://localhost:9000/v1")
        self.openai_chat_model = "gpt-3.5-turbo"
        self.openai_temperature = 1
        self.openai_timeout = 20

        self.file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "example.xlsx")