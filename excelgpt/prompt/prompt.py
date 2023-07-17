import os.path

from jinja2 import Template, DebugUndefined

from excelgpt.util.log import logger


class Prompt(object):
    def __init__(self):
        self.prompt: str = ""
        self.file: str = os.path.join(os.path.dirname(__file__), "prompt.txt")

    def render(self, synopsis: dict[str, str] = dict()) -> str:
        res: str = ""
        with open(self.file, "r", encoding="utf-8") as fp:
            tm = Template(fp.read(), undefined=DebugUndefined)
            res = tm.render(synopsis)

        if len(res) == 0:
            logger.error("Empty Prompt Format, Please check {}".format(self.file))

        return res
