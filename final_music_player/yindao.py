# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yindao.ui'
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
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(620, 480, 75, 31))
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(429, 220, 91, 26))
        self.comboBox.setStyleSheet("background-color: rgb(79, 79, 79);\n"
"color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(348, 176, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.display_style = QtWidgets.QLabel(self.centralwidget)
        self.display_style.setGeometry(QtCore.QRect(420, 250, 201, 221))
        self.display_style.setText("")
        self.display_style.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.display_style.setWordWrap(False)
        self.display_style.setObjectName("display_style")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "进入主页"))
        self.label_1.setText(_translate("MainWindow", "选择喜欢的音乐类型"))

