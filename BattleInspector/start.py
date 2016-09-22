# __author__ = 'gzdaifeng'
# -*- coding: utf-8 -*-
# 2016-05-27 23:08


import sys
from PyQt4 import QtGui
from model.main_model import Model
from view.main_view import MainView
from controller.main_controller import MainController
# -------------------------------------------------------------------------------------------------------------------- #
# 程序入口 --- MVC模型的定义
# -------------------------------------------------------------------------------------------------------------------- #


class StartQT4(QtGui.QApplication):

	def __init__(self, sys_argv):
		# QtGui.QMainWindow.__init__(self)
		super(StartQT4, self).__init__(sys_argv)
		self.model = Model()
		self.main_ctrl = MainController(self.model)
		self.main_view = MainView(self.model, self.main_ctrl)
		self.main_view.show()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	my_app = StartQT4(sys.argv)
	# my_app = StartQT4()
	sys.exit(app.exec_())


