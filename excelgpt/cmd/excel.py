import pandas
from pandas.core.frame import DataFrame

from excelgpt.config.config import Config


class ExcelOpt(object):
    def __init__(self):
        self.cfg = Config()
        self.file = self.cfg.file_path
        self.xls = pandas.ExcelFile(self.file)
        self.worksheet: dict[str, DataFrame] = {}

    def worksheets(self) -> dict[str, DataFrame]:
        return self.worksheet

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

    def set_cell(self, worksheet: str, row: str, col: str, value: any) -> DataFrame:
        res = self.worksheet[worksheet].at[int(row), col] = value
        return res

    def set_col_suffix(self, worksheet: str, col: list[str], value: any) -> DataFrame:
        res = self.worksheet[worksheet][col].astype('str') + value
        self.worksheet[worksheet][col] = res
        return res

    def set_col_prefix(self, worksheet: str, col: list[str], value: any) -> DataFrame:
        res = value + self.worksheet[worksheet][col].astype('str')
        self.worksheet[worksheet][col] = res
        return res

    def get_row(self, worksheet: str, row: list[str]) -> DataFrame:
        res = self.worksheet[worksheet].loc[row]
        return pandas.DataFrame(data=res)

    def get_col(self, worksheet: str, col: list[str]) -> DataFrame:
        res = self.worksheet[worksheet].loc[:, col]
        return pandas.DataFrame(data=res)

    def get_col_sum(self, worksheet: str, col: list[str]) -> DataFrame:
        res = self.get_col(worksheet, col)
        return pandas.DataFrame(data=res.sum())

    def save(self):
        with pandas.ExcelWriter(self.file) as writer:
            for sheet_name in self.xls.sheet_names:
                self.worksheet[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
