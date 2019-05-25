from PyQt5 import QtCore, QtGui, QtWidgets,QtMultimedia
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QPushButton,QLabel,QWidget,QHBoxLayout,QVBoxLayout,QGridLayout,QScrollArea,QFormLayout,QLineEdit,QInputDialog,QTextEdit,QSystemTrayI

class tray(QtWidgets.QMainWindow,QtCore.QObject):
        self.tray = QSystemTrayIcon()  # 创建系统托盘对象
        self.tray.setIcon(QtGui.QIcon('tubiao//icon.png'))  # 设置系统托盘图标
        self.tray_menu = QMenu(QApplication.desktop())  # 创建菜单
        self.RestoreAction = QAction(u'还原 ', self, triggered=self.show)  # 添加一级菜单动作选项(还原主窗口)
        self.QuitAction = QAction(u'退出 ', self, triggered=qApp.quit)  # 添加一级菜单动作选项(退出程序)
        self.tray_menu.addAction(self.RestoreAction)  # 为菜单添加动作
        self.tray_menu.addAction(self.QuitAction)
        self.tray.setContextMenu(self.tray_menu)  # 设置系统托盘菜单

        def trayIcon(self):
                tray = QtGui.QSystemTrayIcon(self)  # 创建托盘
                tray.setIcon(QtGui.QIcon('tubiao//icon.png'))  # 设置托盘图标
                tray.activated.connect(self.iconActivated)   # 托盘图标被激活
                # 设置提示信息
                tray.setToolTip(u'个性化音乐推荐系统')
                tpMenu = QtGui.QMenu()          # 创建托盘的右键菜单
                RestoreAction = QtGui.QAction(QtGui.QIcon('exit.png'), u'还原', self)  # 添加一级菜单动作选项(还原程序)
                RestoreAction.triggered.connect(self.about)
                QuitAction = QtGui.QAction(QtGui.QIcon('exit.png'), u'退出', self)  # 添加一级菜单动作选项(退出程序)
                QuitAction.triggered.connect(self.quit)
                tpMenu.addAction(RestoreAction)
                tpMenu.addAction(QuitAction)
                tray.setContextMenu(tpMenu)  # 把tpMenu设定为托盘的右键菜单
                tray.show()  # 显示托盘
                tray.showMessage(u"标题", '托盘信息内容', icon=1)  # icon的值  0没有图标  1是提示  2是警告  3是错误 托盘创建出来时显示的信息

        def closeEvent(self, event):
                event.ignore()  # 忽略关闭事件
                self.hide()  # 隐藏窗体

        def iconActivated(self, reason):
                if reason == QtGui.QSystemTrayIcon.DoubleClick:  # 双击 显示或隐藏窗口
                        self.doubleclick()
                elif reason == QtGui.QSystemTrayIcon.Trigger:  # 单击  #<code>MiddleClick</code>  中键双击
                        pass

        def doubleclick(self):
                if self.isMinimized() or not self.isVisible():
                        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                        self.showNormal()
                        self.activateWindow()
                else:
                        # 若不是最小化，则最小化
                        self.showMinimized()