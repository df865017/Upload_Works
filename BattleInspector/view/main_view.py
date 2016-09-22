# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-27 23:08

from PyQt4 import QtGui
from PyQt4 import QtCore
from battle_inspector import Ui_MainView
import util
from model import model_global_list
# -------------------------------------------------------------------------------------------------------------------- #
# 视图层 --- UI界面和操作信号函数
# -------------------------------------------------------------------------------------------------------------------- #


class MainView(QtGui.QMainWindow):  # , Ui_MainWindow
	#  properties for widget value #

	def __init__(self, model, main_ctrl):
		self.model = model
		self.main_ctrl = main_ctrl
		super(MainView, self).__init__()
		self.ui = Ui_MainView()
		self.ui.setupUi(self)
		self.build_ui()

	def build_ui(self):

		# 顺序不能反，先table_view 然后 list_view
		self.ui.tableView.setModel(self.model.table_model)
		self.ui.listView_searched_item_name.setModel(self.model.list_model)
		# 定时器 每1s刷新一次
		self.ui.timer = QtCore.QTimer()
		QtCore.QObject.connect(self.ui.timer, QtCore.SIGNAL("timeout()"), self.on_timer)
		self.ui.timer.start(model_global_list.g_refresh_step)

		#  connect widget signals to event functions #
		# lineEdit
		self.ui.lineEdit_search_toupdate_item.textEdited.connect(self.on_search_toupdate_item)
		# checkBox_show_table
		self.ui.checkBox_show_table.stateChanged.connect(self.on_show_table)
		# pushButton_tab_differ
		self.ui.pushButton_submit_table.clicked.connect(self.on_submit_table)
		self.ui.pushButton_tab_differ.clicked.connect(self.on_tab_differ)
		# slider_begin   slider_end
		self.ui.horizontalSlider_begin.valueChanged.connect(self.on_begin_point)
		self.ui.horizontalSlider_end.valueChanged.connect(self.on_end_point)
		# listView_searched_item_name
		self.ui.listView_searched_item_name.clicked.connect(self.on_searched_item_add)
		# pushButton_refresh
		self.ui.pushButton_refresh.clicked.connect(self.on_refresh_tab)

		# 连接成功与否的标记

		if not self.model.table_model.get_conn_error() or model_global_list.g_connect_flag is True:
			p = QtGui.QPalette()
			p.setColor(QtGui.QPalette.Foreground, QtGui.QColor(148, 0, 211))
			self.ui.connect_state.setPalette(p)
			self.ui.connect_state.setText(u'连接成功......')
		else:
			p = QtGui.QPalette()
			p.setColor(QtGui.QPalette.Foreground, QtGui.QColor(255, 0, 0))
			self.ui.connect_state.setPalette(p)
			self.ui.connect_state.setText(u'连接失败，请重新连接！')

	#  widget signal event functions #
	def on_search_toupdate_item(self, text):

		# 关闭刷新数据
		model_global_list.g_refresh_flag = False
		# lineEdit
		text = util.to_unicode(text)
		# 定时器更新停止
		self.main_ctrl.change_search_update(text)
		self.ui.listView_searched_item_name.viewport().repaint()
		self.ui.tableView.viewport().repaint()
		# 刷新数据
		model_global_list.g_refresh_flag = True

	def on_show_table(self, state):

		# 关闭刷新数据
		model_global_list.g_refresh_flag = False
		# 显示全表
		self.model.list_model.show_table = state
		# checkBox_show_table
		if self.ui.checkBox_show_table.isChecked():
			self.main_ctrl.change_show_table(state)
			self.ui.listView_searched_item_name.viewport().repaint()
			self.ui.tableView.viewport().repaint()
		# 开启刷新数据
		model_global_list.g_refresh_flag = True

	def on_submit_table(self):
		# 关闭刷新数据
		model_global_list.g_refresh_flag = False
		# pushButton_submit_table  pushButton_tab_differ
		self.main_ctrl.change_submit_table()
		self.ui.listView_searched_item_name.viewport().repaint()
		self.ui.tableView.viewport().repaint()

		# 开启刷新数据
		model_global_list.g_refresh_flag = True

	def on_refresh_tab(self):
		# 关闭刷新数据
		model_global_list.g_refresh_flag = False
		# pushButton_refresh
		self.main_ctrl.change_refresh_tab()
		self.ui.listView_searched_item_name.viewport().repaint()
		self.ui.tableView.viewport().repaint()
		# 开启刷新数据
		model_global_list.g_refresh_flag = True

	def on_tab_differ(self):
		# 关闭刷新数据
		model_global_list.g_refresh_flag = False
		# tab_differ
		self.main_ctrl.change_tab_differ()
		self.ui.listView_searched_item_name.viewport().repaint()
		self.ui.tableView.viewport().repaint()
		# 开启刷新数据
		model_global_list.g_refresh_flag = True

	def on_begin_point(self, value):
		# 关闭刷新数据
		model_global_list.g_refresh_flag = False
		# slider_begin   slider_begin
		# max_value = self.ui.horizontalSlider_begin.maximum()
		self.main_ctrl.change_slider_begin(value)
		self.ui.listView_searched_item_name.viewport().repaint()
		self.ui.tableView.viewport().repaint()
		# 开启刷新数据
		model_global_list.g_refresh_flag = True

	def on_end_point(self, value):
		# slider_begin   slider_end
		# 关闭刷新数据
		model_global_list.g_refresh_flag = False
		self.main_ctrl.change_slider_end(value)
		self.ui.listView_searched_item_name.viewport().repaint()
		self.ui.tableView.viewport().repaint()
		# 开启刷新数据
		model_global_list.g_refresh_flag = True

	def on_searched_item_add(self, item_index):
		# 关闭刷新数据
		model_global_list.g_refresh_flag = False
		# listView_searched_item_name
		self.main_ctrl.change_search_item_add(item_index)
		self.ui.listView_searched_item_name.viewport().repaint()
		self.ui.tableView.viewport().repaint()
		# 开启刷新数据
		model_global_list.g_refresh_flag = True

	def on_timer(self):
		slider_order = int(self.main_ctrl.change_on_timer())
		self.ui.horizontalSlider_begin.setValue(slider_order)
		self.ui.listView_searched_item_name.viewport().repaint()
		self.ui.tableView.viewport().repaint()
