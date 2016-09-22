# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-27 23:08
from PyQt4 import QtCore
from common_data import CommonData
# -------------------------------------------------------------------------------------------------------------------- #
# 模型层 --- 重写QtCore.QAbstractListModel
# -------------------------------------------------------------------------------------------------------------------- #


class ListModel(QtCore.QAbstractListModel):
	def __init__(self):
		QtCore.QAbstractListModel.__init__(self)
		com_data = CommonData()
		self.get_search_titles = com_data.get_search_titles
		self.set_search_titles = com_data.set_search_titles
		self.clear_search_titles = com_data.clear_search_titles

	# Only-read
	def rowCount(self, model_index=QtCore.QModelIndex()):
		search_titles = self.get_search_titles()
		return len(search_titles)

	def data(self, index, role):
		if not index.isValid() or \
			not 0 <= index.row() < self.rowCount():
			return QtCore.QVariant()
		row = index.row()
		# 只允许显示
		if role == QtCore.Qt.DisplayRole:
			search_titles = self.get_search_titles()
			return QtCore.QVariant(search_titles[row])

	# def flags(self, index):
	# 	flag = super(ListModel, self).flags(index)
	# 	return flag | QtCore.Qt.ItemIsEditable

	# def setData(self, index, value, role = QtCore.Qt.EditRole):
	# 	if role == QtCore.Qt.EditRole:
	#
	# 		row = index.row()
	# 		list_view_data = QtGui.QColor(value)
	#
	# 		if list_view_data.isValid():
	# 			self._list_view_data[row] = list_view_data
	# 			self.dataChanged.emit(index, index)
	# 			return True
	# 	return False
