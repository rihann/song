# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'registered.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.user_name = QtWidgets.QLineEdit(self.centralwidget)
        self.user_name.setGeometry(QtCore.QRect(430, 120, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.user_name.setFont(font)
        self.user_name.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.user_name.setObjectName("user_name")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(430, 180, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.password.setFont(font)
        self.password.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.password.setObjectName("password")
        self.zhuce_button = QtWidgets.QPushButton(self.centralwidget)
        self.zhuce_button.setGeometry(QtCore.QRect(550, 300, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.zhuce_button.setFont(font)
        self.zhuce_button.setObjectName("zhuce_button")
        self.check_pawd = QtWidgets.QLineEdit(self.centralwidget)
        self.check_pawd.setGeometry(QtCore.QRect(430, 240, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.check_pawd.setFont(font)
        self.check_pawd.setObjectName("check_pawd")
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(430, 300, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.back_button.setFont(font)
        self.back_button.setObjectName("back_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.user_name, self.password)
        MainWindow.setTabOrder(self.password, self.check_pawd)
        MainWindow.setTabOrder(self.check_pawd, self.zhuce_button)
        MainWindow.setTabOrder(self.zhuce_button, self.back_button)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.zhuce_button.setText(_translate("MainWindow", "注册"))
        self.back_button.setText(_translate("MainWindow", "返回"))

