# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-27 23:08
from PyQt4 import QtCore
from PyQt4 import QtGui
from core_data_model import CoreDataModel
from model import model_global_list
from logger import LOGGER
import util
import time

# -------------------------------------------------------------------------------------------------------------------- #
# 模型层 --- 重写QAbstractTableModel
# -------------------------------------------------------------------------------------------------------------------- #


class TableModel(QtCore.QAbstractTableModel):
	def __init__(self):
		QtCore.QAbstractTableModel.__init__(self)
		self._update_tab_coord = []
		self.entity_lighted_thread = EntityLightedThread(self)
		self.entity_lighted_thread.trigger.connect(self.close_entity_lighted)

		core_data_model = CoreDataModel()

		self.core_data_model = core_data_model
		# rpyc 连接状态
		self.get_conn_error = core_data_model.get_conn_error
		self.test_connect = core_data_model.test_connect

		self.identify_entity = core_data_model.identify_entity

		# rpyc数据的存取
		self.write_tabs_interface = core_data_model.write_tabs_interface
		self.get_seq_tabs = core_data_model.get_seq_tabs
		self.set_seq_tabs = core_data_model.set_seq_tabs
		self.get_point_tab = core_data_model.get_point_tab
		self.set_point_tab = core_data_model.set_point_tab
		self.get_ui_tab = core_data_model.get_ui_tab
		self.set_ui_tab = core_data_model.set_ui_tab
		self.get_slider_order = core_data_model.get_slider_order
		self.set_slider_order = core_data_model.set_slider_order
		self.removal_seq_tabs = core_data_model.removal_seq_tabs

		self.input_search_result = core_data_model.input_search_result
		self.excel_list = core_data_model.excel_list

		# tab_cell
		self.get_ui_cell = core_data_model.get_ui_cell
		self.set_ui_cell = core_data_model.set_ui_cell
		# self.get_ui_flag = core_data_model.get_ui_flag
		self.get_ui_cell_flag = core_data_model.get_ui_cell_flag
		self.set_ui_cell_flag = core_data_model.set_ui_cell_flag
		self.init_ui_flag = core_data_model.init_ui_flag

		# row_search
		self.row_mapping_interface = core_data_model.row_mapping_interface
		self.tab_init_index = core_data_model.tab_init_index

		# col_search
		self.add_col_data = core_data_model.add_col_data
		self.update_col_index = core_data_model.update_col_index
		self.clear_add_titles = core_data_model.clear_add_titles
		# table_search
		self.search_tab_data = core_data_model.search_tab_data
		# slider
		self.slider_map_data = core_data_model.slider_map_data
		self.slider_tab_differ = core_data_model.slider_tab_differ

		# table_update
		self.submit_point_tab = core_data_model.submit_point_tab
		self.collect_update_data = core_data_model.collect_update_data
		self.update_entity_tab = core_data_model.update_entity_tab

		# table_refresh
		self.update_entity = core_data_model.update_entity
		# self.update_entity_value = core_data_model.update_entity_value

	# 1.Read_Only
	def rowCount(self, modelIndex=QtCore.QModelIndex()):
		ui_tab = self.get_ui_tab()
		if len(ui_tab) > 0:
			return len(ui_tab)

	def columnCount(self, modelIndex=QtCore.QModelIndex()):
		ui_tab = self.get_ui_tab()
		if len(ui_tab) > 0:
			return len(ui_tab[0])

	def data(self, index, role=QtCore.Qt.DisplayRole):
		if not index.isValid():
				return QtCore.QVariant()

		row = index.row()
		column = index.column()
		data = ""
		try:
			data = self.get_ui_cell(row, column)
		except:
			LOGGER.error("data, cannot get_ui_cell :" + str(data))
		if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
			try:
				if data is None:
					return QtCore.QString("")
				else:
					return QtCore.QString(data)
			except:
				LOGGER.error("data, cannot decode the table_modle data :" + str(data))

		changed = self.get_ui_cell_flag(row, column)
		if role == QtCore.Qt.BackgroundColorRole and changed:
			return QtGui.QColor(QtCore.Qt.yellow)

	# 2.Edit_Table
	def flags(self, index):
		return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.BackgroundColorRole

	def setData(self, index, value, role=QtCore.Qt.EditRole | QtCore.Qt.BackgroundColorRole):
		# table data 修改 (x == 0 , y == 0 都不进行修改)
		if role == QtCore.Qt.EditRole:
			row = index.row()
			column = index.column()
			model_global_list.g_refresh_flag = False
			data = util.to_unicode(value.toString())
			# (x > 0 , y == 0 识别游戏中的物体)
			if data is not None and data != "" and row > 0 and column == 0:
				item_name = self.get_ui_cell(row, column)
				self.entity_lighted_thread.set_item_name(item_name)
				self.entity_lighted_thread.start()
				# self.identify_entity(item_name)

			# (x != 0 , y != 0 进行修改)
			elif data is not None and data != "" and row != 0 and column != 0:
				self.set_ui_cell(row, column, data)

				self.dataChanged.emit(index, index)
				if [row, column] not in self.get_tab_coord():
					self._update_tab_coord.append([row, column])
					self.set_ui_cell_flag(row, column, True)
				return True

		return False

	def close_entity_lighted(self):
		self.entity_lighted_thread.quit()
	# =====================================================#
	# 属性的存取
	# =====================================================#

	def get_tab_coord(self):
		return self._update_tab_coord

	def set_tab_coord(self, tab_coord):
		self._update_tab_coord = tab_coord

	def clear_tab_coord(self):
		self._update_tab_coord = []

	# =====================================================#
	# 新建进程
	# =====================================================#


class EntityLightedThread(QtCore.QThread):
	# 进程类,实体高亮数据的进程
	trigger = QtCore.pyqtSignal()  # 初始化数据类型

	def __init__(self, model):
		super(EntityLightedThread, self).__init__()
		self.table_model = model
		self.item_name = None

	def set_item_name(self, val):
		self.item_name = val

	def run(self):
		# rpyc 访问
		begin_time = time.time()
		# global refresh_point_tab
		self.table_model.identify_entity(self.item_name)
		end_time = time.time()
		print "high_lighted entity time length : " + str(end_time - begin_time)
		self.trigger.emit()  # 传递信号，并传递数据
# if __name__ == "__main__":
# 	#1
# 	table_model = TableModel()
# 	print table_model.get_ui_tab()
