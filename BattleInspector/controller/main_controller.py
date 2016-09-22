# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-27 23:08

# from PyQt4 import QtGui
from PyQt4 import QtCore
from model import model_global_list
import util
import time

# -------------------------------------------------------------------------------------------------------------------- #
# 控制层 --- 对用户命令采取不同的操作
# -------------------------------------------------------------------------------------------------------------------- #


class MainController(object):

	def __init__(self, model):
		self.model = model
		self.last_refresh_time = 0
		self.timer_thread = ReadDataThread(model)
		self.timer_thread.trigger.connect(self.timer_tab)
		self.refresh_thread = ReadDataThread(model)
		self.refresh_thread.trigger.connect(self.refresh_tab)

	# widget event functions
	def clear_high_lighted(self):
		ui_tab = self.model.table_model.get_ui_tab()
		if len(ui_tab) > 0:
			self.model.table_model.init_ui_flag(ui_tab)
		# 清空表格修改提交变量
		self.model.table_model.clear_tab_coord()

	def clear_list_view(self):
		self.model.list_model.clear_search_titles()
		# 清空列的add_titles 并且计数还原
		self.model.table_model.clear_add_titles()
		model_global_list.g_add_column_times = 1

	def change_search_update(self, text):
		# LineEdit
		self.model.search_update = text

		if len(text) > model_global_list.g_search_min_length:
			# 搜索结果
			if len(text) > model_global_list.g_search_min_length:
				# name_set 行标题的匹配集合,列标题的匹配集合,数据下标的匹配集合
				search_titles = self.model.table_model.input_search_result(text)
				# 行列索引的初始化
				self.model.table_model.tab_init_index()

				# 搜索行，自动过滤行
				if model_global_list.g_row_search_flag == model_global_list.g_input_flag:
					# 清空高亮标记
					self.clear_high_lighted()
					# 保存搜索的结果
					self.model.list_model.set_search_titles(search_titles)
					if search_titles is not None and search_titles != []:
						# 所有行数据 并过滤行
						self.model.table_model.row_mapping_interface(search_titles)

				elif model_global_list.g_column_search_flag == model_global_list.g_input_flag:
					# 清空高亮标记
					self.clear_high_lighted()

					self.model.list_model.set_search_titles(search_titles)
				elif model_global_list.g_table_search_flag == model_global_list.g_input_flag:
					# 清空list_view
					self.clear_list_view()

					high_lighted_coord = search_titles
					self.model.table_model.search_tab_data(high_lighted_coord)

	def change_show_table(self, state):

		# checkBox_show_table
		self.model.table_model.show_table = state

		ui_tab = self.model.table_model.get_point_tab()
		self.model.table_model.set_ui_tab(ui_tab)
		# 重置
		# 高亮标记 #索引 #行列标题
		self.clear_high_lighted()

		# 清空list_view
		self.clear_list_view()

	def change_submit_table(self):
		# pushButton_submit_table  提交对表格的修改
		# 修改表格的坐标集(x == 0 , y == 0 都不进行修改)
		update_tab_coord = self.model.table_model.get_tab_coord()
		if len(update_tab_coord) > 0:
			# 修改表格point_tab
			self.model.table_model.submit_point_tab(update_tab_coord)
			# 修改表格seq_tabs
			point_tab = self.model.table_model.get_point_tab()
			slider_order = self.model.table_model.get_slider_order()
			self.model.table_model.set_seq_tabs(point_tab, slider_order)
			# 写入本地文件
			# seq_tabs = self.model.table_model.get_seq_tabs()
			# self.model.table_model.write_tabs_interface(seq_tabs, slider_order)
			# 写入服务端
			xy_items_value = self.model.table_model.collect_update_data(update_tab_coord)
			self.model.table_model.update_entity_tab(xy_items_value)

		# 清空高亮标记
		self.clear_high_lighted()

	def change_refresh_tab(self):
		# push_button refresh tab
		# 清空高亮标记
		self.clear_high_lighted()
		self.refresh_thread.start()

	def refresh_tab(self, update_point_tab):
		self.model.table_model.set_ui_tab(update_point_tab)
		model_global_list.pop_exception("Congratulations, update the table successfully!")
		self.refresh_thread.quit()

	def change_tab_differ(self):
		# 提取begin和end表格差异信息
		# 消除高亮
		self.clear_high_lighted()

		# 获取begin table映射数据
		ui_tab_begin = self.model.table_model.slider_map_data(self.model.slider_begin)
		# 获取end table映射数据
		ui_tab_end = self.model.table_model.slider_map_data(self.model.slider_end)
		# 提取表格差异
		ui_tab_differ = self.model.table_model.slider_tab_differ(ui_tab_begin, ui_tab_end, model_global_list.g_table_differ_one)
		self.model.table_model.set_ui_tab(ui_tab_differ)

	# def change_slider_begin(self, value,  max_value):
	def change_slider_begin(self, slider_order):
		# ui.horizontalSlider_begin

		# 初始化，清空表格修改提交变量
		self.clear_high_lighted()

		if slider_order <= model_global_list.g_slider_index:
			self.model.table_model.set_slider_order(slider_order)
			# 记录时间标记
			self.model.slider_begin = slider_order
			time_point_tab = self.model.table_model.get_point_tab(slider_order)
			# 保存
			self.model.table_model.set_point_tab(time_point_tab)
			# 映射tab数据
			ui_tab = self.model.table_model.slider_map_data()
			self.model.table_model.set_ui_tab(ui_tab)

	# def change_slider_end(self, value,  max_value):
	def change_slider_end(self, slider_order):
		# ui.horizontalSlider_end

		# 初始化，清空表格修改提交变量
		self.clear_high_lighted()

		if slider_order <= model_global_list.g_slider_index:
			self.model.table_model.set_slider_order(slider_order)
			# 记录时间标记
			self.model.slider_end = slider_order
			time_point_tab = self.model.table_model.get_point_tab(slider_order)
			# 保存修改
			self.model.table_model.set_point_tab(time_point_tab)
			# 映射tab数据
			ui_tab = self.model.table_model.slider_map_data()
			self.model.table_model.set_ui_tab(ui_tab)

	def change_search_item_add(self, item_index):
		# listView_searched_item_name
		# 清空高亮标记
		self.clear_high_lighted()
		# 搜索列标题，点击后，添加自定列
		if model_global_list.g_input_flag == model_global_list.g_column_search_flag:
			# 列标题自动添加第一列
			# 从files_table去映射对应的列
			# 把映射的列添加到ui_table
			# 记录添加次数加一
			search_col = self.model.list_model.get_search_titles()
			self.model.table_model.add_col_data(search_col[item_index.row()])   # 点击添加的子行标题
			self.model.table_model.update_col_index()

	def change_on_timer(self):
		# 定时器的效果
		if model_global_list.g_refresh_flag and time.time() - self.last_refresh_time > 5:
			# 是否断开连接
			if self.model.table_model.test_connect():
				model_global_list.g_connect_flag = True
			else:
				model_global_list.g_connect_flag = False
			self.timer_thread.start()

		else:
			self.last_refresh_time = time.time()
		return model_global_list.g_slider_index

	def timer_tab(self, refresh_point_tab):

		# 没有断开连接并且能读取到读取数据
		if model_global_list.g_connect_flag and len(refresh_point_tab) > 0:
			# 修改时间轴,保存数据
			util.slider_add_one()
			self.model.table_model.set_slider_order(model_global_list.g_slider_index)

			# 时间轴的迁移和数据的映射
			if model_global_list.g_slider_index < model_global_list.g_slider_max:
				self.model.table_model.set_seq_tabs(refresh_point_tab, model_global_list.g_slider_index)
			else:
				# self.model.table_model.removal_seq_tabs()
				self.model.table_model.excel_list(self.model.table_model.get_seq_tabs())

				# 回到时间起点
				model_global_list.g_slider_index = 0
				self.model.table_model.set_seq_tabs(refresh_point_tab, model_global_list.g_slider_index)

			self.change_slider_begin(model_global_list.g_slider_index)

		self.timer_thread.quit()


class ReadDataThread(QtCore.QThread):
	# 进程类,rpyc读取数据的进程
	trigger = QtCore.pyqtSignal(dict)  # 初始化数据类型

	def __init__(self, model):
		super(ReadDataThread, self).__init__()
		self.model = model

	def run(self):
		# rpyc 访问
		begin_time = time.time()
		# global refresh_point_tab
		update_point_tab = self.model.table_model.update_entity()
		end_time = time.time()
		print "rpyc time length : " + str(end_time - begin_time)
		self.trigger.emit(update_point_tab)  # 传递信号，并传递数据
