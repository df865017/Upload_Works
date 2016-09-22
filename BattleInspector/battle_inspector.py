# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'battle_inspector.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainView(object):
    def setupUi(self, MainView):
        MainView.setObjectName(_fromUtf8("MainView"))
        MainView.resize(819, 605)
        self.centralwidget = QtGui.QWidget(MainView)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 791, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_search_toupdate_item = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_search_toupdate_item.setObjectName(_fromUtf8("lineEdit_search_toupdate_item"))
        self.horizontalLayout.addWidget(self.lineEdit_search_toupdate_item)
        self.pushButton_refresh = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.pushButton_submit_table = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_submit_table.setObjectName(_fromUtf8("pushButton_submit_table"))
        self.horizontalLayout.addWidget(self.pushButton_submit_table)
        self.pushButton_tab_differ = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_tab_differ.setObjectName(_fromUtf8("pushButton_tab_differ"))
        self.horizontalLayout.addWidget(self.pushButton_tab_differ)
        self.listView_searched_item_name = QtGui.QListView(self.centralwidget)
        self.listView_searched_item_name.setGeometry(QtCore.QRect(10, 60, 81, 481))
        self.listView_searched_item_name.setObjectName(_fromUtf8("listView_searched_item_name"))
        self.horizontalSlider_begin = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider_begin.setGeometry(QtCore.QRect(150, 70, 659, 16))
        self.horizontalSlider_begin.setMinimum(0)
        self.horizontalSlider_begin.setMaximum(100)
        self.horizontalSlider_begin.setProperty("value", 0)
        self.horizontalSlider_begin.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_begin.setInvertedAppearance(False)
        self.horizontalSlider_begin.setObjectName(_fromUtf8("horizontalSlider_begin"))
        self.label_end = QtGui.QLabel(self.centralwidget)
        self.label_end.setGeometry(QtCore.QRect(100, 100, 24, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_end.setFont(font)
        self.label_end.setObjectName(_fromUtf8("label_end"))
        self.label_begin = QtGui.QLabel(self.centralwidget)
        self.label_begin.setGeometry(QtCore.QRect(100, 70, 40, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_begin.setFont(font)
        self.label_begin.setObjectName(_fromUtf8("label_begin"))
        self.horizontalSlider_end = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider_end.setGeometry(QtCore.QRect(150, 100, 661, 20))
        self.horizontalSlider_end.setMinimum(0)
        self.horizontalSlider_end.setMaximum(100)
        self.horizontalSlider_end.setProperty("value", 0)
        self.horizontalSlider_end.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_end.setObjectName(_fromUtf8("horizontalSlider_end"))
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(100, 120, 711, 421))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.checkBox_show_table = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_show_table.setGeometry(QtCore.QRect(100, 50, 71, 16))
        self.checkBox_show_table.setObjectName(_fromUtf8("checkBox_show_table"))
        self.connect_state = QtGui.QLabel(self.centralwidget)
        self.connect_state.setGeometry(QtCore.QRect(460, 50, 421, 16))
        self.connect_state.setText(_fromUtf8(""))
        self.connect_state.setObjectName(_fromUtf8("connect_state"))
        MainView.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 819, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainView.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainView)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainView.setStatusBar(self.statusbar)

        self.retranslateUi(MainView)
        QtCore.QMetaObject.connectSlotsByName(MainView)

    def retranslateUi(self, MainView):
        MainView.setWindowTitle(_translate("MainView", "MainWindow", None))
        self.pushButton_refresh.setText(_translate("MainView", "刷新", None))
        self.pushButton_submit_table.setText(_translate("MainView", "提交表格修改", None))
        self.pushButton_tab_differ.setText(_translate("MainView", "时间轴差异对比", None))
        self.label_end.setText(_translate("MainView", "end", None))
        self.label_begin.setText(_translate("MainView", "begin", None))
        self.checkBox_show_table.setText(_translate("MainView", "显示全表", None))

