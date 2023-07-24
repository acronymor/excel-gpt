import sys
from os.path import dirname, abspath

import streamlit as st
from pandas.core.frame import DataFrame
from st_aggrid import AgGrid
from st_aggrid.shared import ColumnsAutoSizeMode

path: str = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)

from excelgpt.cmd.excel import ExcelOpt
from excelgpt.api import core

st.title("Excel-GPT")

excel = ExcelOpt()
excel.open()
all_worksheet: dict[str, DataFrame] = excel.worksheets()
worksheets = list(all_worksheet.keys())

col1, col2 = st.columns([1, 3])
with col1:
    worksheet = st.selectbox('select worksheet', worksheets)

with col2:
    task = st.text_input('please input task')

tabs = [tab for tab in st.tabs(worksheets)]
for i in range(len(worksheets)):
    with tabs[i]:
        AgGrid(all_worksheet[worksheets[i]], height=300, width='100%',
               min_column_width=100,
               fit_columns_on_grid_load=True,
               scrollbarWidth=8,
               columns_auto_size_mode=ColumnsAutoSizeMode.NO_AUTOSIZE)

if len(task) != 0:
    res = core.go(worksheet, task)
    print(res)
    tab = st.tabs(["Result"])
    AgGrid(res, height=300, width='100%',
           fit_columns_on_grid_load=True,
           scrollbarWidth=8,
           columns_auto_size_mode=ColumnsAutoSizeMode.NO_AUTOSIZE)
