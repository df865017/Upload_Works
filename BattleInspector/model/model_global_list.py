# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-21 23:08
from PyQt4 import QtGui
from PyQt4 import QtCore
# -------------------------------------------------------------------------------------------------------------------- #
# 全局模块 --- 提供全局函数和全局变量
# -------------------------------------------------------------------------------------------------------------------- #

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s


g_file_dir = "./data/"
g_file_type = ".xls"
# 读取第一张表
g_sheet_rw_index = 0
# 读取一行
g_row_index = 1
# 读取一列
g_column_index = 2
# 读取ui_tab
g_ui_table_flag = 1
# 读取point_tab
g_files_table_flag = 2
# table循环刷新变量
g_flush_times = 0
# 行标题搜索
g_row_search_flag = 1
g_row_search_prefix = "row_name"
# 列标题搜索
g_column_search_flag = 2
g_column_search_prefix = "column_name"
# 表格数据搜素
g_table_search_flag = 3
g_table_search_prefix = "table_data"
# 其他搜索
g_others_search_flag = 0
# len("row_name") is min
g_search_min_length = 8
# 搜索数据集分类标志
# 1 row_name_set
# 2 column_name_set
# 3 table_name_set
# 0 others_set
g_input_flag = 0

# 添加列元素的初始值
g_add_column_times = 1
g_add_column_first = 1

# 索引标志位
is_index_flag = 1
not_index_flag = 0

# table_differ 不同形式
g_table_differ_one = 1
g_table_differ_two = 2

# 全局函数
# 弹出各种异常的信息
g_slider_max = 100
g_slider_index = 0

# 表格刷新的开关
g_refresh_flag = True
# 连接状态刷新的开关
g_connect_flag = False
# 表格刷新的时间间隔
g_refresh_step = 5000


def pop_exception(str_exception):
	msg_box = QtGui.QMessageBox()
	msg_box.setText(str_exception)
	msg_box.exec_()
