# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-27 23:08
from common_data import CommonData
import model_global_list
import util
from logger import LOGGER
# -------------------------------------------------------------------------------------------------------------------- #
# 表格映射模块 --- 表格数据索引和映射，应用于表格数据的行标题过滤和列标题自定制功能
# -------------------------------------------------------------------------------------------------------------------- #


class TabMapping:
	def __init__(self):

		self._add_col_titles = []

		com_data = CommonData()
		self.get_search_titles = com_data.get_search_titles
		self.set_search_titles = com_data.set_search_titles
		self.get_point_tab = com_data.get_point_tab
		self.set_point_tab = com_data.set_point_tab
		self.get_ui_tab = com_data.get_ui_tab
		self.set_ui_tab = com_data.set_ui_tab
		self.get_ui_cell = com_data.get_ui_cell
		self.set_ui_cell = com_data.set_ui_cell

		self.get_ui_flag = com_data.get_ui_flag
		self.set_ui_flag = com_data.set_ui_flag
		self.get_ui_cell_flag = com_data.get_ui_cell_flag
		self.set_ui_cell_flag = com_data.set_ui_cell_flag

		self.get_row_titles = com_data.get_row_titles
		self.set_row_titles = com_data.set_row_titles
		self.get_col_titles = com_data.get_col_titles
		self.set_col_titles = com_data.set_col_titles

		self.get_row_search_index = com_data.get_row_search_index
		self.set_row_search_index = com_data.set_row_search_index
		self.get_col_search_index = com_data.get_col_search_index
		self.set_col_search_index = com_data.set_col_search_index

	# =====================================================#
	# 属性的存取
	# =====================================================#

	def get_add_titles(self):
		return self._add_col_titles

	def set_add_titles(self, titles):
		self._add_col_titles = titles

	def clear_add_titles(self):
		self._add_col_titles = []
	# =====================================================#
	# 变量初始化
	# =====================================================#

	@staticmethod
	def init_dict(rows, cols, data=None):
		# 指定元素初始化扩展制定长宽的dict
		dict_init = {}
		for index_x in xrange(rows):
			dict_temp = {}
			for index_y in xrange(cols):
				dict_temp[index_y] = data
			if rows > 1:
				dict_init[index_x] = dict_temp
			elif rows == 1:
				dict_init = dict_temp
		return dict_init

	def _clear_dict(self, dict_data, data=None):
		# 指定数据格式清空数据
		return self.init_dict(len(dict_data), len(dict_data[0]), data)

	@staticmethod
	def init_list(rows, cols, data=None):
		# 指定元素初始化扩展制定长宽的list
		list_init = []
		for index_x in xrange(rows):
			list_temp = []
			for index_y in xrange(cols):
				list_temp.append(data)
			if rows > 1:
				list_init.append(list_temp)
			elif rows == 1:
				list_init = list_temp
		return list_init

	def _clear_list(self, list_data, data=None):
		# 指定数据格式清空数据
		return self.init_dict(len(list_data), len(list_data[0]), data)

	def init_ui_flag(self, ui_tab):
		try:
			ui_flag = self.init_dict(len(ui_tab), len(ui_tab[0]), False)
			self.set_ui_flag(ui_flag)
		except:
			LOGGER.war("init_ui_flag, cannot get the ui_tab for the ui_flag!")
	# =====================================================#
	# 行标题的映射数据
	# =====================================================#

	@staticmethod
	def init_row_index(time_point_tab):
		# 初始化行索引 1-00000
		row_name_index = []
		if time_point_tab != {}:
			for row_index in xrange(len(time_point_tab)):
				if row_index == 0:
					row_name_index.append(model_global_list.is_index_flag)
				else:
					row_name_index.append(model_global_list.not_index_flag)
		return row_name_index

	@staticmethod
	def init_col_index(time_point_tab):
		# 初始化列索引 1-00000
		col_name_index = []
		if time_point_tab != {}:
			for col_index in xrange(len(time_point_tab[0])):
				if col_index == 0:
					col_name_index.append(model_global_list.is_index_flag)
				else:
					col_name_index.append(model_global_list.not_index_flag)
		return col_name_index

	def tab_init_index(self, ui_tab=None, time_point_tab=None):
		# 表格对应初始化行和列的索引

		if ui_tab is None:
			ui_tab = self.get_ui_tab()
		if time_point_tab is None:
			time_point_tab = self.get_point_tab()
		row_name_set = self.get_row_titles(time_point_tab)
		ui_row_name_set = self.get_row_titles(ui_tab)
		# 初始化索引的长度
		row_name_index = self.init_row_index(time_point_tab)
		row_name_index = self.create_index(ui_row_name_set, row_name_set, row_name_index)

		col_name_set = self.get_col_titles(time_point_tab)
		ui_col_name_set = self.get_col_titles(ui_tab)
		# 初始化索引的长度
		col_name_index = self.init_col_index(time_point_tab)
		col_name_index = self.create_index(ui_col_name_set, col_name_set, col_name_index)

		self.set_row_search_index(row_name_index)
		self.set_col_search_index(col_name_index)
		# return row_name_index, col_name_index

	@staticmethod
	def create_index(ui_name_set, name_set, init_index):
		# 原标题集合与目标标题集合的索引映射的生成
		# 默认第一个映射为 model_global_list.is_index_flag标记
		search_index = init_index
		for index_i in xrange(len(ui_name_set)):
			# 默认一定为model_global_list.is_index_flag ()
			if index_i == 0:
				search_index[index_i] = model_global_list.is_index_flag
			else:
				if ui_name_set[index_i] in name_set:
					index = name_set.index(ui_name_set[index_i])
					search_index[index] = model_global_list.is_index_flag

		return search_index

	def _create_row_index(self, list_view_data, time_point_tab):
		# 检索标题,生成行索引
		row_name_set = self.get_row_titles(time_point_tab)
		# 初始化索引的长度
		row_name_index = self.init_row_index(time_point_tab)
		row_name_index = self.create_index(list_view_data, row_name_set, row_name_index)
		return row_name_index

	def _create_col_index(self, add_col_set, time_point_tab):
		# 检索标题,生成列索引
		col_name_set = self.get_col_titles(time_point_tab)
		# 初始化索引的长度
		col_name_index = self.init_col_index(time_point_tab)
		col_name_index = self.create_index(add_col_set, col_name_set, col_name_index)
		return col_name_index

	@staticmethod
	def index_flag_length(flag_set, index_pos=None):
		# 索引的有效长度 model_global_list.is_index_flag 的个数 或者 第index_pos个标记的下标
		length = 0
		for index in xrange(len(flag_set)):
			if flag_set[index] == model_global_list.is_index_flag:
				if index_pos is not None and length == index_pos:
					return index
				length += 1
		return length

	def _create_map_data(self, row_search_index, col_search_index, time_point_tab):
		# 由行列映射生成映射的tab数据
		# 初始化map数据
		row = self.index_flag_length(row_search_index)
		col = self.index_flag_length(col_search_index)
		map_data = self.init_dict(row, col)

		row_i = 0
		for index_x in xrange(len(time_point_tab)):
			col_j = 0
			if row_search_index[index_x] == model_global_list.is_index_flag:
				for index_y in xrange(len(time_point_tab[0])):
					if col_search_index[index_y] == model_global_list.is_index_flag:
						map_data[row_i][col_j] = time_point_tab[index_x][index_y]
						col_j += 1
						if col_j == col:
							row_i += 1

		return map_data

	def _create_row_mapping(self, list_view_data, time_point_tab):
		# 行标题的映射数据

		# 获取行的映射索引
		if time_point_tab[0][0] not in list_view_data:
			list_view_data.insert(0, time_point_tab[0][0])    # 插入首项日期
		# 修改
		row_search_index = self._create_row_index(list_view_data, time_point_tab)
		self.set_row_search_index(row_search_index)
		# 不变
		col_search_index = self.get_col_search_index()
		return self._create_map_data(row_search_index, col_search_index, time_point_tab)

	def row_mapping_interface(self, list_view_data):
		# 按行标题搜索，对应的索引结果

		time_point_tab = self.get_point_tab()
		ui_mapping_tab = self._create_row_mapping(list_view_data, time_point_tab)
		self.set_ui_tab(ui_mapping_tab)
	# =====================================================#
	# 列标题添加映射数据
	# =====================================================#
	# 添加自定制的列标题 (以point_tab,搜索列项的一个映射)

	def _map_col_data(self, add_col_titles, point_tab):
		if len(point_tab[0]) >= len(add_col_titles):
			# 首次添加-自动添加第一列 add_column_set is a list
			if model_global_list.g_add_column_times == model_global_list.g_add_column_first\
					and point_tab[0][0] not in add_col_titles:

				add_col_titles.insert(0, point_tab[0][0])
			# 初始化表格大小
			ui_copy_tab = self.init_dict(len(point_tab), len(add_col_titles))
			# 获取列标题
			col_titles = self.get_col_titles(point_tab)
			for index_i in xrange(len(ui_copy_tab)):
				for index_j in xrange(len(add_col_titles)):
					#
						if index_i == 0 and index_j == 0:
							ui_copy_tab[index_i][index_j] = point_tab[index_i][index_j]
						else:
							index_y = col_titles.index(add_col_titles[index_j])
							ui_copy_tab[index_i][index_j] = point_tab[index_i][index_y]
			return ui_copy_tab

	@staticmethod
	def check_existed(flag_item, data_item):
		# 判断是否重复添加
		if data_item == [] or data_item is None:
			return False

		for i in xrange(len(data_item)):
			if data_item[i] == flag_item:
				return True
		return False

	def add_col_data(self, col_name):
		# (添加列项数据进入的接口)
		# 自动添加第一列
		if not self.check_existed(col_name, self.get_add_titles()):
			self._add_col_titles.append(col_name)

			ui_copy_table_data = self._map_col_data(self.get_add_titles(), self.get_point_tab())
			self.set_ui_tab(ui_copy_table_data)
			# 记录次数
			model_global_list.g_add_column_times += 1
		else:
			model_global_list.pop_exception(model_global_list._fromUtf8("Don't to add the same item for many times!"))

	def update_col_index(self):
		ui_tab = self.get_ui_tab()
		# 获取列标题
		col_titles = self.get_col_titles(ui_tab)
		point_tab = self.get_point_tab()
		# 获取列索引
		col_search_index = self._create_col_index(col_titles, point_tab)
		self.set_col_search_index(col_search_index)

	# =====================================================#
	# 时间标记移动的映射数据
	# =====================================================#
	def slider_map_data(self, slider_order=None):
		# (slider移动时间轴标记,生成映射数据的接口)
		# ui_tab point_tab 建立行列映射
		self.tab_init_index()
		row_search_index = self.get_row_search_index()
		col_search_index = self.get_col_search_index()
		time_point_tab = self.get_point_tab(slider_order)

		return self._create_map_data(row_search_index, col_search_index, time_point_tab)

	def search_tab_data(self, search_coord):
		# tab搜索结果高亮
		# 初始化
		self.init_ui_flag(self.get_ui_tab())
		# 修改
		if search_coord is not None and search_coord != []:
			for index_x in xrange(len(search_coord)):
				self.set_ui_cell_flag(search_coord[index_x][0], search_coord[index_x][1], True)
	# =====================================================#
	# 表格数据修改的提交
	# =====================================================#

	def _coord_map_set(self, update_tab_coord):
		# ui_tab修改坐标集合映射回point_tab坐标集合
		map_tab_coord = self.init_list(len(update_tab_coord), len(update_tab_coord[0]))
		if len(update_tab_coord) == 1:
			map_tab_coord = [map_tab_coord]
		row_search_index = self.get_row_search_index()
		col_search_index = self.get_col_search_index()
		for index_x in xrange(len(update_tab_coord)):
			for index_y in xrange(len(update_tab_coord[0])):
				if 0 == index_y:
					new_x = self.index_flag_length(row_search_index, update_tab_coord[index_x][index_y])
					map_tab_coord[index_x][index_y] = new_x
				elif 1 == index_y:
					new_y = self.index_flag_length(col_search_index, update_tab_coord[index_x][index_y])
					map_tab_coord[index_x][index_y] = new_y
		return map_tab_coord

	@staticmethod
	def update_tab_data(update_tab_coord, ui_tab, map_tab_coord, point_tab):
		# 修改文件坐标集合的数据为更改后的数据
		for index_x in xrange(len(update_tab_coord)):
				point_tab[map_tab_coord[index_x][0]][map_tab_coord[index_x][1]] = \
					ui_tab[update_tab_coord[index_x][0]][update_tab_coord[index_x][1]]
		return point_tab

	def submit_point_tab(self, update_tab_coord):
		# (提交表格数据修改的接口)
		# 获取映射坐标
		ui_tab = self.get_ui_tab()
		point_tab = self.get_point_tab()
		map_tab_coord = self._coord_map_set(update_tab_coord)
		point_tab = self.update_tab_data(update_tab_coord, ui_tab, map_tab_coord, point_tab)
		# 写入point_tab
		self.set_point_tab(point_tab)

	@staticmethod
	def get_xy_items_value(update_tab_coord, ui_tab):
		# 返回修改cell的 [$1:行标题项, $2:列标题项, $3:修改值]
		# ui_修改值，删除QString编码为ascii
		xy_items_value = []
		for index_x in xrange(len(update_tab_coord)):
			row_index = update_tab_coord[index_x][0]
			col_index = update_tab_coord[index_x][1]
			xy_items_value.append([ui_tab[row_index][0], ui_tab[0][col_index], ui_tab[row_index][col_index]])
		return xy_items_value

	def collect_update_data(self, update_tab_coord):
		# 收集表格修改的数据， 返回修改cell的 [$1:行标题项, $2:列标题项, $3:修改值]
		ui_tab = self.get_ui_tab()
		return self.get_xy_items_value(update_tab_coord, ui_tab)

	@staticmethod
	def slider_tab_differ(ui_tab_begin, ui_tab_end, differ_flag=None):
		ui_tab_differ = {}
		for index_i in xrange(len(ui_tab_begin)):
			dict_temp = {}
			for index_j in xrange(len(ui_tab_begin[index_i])):
				if ui_tab_begin[index_i][index_j] == ui_tab_end[index_i][index_j]:
					dict_temp[index_j] = ui_tab_begin[index_i][index_j]
				else:
					if differ_flag == model_global_list.g_table_differ_one or differ_flag is None:
						dict_temp[index_j] = '(' + str(ui_tab_begin[index_i][index_j]) + ',' + str(ui_tab_end[index_i][index_j]) + ')'
					elif differ_flag == model_global_list.g_table_differ_two:
						dict_temp[index_j] = '(' + str(ui_tab_begin[index_i][index_j]) + '_' + str(ui_tab_end[index_i][index_j]) + ')'
			if len(ui_tab_begin) == 1:
				ui_tab_differ = dict_temp
			elif len(ui_tab_begin) > 1:
				ui_tab_differ[index_i] = dict_temp
		return ui_tab_differ
