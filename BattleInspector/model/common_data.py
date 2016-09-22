# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-27 23:08
from logger import LOGGER
# -------------------------------------------------------------------------------------------------------------------- #
# 共享数据存储模块
# self.time_seq_tabs --- 所有时间点构成的表格的集合
# self.time_point_tab --- 具体一个时间点的表格数据
# self._row_search_index --- 表格映射的行索引（time_point_tab 而言）
# self._col_search_index --- 表格映射的列索引（time_point_tab 而言）
# self._slider_order = None --- 时间轴的标记
# self._search_titles = None --- 搜索标题的结果 和 数据的结果
# self.get_seq_tabs self.set_seq_tabs --- 取存时间序列表格数据的修改
# self.get_point_tab self.set_point_tab --- 取存时间点的表格数据
# self.update_point_tab --- slider改变更新时间点的表格数据
# -------------------------------------------------------------------------------------------------------------------- #


class CommonData(object):
	__instance = None

	def __init__(self):

		self._time_seq_tabs = {}
		self._time_point_tab = {}
		self._slider_order = None
		self._search_titles = []
		self._row_search_index = []   # 添加行索引
		self._col_search_index = []   # 添加列索引
		self._ui_tab = {}
		self._ui_flag = {}
		self._row_titles = None
		self._col_titles = None

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = super(CommonData, cls).__new__(cls, *args, **kwargs)
		return cls.__instance
	# =====================================================#
	# 属性的存取
	# =====================================================#

	def get_seq_tabs(self):
		return self._time_seq_tabs

	def get_point_tab(self, slider_order=None):
		if slider_order is None:
			return self._time_point_tab
		else:
			return self._time_seq_tabs[slider_order]

	def set_seq_tabs(self, time_seq_tabs, slider_order=None):
		# 直接修改seq_tabs, 修改set_seq_tabs的一个table
		if slider_order is None:
			self._time_seq_tabs = time_seq_tabs
		else:
			point_tab = time_seq_tabs
			self._time_seq_tabs[slider_order] = point_tab

	def set_point_tab(self, time_point_tab):
		self._time_point_tab = time_point_tab

	def get_slider_order(self):
		return self._slider_order

	def set_slider_order(self, val):
		self._slider_order = val

	def get_row_search_index(self):
		return self._row_search_index

	def set_row_search_index(self, row_index):
		self._row_search_index = row_index

	def get_col_search_index(self):
		return self._col_search_index

	def set_col_search_index(self, col_search_index):
		self._col_search_index = col_search_index

	def get_search_titles(self):
		return self._search_titles

	def set_search_titles(self, search_titles):
		self._search_titles = search_titles

	def clear_search_titles(self):
		self._search_titles = []

	def get_ui_tab(self):
		return self._ui_tab

	def set_ui_tab(self, ui_tab):
		self._ui_tab = ui_tab

	def get_ui_cell(self, row, col):
		return self._ui_tab[row][col]

	def set_ui_cell(self, row, col, val):
		self._ui_tab[row][col] = val

	def get_ui_flag(self):
		return self._ui_flag

	def set_ui_flag(self, ui_flag):
		self._ui_flag = ui_flag

	def get_ui_cell_flag(self, row, col):
		try:
			return bool(self._ui_flag[row][col])
		except:
			LOGGER.war("get_ui_cell_flag, cannot give the correct bool type to ui_cell_flag!")

	def set_ui_cell_flag(self, row, col, val):
		self._ui_flag[row][col] = val

	def get_row_titles(self, time_point_tab=None):
		# 获取行标题
		if time_point_tab is None:
			time_point_tab = self.get_point_tab()
		row_titles = []
		if time_point_tab != {}:
			for row_index in xrange(len(time_point_tab)):
				row_titles.append(time_point_tab[row_index][0])
		return row_titles

	def set_row_titles(self, row_titles):
		self._row_titles = row_titles

	def get_col_titles(self, time_point_tab=None):
		# 获取列标题
		if time_point_tab is None:
			time_point_tab = self.get_point_tab()
		col_titles = []
		if time_point_tab != {}:
			for column_index in xrange(len(time_point_tab[0])):
				col_titles.append(time_point_tab[0][column_index])
		return col_titles

	def set_col_titles(self, col_titles):
		self._col_titles = col_titles

	def removal_seq_tabs(self):
		for index_i in xrange(len(self.get_seq_tabs())):
			if index_i > 0:
				self._time_seq_tabs[index_i - 1] = self._time_seq_tabs[index_i]
