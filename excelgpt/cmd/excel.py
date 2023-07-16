import pandas
from pandas.core.frame import DataFrame


class ExcelOpt:
    def __init__(self, filename: str):
        self.xls = pandas.ExcelFile(filename)
        self.worksheet: dict[str, DataFrame] = {}

    def open(self) -> None:
        for sheet_name in self.xls.sheet_names:
            self.worksheet[sheet_name]: DataFrame = self.xls.parse(sheet_name)

    def get_shape(self, worksheet: str) -> tuple(int, int):
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