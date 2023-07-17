from unittest import TestCase

from excelgpt.prompt.prompt import Prompt


class TestChatGpt(TestCase):

    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.stub: Prompt = Prompt()

    def test_render(self) -> None:
        data: str = """
```
| 课程编号 | 课程名称 | 课程学分 |
|:-------:|:-------:|:--------:|
| 1 | 数学 | 5 |
| 2 | 语文 | 2 |
```
"""
        synopsis: dict[str, str] = dict()
        synopsis["task"] = "This is a simple task"
        synopsis["worksheets"] = {"课程清单": data}

        prompt = self.stub.render(synopsis)
        assert len(prompt) != 0
