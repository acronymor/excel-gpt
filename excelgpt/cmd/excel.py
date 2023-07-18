import pandas
from pandas.core.frame import DataFrame

from excelgpt.config.config import Config


class ExcelOpt(object):
    def __init__(self):
        self.cfg = Config()
        self.xls = pandas.ExcelFile(self.cfg.file_path)
        self.worksheet: dict[str, DataFrame] = {}

    def open(self) -> None:
        for sheet_name in self.xls.sheet_names:
            self.worksheet[sheet_name]: DataFrame = self.xls.parse(sheet_name)

    def head(self, n: int = 2) -> dict[str, DataFrame]:
        res: dict[str, DataFrame] = dict()
        for sheet_name in self.xls.sheet_names:
            res[sheet_name] = self.worksheet[sheet_name].head(n)

        return res

    def get_shape(self, worksheet: str) -> tuple:
        return self.worksheet[worksheet].shape

    def get_cell(self, worksheet: str, row: list[str], col: list[str]) -> DataFrame:
        res = self.worksheet[worksheet].loc[row, col]
        return pandas.DataFrame(data=res)

    def get_row(self, worksheet: str, row: list[str]) -> DataFrame:
        res = self.worksheet[worksheet].loc[row]
        return pandas.DataFrame(data=res)

    def get_col(self, worksheet: str, col: list[str]) -> DataFrame:
        res = self.worksheet[worksheet].loc[:, col]
        return pandas.DataFrame(data=res)