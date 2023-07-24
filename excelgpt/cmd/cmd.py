from abc import ABC

from pandas.core.frame import DataFrame

from excelgpt.cmd.excel import ExcelOpt
from excelgpt.util.log import logger


class Command(ABC):
    def __init__(self):
        self.excel = ExcelOpt()
        self.res_map = {}
        self.prefix = "<resource>-"
        self.res = None

    def exec(self, id: int, command_name: str, args: dict):
        if command_name == "open":
            self.excel.open()
        elif command_name == "set_cell":
            row = args["row"]
            col = args["col"]
            value = args["value"]
            if str(args["value"]).startswith(self.prefix):
                if isinstance(self.res_map[value], list):
                    value = self.res_map[value][0][0].value
                elif isinstance(self.res_map[value], int):
                    value = self.res_map[value]
            self.excel.set_cell(worksheet=args["worksheet"], row=row, col=col, value=value)
        elif command_name == "get_cell":
            self.excel.get_cell(worksheet=args["worksheet"], row=args["row"], col=args["col"])
        elif command_name == "get_row":
            row = args["row"]
            if isinstance(row, str) and row.startswith(self.prefix):
                row = self.res_map[args["row"]]
            res = self.excel.get_row(worksheet=args["worksheet"], row=row)
            self.res_map[self.prefix + str(id)] = res
        elif command_name == "get_col":
            self.excel.get_col(worksheet=args["worksheet"], col=args["col"])
        elif command_name == "get_col_sum":
            self.res = self.excel.get_col_sum(worksheet=args["worksheet"], col=args["col"])
            self.res.columns = ["sum"]
        elif command_name == "set_col":
            self.excel.set_cell(worksheet=args["worksheet"], row=args["row"], col=args["col"], value=args["value"])
        elif command_name == "set_col_suffix":
            self.excel.set_col_suffix(worksheet=args["worksheet"], col=args["col"], value=args["value"])
        elif command_name == "set_col_prefix":
            self.excel.set_col_prefix(worksheet=args["worksheet"], col=args["col"], value=args["value"])
        elif command_name == "get_shape":
            self.excel.get_shape(worksheet=args["worksheet"])
        elif command_name == "save":
            self.excel.save()
        else:
            logger.error("Not found command: %s" % command_name)

    def get(self, worksheet: str) -> DataFrame:
        if self.res is None:
            return self.excel.worksheets().get(worksheet)
        return self.res
