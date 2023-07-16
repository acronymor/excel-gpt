from unittest import TestCase

from excelgpt.cmd.excel import ExcelOpt
from pandas.core.frame import DataFrame


class TestChatGpt(TestCase):
    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        file: str = "/home/li/Workspace/excel-gpt/files/example.xlsx"
        self.excel = ExcelOpt(file)

    def test_get(self):
        """
        | 课程编号 | 课程名称 | 课程学分 |
        |---|---|---|
        | 1 | math | 5 |
        | 2 | chinese | 2 |
        """
        self.excel.open()
        res1: DataFrame = self.excel.get_row("课程清单", [0, 1])
        shape = res1.shape
        assert 2 == shape[0]
        assert 3 == shape[1]

        res2 = self.excel.get_col("课程清单", ["课程编号"])
        shape = res2.shape
        assert 2 == shape[0]
        assert 1 == shape[1]

        res3 = self.excel.get_cell("课程清单", [0], ["课程编号"])
        shape = res3.shape
        assert 1 == shape[0]
        assert 1 == shape[1]
        assert 1 == res3.values[0][0]
