import json

from pandas.core.frame import DataFrame

from excelgpt.cmd.cmd import Command
from excelgpt.cmd.excel import ExcelOpt
from excelgpt.config.config import Config
from excelgpt.llm.chatgpt import ChatGpt
from excelgpt.prompt.prompt import Prompt
from excelgpt.scheduler import dag
from excelgpt.util.log import logger

cfg = Config()


def main():
    prompt: Prompt = Prompt()
    excel: ExcelOpt = ExcelOpt()
    excel.open()
    worksheet: str = "学生清单"
    head: DataFrame = excel.head().get(worksheet)

    synopsis: dict[str, str] = dict()
    synopsis["task"] = "获取所有的课程编号"
    synopsis["worksheets"] = {worksheet: head}

    messages = [
        {
            "role": "system",
            "content": "As an AI, your current role is as a task decomposer, and your responsibility is to decompose a task given by a user into multiple executable small actions"
        },
        {
            "role": "user",
            "content": prompt.render(synopsis)
        },
    ]

    print(prompt.render(synopsis))
    gpt: ChatGpt = ChatGpt()
    gpt_res: str = gpt.say(messages)

    json_res = json.loads(gpt_res)

    actions_map: dict = {}
    actions_dep: dict = {}
    for entry in json_res:
        actions_dep[entry["id"]] = entry["dep"]
        actions_map[entry["id"]] = entry


if __name__ == '__main__':
    main()
