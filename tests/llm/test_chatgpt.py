from unittest import TestCase

from excelgpt.llm.chatgpt import ChatGpt


class TestChatGpt(TestCase):

    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.gpt = ChatGpt()

    def test_say(self) -> None:
        messages = [
            {"role": "system", "content": "you are network tool"},
            {"role": "user", "content": "ping"},
        ]
        res = self.gpt.say(messages)
        assert len(res) != 0