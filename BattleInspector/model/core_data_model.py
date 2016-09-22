# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-21 23:08

from search_result import SearchResult
from tab_mapping import TabMapping
from data_collector import DataCollector
from logger import LOGGER
# -------------------------------------------------------------------------------------------------------------------- #
# 模型处理层
# self.time_seq_tabs --- 所有时间点构成的表格的集合
# self.time_point_tab --- 具体一个时间点的表格数据
# self.read_tabs_interface(self, slider_order=None) --- 读取文件夹下时间序列表格数据
# self.read_tabs_interface: slider_order is not None --- 读取time_seq_tabs 和 time_point_tab

# self.write_tabs_interface(self, time_seq_tabs,slider_order=None) --- 保存time_seq_tabs表格数据的修改
# self.write_tabs_interface: slider_order is not None --- 保存具体时间点的表格数据
#
# -------------------------------------------------------------------------------------------------------------------- #


class CoreDataModel(object):
	def __init__(self):
		# 属性变量

		# 变量的初始化
		data_collector = DataCollector()
		self.get_conn_error = data_collector.get_conn_error
		self.update_entity = data_collector.update_entity
		# self.update_entity_value = data_collector.update_entity_value
		self.update_entity_tab = data_collector.update_entity_tab
		self.excel_list = data_collector.excel_list
		self.test_connect = data_collector.test_connect

		self.identify_entity = data_collector.identify_entity

		self.get_seq_tabs = data_collector.get_seq_tabs
		self.set_seq_tabs = data_collector.set_seq_tabs
		self.get_point_tab = data_collector.get_point_tab
		self.set_point_tab = data_collector.set_point_tab
		self.get_slider_order = data_collector.get_slider_order
		self.set_slider_order = data_collector.set_slider_order
		self.read_tabs_interface = data_collector.read_tabs_interface
		self.write_tabs_interface = data_collector.write_tabs_interface
		self.removal_seq_tabs = data_collector.removal_seq_tabs

		search_res = SearchResult()
		self.get_search_titles = search_res.get_search_titles
		self.set_search_titles = search_res.set_search_titles
		self.get_row_titles = search_res.get_row_titles
		self.set_row_titles = search_res.set_row_titles
		self.get_ui_tab = search_res.get_ui_tab
		self.set_ui_tab = search_res.set_ui_tab
		self.get_ui_cell = search_res.get_ui_cell
		self.set_ui_cell = search_res.set_ui_cell
		self.input_search_result = search_res.input_search_result

		tab_mapping = TabMapping()
		# self.get_ui_flag = tab_mapping.get_ui_flag
		self.get_ui_cell_flag = tab_mapping.get_ui_cell_flag
		self.set_ui_cell_flag = tab_mapping.set_ui_cell_flag
		self.init_ui_flag = tab_mapping.init_ui_flag
		self.row_mapping_interface = tab_mapping.row_mapping_interface
		self.tab_init_index = tab_mapping.tab_init_index
		self.slider_map_data = tab_mapping.slider_map_data
		# 高亮显示搜索结果
		self.search_tab_data = tab_mapping.search_tab_data
		# 添加自定制的列标题
		self.add_col_data = tab_mapping.add_col_data
		self.update_col_index = tab_mapping.update_col_index
		self.clear_add_titles = tab_mapping.clear_add_titles
		# 表格修改提交
		self.submit_point_tab = tab_mapping.submit_point_tab
		self.collect_update_data = tab_mapping.collect_update_data

		# 表格的对比输出
		self.slider_tab_differ = tab_mapping.slider_tab_differ

	def init_setup(self):
		# 初始化时间轴标记
		# 日志的开始节点
		LOGGER.info("---start---")
		self.set_slider_order(0)
		self.read_tabs_interface(self.get_slider_order())
		# # 初始化ui表格数据
		# time_point_tab = self.get_point_tab()
		# if len(time_point_tab) > 0:
		# 	self.set_ui_tab(time_point_tab)
		# 	self.init_ui_flag(self.get_ui_tab())
		# 	# 初始化标题数据
		# 	row_titles = self.get_row_titles()
		# 	self.set_search_titles(row_titles)
		# 	# 初始化索引
		# 	self.tab_init_index(self.get_ui_tab(), self.get_point_tab())
		# else:
		# 	LOGGER.error("init_set_up, failed to init the gui, please check the rpyc connect!")
		if not self.get_conn_error():
			# 初始化ui表格数据
			time_point_tab = self.get_point_tab()
			self.set_ui_tab(time_point_tab)
			self.init_ui_flag(self.get_ui_tab())
			# 初始化标题数据
			row_titles = self.get_row_titles()
			self.set_search_titles(row_titles)
			# 初始化索引
			self.tab_init_index(self.get_ui_tab(), self.get_point_tab())
		else:
			LOGGER.error("init_set_up, failed to init the gui, please check the rpyc connect!")
	# =====================================================#
	# 属性的存取
	# =====================================================#

#
# if __name__ == "__main__":
# 	#1
# 	model = CoreDataModel()
# 	model.read_tabs_interface()
# 	time_seq_tabs = model.get_seq_tabs()
# 	time_seq_tabs[0][1][1] = "core_data_model"
# 	model.write_tabs_interface(time_seq_tabs)
