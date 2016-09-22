# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-27 23:08
from common_data import CommonData
import model_global_list
import util
# -------------------------------------------------------------------------------------------------------------------- #
# 字符检索匹配模块 --- 对输入字符命名，匹配对应的操作和数据
# -------------------------------------------------------------------------------------------------------------------- #


class SearchResult:
	def __init__(self):

		com_data = CommonData()
		self.get_search_titles = com_data.get_search_titles
		self.set_search_titles = com_data.set_search_titles
		self.get_point_tab = com_data.get_point_tab
		self.set_point_seq = com_data.set_point_tab
		self.get_ui_tab = com_data.get_ui_tab
		self.set_ui_tab = com_data.set_ui_tab
		self.get_ui_cell = com_data.get_ui_cell
		self.set_ui_cell = com_data.set_ui_cell

		self.get_row_titles = com_data.get_row_titles
		self.set_row_titles = com_data.set_row_titles
		self.get_col_titles = com_data.get_col_titles
		self.set_col_titles = com_data.set_col_titles

	# =====================================================#
	# 字符串的子串检索
	# =====================================================#
	@staticmethod
	def get_input_substr(check_str, input_str):
		# LineEdit.text() 子串判定

		split_search_str = ""
		if check_str != "" and check_str in input_str and len(check_str) < input_str:
			#
			# n_pos = input_str.index(check_str)
			n_pos = util.str_match(check_str, input_str)
			# n_pos += len(check_str)
			index = n_pos
			for index in xrange(n_pos, len(input_str)):
				if util.to_unicode(" ") == input_str[index]:
					pass
				else:
					break
			split_search_str = input_str[index:]
			if split_search_str != "":
				return True, split_search_str
			return False, split_search_str
		else:
			return False, split_search_str

	def _sub_str_split(self, input_str):
		# LineEdit 子串分类和判断
			# 初始化
			#  0 = others
			#  1 = "row_name"
			#  2 = "column_name"
			#  3 = "table_data"
			# 初始化
			check_flag = False
			model_global_list.g_input_flag = model_global_list.g_others_search_flag
			split_search_str = ""
			# 分割搜索信息串
			# 1row_name
			check_flag, split_search_str = self.get_input_substr(model_global_list.g_row_search_prefix, input_str)
			if check_flag is True:
				model_global_list.g_input_flag = model_global_list.g_row_search_flag	  # row

			else:
				# 2column_name
				check_flag, split_search_str = self.get_input_substr(model_global_list.g_column_search_prefix, input_str)
				if check_flag is True:
					model_global_list.g_input_flag = model_global_list.g_column_search_flag    # column

				else:
					# 3table_name
					check_flag, split_search_str = self.get_input_substr(model_global_list.g_table_search_prefix, input_str)
					if check_flag is True:
						model_global_list.g_input_flag = model_global_list.g_table_search_flag   # table

					else:
						# 0
						model_global_list.g_input_flag = model_global_list.g_others_search_flag
			return split_search_str
	# =====================================================#
	# 搜索行列标题和表格数据搜索
	# =====================================================#

	def _get_search_titles(self):
		# 获取搜素的数据集,get_search_titles
		if model_global_list.g_input_flag == model_global_list.g_row_search_flag:
			# 直接从ui_table 检索行标题
			return self.get_row_titles(self.get_point_tab())
		elif model_global_list.g_input_flag == model_global_list.g_column_search_flag:
			# 直接从files_table 检索列标题
			return self.get_col_titles(self.get_point_tab())
		elif model_global_list.g_input_flag == model_global_list.g_table_search_flag:
			return self.get_point_tab()

	@staticmethod
	def match_sub_str(search_item, variable_name_set):
		# 子串实时检索匹配的字符

		if search_item is not None and search_item != "":
			# 初始化
			list_1 = variable_name_set  # row_name
			list_2 = []
			for letter_index in xrange(len(search_item)):
				list_1_copy = []
				list_2_copy = []
				for name_index in xrange(len(list_1)):
					letter_search_item = list_1[name_index]
					if letter_search_item[letter_index] == search_item[letter_index]:
						list_1_copy.append(list_1[name_index])
					else:
						list_2_copy.append(list_1[name_index])
				# 恢复数据list_1
				list_1 = list_1_copy
				list_2 = list_2 + list_2_copy
			return list_1, list_2

	@staticmethod
	def search_ui_tab(search_item, ui_tab):
		# 搜索匹配的表格数据

		search_tab_coord = []
		for index_x in xrange(len(ui_tab)):
			for index_y in xrange(len(ui_tab[index_x])):
				if search_item == ui_tab[index_x][index_y]:
					search_tab_coord.append([index_x, index_y])
		return search_tab_coord

	def input_search_result(self, input_str):
		# LineEdit输入关键字的行列标题搜索匹配结果

		list1 = []
		# 分割出查找的核心字符串 和 判断搜索分类标记
		split_str = self._sub_str_split(input_str)

		if split_str is not None and split_str != "":
			# 搜索结果
			name_set = self._get_search_titles()
			# row column name
			if model_global_list.g_input_flag == model_global_list.g_row_search_flag\
				or model_global_list.g_input_flag == model_global_list.g_column_search_flag:
				# model_global_list.g_lineEdit_flag = model_global_list.g_row_search_flag
				list1, list2 = self.match_sub_str(split_str, name_set)
				if list1 is []:
					return list1
			#  table_data 搜索下标的集合
			elif model_global_list.g_input_flag == model_global_list.g_table_search_flag:
				return self.search_ui_tab(split_str, self.get_ui_tab())

		return list1

# if __name__ == "__main__":
# 		search_result = SearchResult()
# 		test_dict = {0: 'column_name   1', 1: 'row_name ', 2: 'row_name row3', 3: 'column_name column4',\
# 4: 'table_data',5: 'table_data table6'}
#
# 		for index in xrange(len(test_dict)):
# 			print search_result._sub_str_split(test_dict[index])
