# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-27 23:08

# from PyQt4 import QtGui
from model.table_model import TableModel
from model.list_model import ListModel
# -------------------------------------------------------------------------------------------------------------------- #
# 模型层 --- MVC模型中的模型层，为控制层和视图层提供数据处理的模型
# -------------------------------------------------------------------------------------------------------------------- #


class Model(object):
	#  properties for value of Qt model contents #

	def __init__(self):
		# create Qt models for compatible widget types #
		self.table_model = TableModel()
		self.list_model = ListModel()
		# model variables
		self.search_toupdate_item = None
		self.show_table = None
		self.submit_table = None
		self.tab_differ = None
		self.slider_order = 0
		self.slider_begin = 0       # 初始化为0
		# self.slider_end = len(self.table_model.get_seq_tabs())-1      # 初始化为0
		self.slider_end = 0     # 初始化为0

		# UI界面的初始化
		self.table_model.core_data_model.init_setup()
