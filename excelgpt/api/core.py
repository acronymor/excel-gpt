import json

from pandas.core.frame import DataFrame

from excelgpt.cmd.cmd import Command
from excelgpt.cmd.excel import ExcelOpt
from excelgpt.llm.chatgpt import ChatGpt
from excelgpt.prompt.prompt import Prompt
from excelgpt.scheduler import dag
from excelgpt.util.log import logger


def to_json(body: str) -> list[dict]:
    res: list[dict] = list()

    import re
    for line in body.splitlines():
        line = line.replace("'", "\"")
        match = re.search(r'\{.*\}', line)
        if match:
            res.append(json.loads(match.group()))

    return res


def go(worksheet: str, task: str) -> str:
    prompt: Prompt = Prompt()
    excel: ExcelOpt = ExcelOpt()
    excel.open()
    head: DataFrame = excel.head().get(worksheet)

    synopsis: dict[str, str] = dict()
    synopsis["task"] = task
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

    logger.debug(json.dumps(messages, ensure_ascii=False))

    gpt: ChatGpt = ChatGpt()
    gpt_res: str = gpt.say(messages)
    logger.debug(gpt_res)

    json_res = to_json(gpt_res)
    logger.debug(json.dumps(json_res, ensure_ascii=False))
    if len(json_res) == 0:
        logger.error("Error Gpt Response")
        return None

    actions_map: dict = {}
    actions_dep: dict = {}
    for entry in json_res:
        actions_dep[entry["id"]] = entry["dep"]
        actions_map[entry["id"]] = entry

    logger.info("dag: scheduling")
    actions_list = dag.to(actions_dep)

    logger.info("cmd: executing")
    cmd: Command = Command()

    for i in actions_list:
        if i == -1:
            continue

        if i not in actions_map:
            logger.error("Execute step %d not in actions_map" % i)
            continue
        func_name: str = actions_map[i]["action"]
        func_args: str = actions_map[i].get("args")
        logger.debug("Execute step {} -> {}({})".format(i, func_name, func_args))
        cmd.exec(id=i, command_name=func_name, args=func_args)

    return cmd.get(worksheet)
