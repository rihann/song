import main_ui
from PyQt5 import QtCore, QtGui, QtWidgets,QtMultimedia
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, Qt,QEvent
import sys
from PyQt5.QtWidgets import QPushButton,QLabel,QWidget,QHBoxLayout,QVBoxLayout,QGridLayout,QScrollArea,QFormLayout,QLineEdit,QInputDialog,QTextEdit,QSystemTrayIcon,QMenu,QAction,QApplication,qApp,QToolTip
import qtawesome
import mongo_process
import my_widget
import time
import algorithms
import denglu
import registered
import yindao
class denglu_gui(QtWidgets.QMainWindow,QtCore.QObject,denglu.Ui_MainWindow):#登陆界面
    _signal = QtCore.pyqtSignal(int)
    _signal_zhuce = QtCore.pyqtSignal()
    _signal_yindao = QtCore.pyqtSignal(int)
    def __init__(self,parent=None):
        super(denglu_gui,self).__init__(parent)
        super().setupUi(self)
        self.mongo=mongo_process.process_data()
        self.user_name.returnPressed.connect(self.denglu)
        self.password.returnPressed.connect(self.denglu)
        self.pushButton.clicked.connect(self.denglu)
        self.pushButton_2.clicked.connect(self.enter_zhuce)
        self.setWindowTitle('个性化音乐推荐')
        self.setWindowIcon(QtGui.QIcon('tubiao//icon.png'))
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.statusbar.setStyleSheet("color:red")
        self.user_name.setPlaceholderText("用户名")
        self.password.setPlaceholderText("密码")
        self.password.setEchoMode(QLineEdit.Password)
        self.label.setPixmap((QPixmap('tubiao//denglu.jpg')))
        self.set_widget(self.widget)
        self.set_denglubutton(self.pushButton)
        self.set_zhucebutton(self.pushButton_2)
    def set_widget(self,btn):
        btn.setStyleSheet(
                       '''QWidget{border-image:url(tubiao//denglu_beijing.jpg);}
        ''')
    def set_denglubutton(self,qlaber):
        qlaber.setStyleSheet(
                          '''QPushButton{
                             color:white;
                             border-radius:10px;
                             background:#2ba3ff;}
                             QPushButton:hover{
                             color:white;
                             background:#156fff;}
                             QPushButton:pressed{
                             font:Bold;}
        ''')
    def set_zhucebutton(self,qlaber):
        qlaber.setStyleSheet(
                          '''QPushButton{
                             border:none;
                             color:white;}
                             QPushButton:hover{
                             font:Bold;
                             color:white;}
                             QPushButton:pressed{
                             color:#34ff41;}
        ''')
    def show_gui(self):
        self.show()
        self.setWindowState(Qt.WindowNoState)
    def quit(self):
        self.close()
        self.tray.deleteLater()
    def denglu(self):
        user_name=self.user_name.text()
        password = self.password.text()
        if(not user_name.isdigit()):
            self.statusbar.showMessage("用户名无效", 3000)
        else:
            if(not password.isdigit()):
                self.statusbar.showMessage("密码无效",3000)
            else:
                real_password = self.mongo.get_password(int(user_name))
                if (real_password != None and real_password == password):
                    self.close()
                    user_info=self.mongo.get_user_info(int(user_name))
                    data=user_info['songRecord']
                    if(len(data)>0):
                        self._signal.emit(int(user_name))
                    else:
                        self._signal_yindao.emit(int(user_name))
                        self.mongo.my_close()
                else:
                    self.statusbar.showMessage("密码或账号错误", 3000)
    def enter_zhuce(self):
        self.close()
        self._signal_zhuce.emit()
class registered_gui(QtWidgets.QMainWindow,QtCore.QObject,registered.Ui_MainWindow):
    _signal = QtCore.pyqtSignal()
    _signal_back = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(registered_gui,self).__init__(parent)
        super().setupUi(self)
        self.mongo=mongo_process.process_data()
        self.user_name.returnPressed.connect(self.zhuce)
        self.password.returnPressed.connect(self.zhuce)
        self.check_pawd.returnPressed.connect(self.zhuce)
        self.zhuce_button.clicked.connect(self.zhuce)
        self.back_button.clicked.connect(self.go_back)
        self.setWindowTitle('个性化音乐推荐')
        self.setWindowIcon(QtGui.QIcon('tubiao//icon.png'))
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setStyleSheet('''
                        #MainWindow{border-image:url(tubiao//beijing.jpg)};
                        background:transparent;
        ''')
        self.user_name.setPlaceholderText("设置你的用户名")
        self.password.setPlaceholderText("设置你的密码")
        self.check_pawd.setPlaceholderText("再次输入密码")
        self.password.setEchoMode(QLineEdit.Password)
        self.check_pawd.setEchoMode(QLineEdit.Password)
        self.set_zhuce_button(self.zhuce_button)
        self.set_back_button(self.back_button)
        self.statusbar.setStyleSheet("color:red")
    def set_zhuce_button(self, qlaber):
        qlaber.setStyleSheet(
            '''QPushButton{
               color:white;
               border-radius:10px;
               background:#2ba3ff;}
               QPushButton:hover{
               color:white;
               background:#156fff;}
               QPushButton:pressed{
               font:Bold;}
            ''')
    def set_back_button(self, qlaber):
        self.back_button.setToolTip('返回登录界面')
        qlaber.setStyleSheet(
            '''QPushButton{
               color:white;
               border-radius:10px;
               background:#ff421d;}
               QPushButton:hover{
               color:white;
               background:#ff1010;}
               QPushButton:pressed{
               font:Bold;}
            ''')
    def show_gui(self):
        self.show()
        self.setWindowState(Qt.WindowNoState)
    def quit(self):
        self.close()
    def zhuce(self):
        user_name = self.user_name.text()
        password = self.password.text()
        check_pawd = self.check_pawd.text()
        if(not user_name.isdigit()):
            self.statusbar.showMessage("用户名无效", 3000)
        else:
            if(not password.isdigit()):
                self.statusbar.showMessage("密码无效", 3000)
            else:
                real_password = self.mongo.get_password(int(user_name))
                if (real_password != None):
                    self.statusbar.showMessage("账号已被注册", 3000)
                else:
                    if(password!=check_pawd):
                        self.statusbar.showMessage("输入两次密码不一致", 3000)
                    else:
                        self.mongo.insert_user(int(user_name), password)
                        self.close()
                        self.mongo.my_close()
                        self._signal.emit()
    def go_back(self):
        self.close()
        self._signal_back.emit()
class yindao_gui(QtWidgets.QMainWindow,QtCore.QObject,yindao.Ui_MainWindow):#引导界面
    _signal = QtCore.pyqtSignal(int,list)
    def __init__(self,parent=None):
        super(yindao_gui,self).__init__(parent)
        super().setupUi(self)
        self.pushButton.clicked.connect(self.enter_main)
        self.mongo=mongo_process.process_data()
        self.setStyleSheet('''
                        #MainWindow{border-image:url(tubiao//beijing.jpg)};
                        background:transparent;
        ''')
        self.setWindowTitle('个性化音乐推荐')
        self.setWindowIcon(QtGui.QIcon('tubiao//icon.png'))
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.label_1.setStyleSheet("color:white")
        self.pushButton.setStyleSheet(
                          '''QPushButton{
                             color:white;
                             border-radius:10px;
                             background:#2ba3ff;}
                             QPushButton:hover{
                             color:white;
                             background:#156fff;}
                             QPushButton:pressed{
                             font:Bold;}
        ''')
        style_lists=self.mongo.get_all_style()
        self.comboBox.addItem('')
        for style in style_lists:
            self.comboBox.addItem(style)
        self.style_list=[]
        self.comboBox.currentIndexChanged.connect(self.show_style)
    def show_init(self,user_id):
        self.ID=user_id
        self.show()
        self.setWindowState(Qt.WindowNoState)
    def enter_main(self):
        self.close()
        self.style_list=list(set(self.style_list))
        self._signal.emit(self.ID,self.style_list)
    def show_style(self,i):
        current_text=self.display_style.text()
        local_text=self.comboBox.currentText()
        self.style_list.append(local_text)
        new_text=current_text+"  "+local_text
        self.display_style.setText(new_text+"\n")
        self.display_style.setStyleSheet("color:white")
class main_gui(QtWidgets.QMainWindow,QtCore.QObject,main_ui.Ui_MainWindow):
    _signal=QtCore.pyqtSignal(dict)
    def __init__(self,parent=None):
        super(main_gui,self).__init__(parent)
        super().setupUi(self)
        self.music_count = 0
        self.mongo = mongo_process.process_data()
        self.set_recommend()
        self.set_process_bar()
        self.setWindowTitle('个性化音乐推荐')
        self.setWindowIcon(QtGui.QIcon('tubiao//icon.png'))
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setStyleSheet('''
                        #MainWindow{border-image:url(tubiao//beijing.jpg)};
                        background:transparent;
        ''')

        self.img_label.setPixmap(QPixmap('tubiao//gedan.png'))
        self.sousuo.clicked.connect(self.find_music_singer)
        self.sousuo_input.returnPressed.connect(self.find_music_singer)
        self.sousuo.setIcon(qtawesome.icon('fa.search',color='white'))
        self.sousuo.setStyleSheet("border:none")
        self.sousuo_input.setPlaceholderText("搜索音乐，歌手，音乐类型")
        self.sousuo_input.setStyleSheet(
                          '''QLineEdit{
                             border:1px solid gray;
                             width:300px;
                             border-radius:10px;
                             padding:2px 4px;
                             background:transparent;
                             color:white;}
                               ''')
        self.set_background_style(self.music_form)
        self.set_background_style(self.scrollAreaWidgetContents_2)
        self.set_background_style(self.scrollArea)
        self.music_form_info.setStyleSheet("color:white")
        self.user_info.setStyleSheet("color:#8f8f8f")
        self.statusbar.setStyleSheet("color:red")
        self.algorithn1_form_info = {}  # 推荐算法一歌单
        self.algorithn2_form_info = {}  # 推荐算法二歌单
        self.player = QtMultimedia.QMediaPlayer()
        self.player.durationChanged.connect(self.set_dateDuration)
        self.player.positionChanged.connect(self.update_position)
        self.style_list=self.mongo.get_all_style()
        for style in self.style_list:
            self.comboBox.addItem(style)
        self.comboBox.currentIndexChanged.connect(self.show_style)
    def show_gui(self,user_name):
        self.ID = user_name
        self.get_user_history_form()
        self.music_forms()
        self.user_info.setText('用户名:'+str(self.ID))
        self.trayIcon()
        self.show()
        self.setWindowState(Qt.WindowNoState)
    def show_gui_yindao(self,user_name,style_list):
        self.ID = user_name
        self.get_user_history_form()
        self.music_forms()
        self.user_info.setText('用户名:' + str(self.ID))
        self.style_list_love=style_list
        self.local_music_info=self.mongo.return_song_in_style_list(self.style_list_love)
        self.show_sousuo()
        self.music_form_info.setText('根据您喜欢的音乐风格，给您推荐的音乐')
        self.trayIcon()
        self.show()
        self.setWindowState(Qt.WindowNoState)
    def show_style(self,i):
        data,a=self.mongo.get_sousuo(self.comboBox.currentText())
        if(data!=None):
            self.local_music_info=data
            self.show_sousuo()
    def set_recommend(self):#设置三个推荐内容模块，和歌单
        self.QPushButton_algorithm1=QPushButton(qtawesome.icon('fa.music',color='#bababa'),'协同过滤')
        self.QPushButton_history=QPushButton(qtawesome.icon('fa.music',color='#bababa'),'历史播放')#按照播放频率排序
        self.QPushButton_fav=QPushButton(qtawesome.icon('fa.heart',color='#bababa'),'我的关注')#按照播放频率排序
        self.QPushButton_algorithm2=QPushButton(qtawesome.icon('fa.music',color='#bababa'),'内容推荐')
        self.Qlabel_1 = QLabel('推荐')
        self.Qlabel_2 = QLabel('我的音乐')
        self.Qlabel_3 = QLabel(''+'\n')
        self.QPushButton_history.clicked.connect(self.control_music_form)
        self.QPushButton_fav.clicked.connect(self.control_music_form)
        self.QPushButton_algorithm1.clicked.connect(self.control_music_form)
        self.QPushButton_algorithm2.clicked.connect(self.control_music_form)
        #将按钮加入布局
        self.left_layout.addWidget(self.Qlabel_1)
        self.left_layout.addWidget(self.QPushButton_algorithm1)
        self.left_layout.addWidget(self.QPushButton_algorithm2)
        self.left_layout.addWidget(self.Qlabel_3)
        self.left_layout.addWidget(self.Qlabel_2)
        self.left_layout.addWidget(self.QPushButton_history)
        self.left_layout.addWidget(self.QPushButton_fav)
        self.set_putton_style(self.QPushButton_history)
        self.set_putton_style(self.QPushButton_algorithm1)
        self.set_putton_style(self.QPushButton_algorithm2)
        self.set_putton_style(self.QPushButton_fav)
        self.set_qlabel_style(self.Qlabel_1)
        self.set_qlabel_style(self.Qlabel_2)
    def set_qlabel_style(self,btn):
        btn.setStyleSheet('''QLabel{
                          color:#676767;
                          font-size:14px;
                          }              
        ''')
    def set_putton_style(self,btn):
        btn.setStyleSheet('''
                    QPushButton{
                        color:#bababa;
                        border:none;
                        font-size:15px;
                        text-align:left;
                    }
                    QPushButton:hover{color:white;}
                ''')
    def set_background_style(self,btn):
        btn.setStyleSheet("background-color:transparent;")
    def control_music_form(self):
        btn=self.sender()
        if(btn.text()=='历史播放'):
            self.music_form_info.setText('历史播放记录列表')
            self.get_user_history_form()
            self.local_music_info=self.history_form_info
            self.show_music_form(0)
        if (btn.text() == '我的关注'):
            self.music_form_info.setText('我的关注列表')
            self.get_user_fav_form()
            self.local_music_info = self.fav_form_info
            self.show_music_form(2)
        if(btn.text()=='协同过滤'):
            if(len(self.history_form_info)>=10):
                if (len(self.algorithn1_form_info) > 0):
                    self.music_form_info.setText('基于nmf模型的协同过滤推荐')
                    self.local_music_info = self.algorithn1_form_info
                    self.show_music_form(1)
                else:
                    self.work_1 = work_algorithm_1(self.ID)
                    self.work_1.qt_signal.connect(self.respond_algorithm_1)
                    self.work_1.start()
            else:
                self.statusbar.showMessage('请先听10首音乐以上，再点击推荐', 3000)
        if (btn.text() == '内容推荐'):
            if (len(self.history_form_info) >= 10):
                if (len(self.algorithn2_form_info) > 0):
                    self.music_form_info.setText('基于knn模型的内容推荐')
                    self.local_music_info = self.algorithn2_form_info
                    self.show_music_form(1)
                else:
                    self.work_2 = work_algorithm_2(self.ID)
                    self.work_2.qt_signal.connect(self.respond_algorithm_2)
                    self.work_2.start()
            else:
                self.statusbar.showMessage('请先听10首音乐以上，再点击推荐', 3000)
    def respond_algorithm_1(self,info,song_list):
        self.work_1.quit()
        self.algorithn1_form_info = self.get_recommend(song_list)
        self.music_form_info.setText('基于nmf模型的协同过滤推荐')
        self.local_music_info = self.algorithn1_form_info
        self.show_music_form(1)
        self.statusbar.showMessage(info, 3000)
    def respond_algorithm_2(self,info,song_list):
        self.work_2.quit()
        self.algorithn2_form_info = self.get_recommend(song_list)
        self.music_form_info.setText('基于逻辑回归模型的内容推荐')
        self.local_music_info = self.algorithn2_form_info
        self.show_music_form(1)
        self.statusbar.showMessage(info, 3000)
    def music_forms(self):
        self.music_layout=QFormLayout()
        music_widget=QWidget()
        music_widget.setLayout(self.music_layout)
        self.music_form.setWidget(music_widget)
        self.music_form.setWidgetResizable(True)
        self.music_form_info.setText('欢迎使用个性化音乐推荐系统')

    def set_process_bar(self):#进度条及播放控制
        self.music_name_label=QLabel()
        self.music_name_label.setFixedHeight(15)
        self.music_name_label.setContentsMargins(20,0,0,0)
        self.music_name_label.setWordWrap(True)
        self.music_name_label.setStyleSheet("color:white")
        self.right_process_bar = QtWidgets.QProgressBar()  # 播放进度部件
        self.right_process_bar.setRange(0,100)
        self.right_process_bar.setValue(0)
        self.right_process_bar.setFixedHeight(6)  # 设置进度条高度
        self.right_process_bar.setTextVisible(False)  # 不显示进度条文字
        self.right_process_bar.setStyleSheet('''
                             QProgressBar{
                             border-radius:3px;
                             background-color:#676767;
                             }
                             QProgressBar::chunk{
                             background-color:red;
                             border-radius:3px;
                             width:1px;
                             }
                             ''')
        self.left_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
        self.left_playconsole_layout = QtWidgets.QHBoxLayout()  # 播放控制部件水平布层
        self.left_playconsole_widget.setLayout(self.left_playconsole_layout)
        self.console_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.backward', color='red'), "")
        self.console_button_1.clicked.connect(self.play_before)
        self.console_button_1.setIconSize(QtCore.QSize(20, 20))
        self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='red'), "")
        self.console_button_2.clicked.connect(self.play_next)
        self.console_button_2.setIconSize(QtCore.QSize(20, 20))
        self.console_button_3 = my_widget.my_pause_putton()
        self.console_button_3.clicked.connect(self.pause_music)
        self.console_button_3.setIconSize(QtCore.QSize(30, 30))
        self.left_playconsole_layout.addWidget(self.console_button_1)
        self.left_playconsole_layout.addWidget(self.console_button_3)
        self.left_playconsole_layout.addWidget(self.console_button_2)
        self.console_button_1.setStyleSheet("border:none")
        self.console_button_2.setStyleSheet("border:none")
        self.console_button_3.setStyleSheet("border:none")
        self.left_playconsole_layout.setAlignment(QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示
        self.procee_up_layout = QHBoxLayout()
        self.procee_up_widget = QtWidgets.QWidget()
        self.procee_up_widget.setLayout(self.procee_up_layout)
        self.procee_up_layout.addWidget(self.left_playconsole_widget)
        self.procee_up_layout.addWidget(self.right_process_bar)
        self.process_layout.addWidget(self.music_name_label)
        self.process_layout.addWidget(self.procee_up_widget)
    def show_music_form(self,flag):#歌曲列表界面
        self.clear_music_form()
        self.music_count = 0
        qlabel_music_name = QLabel('音乐名')
        qlabel_music_singer = QLabel('歌手')
        qlabel_music_style = QLabel('歌曲类型')
        qlabel_music_time = QLabel('时长')
        if(flag==0):
            qlabel_music_num = QLabel('播放次数')
        qlabel_music_score = QLabel('分数')
        qlabel = QLabel('')
        qlabe2 = QLabel('')
        qlabe3 = QLabel('')
        h = QWidget()
        layout = QHBoxLayout()
        h.setLayout(layout)
        layout.addWidget(qlabel_music_name)
        layout.addWidget(qlabel_music_singer)
        layout.addWidget(qlabel_music_style)
        layout.addWidget(qlabel_music_time)
        if(flag==0):
            layout.addWidget(qlabel_music_num)
        layout.addWidget(qlabel_music_score)
        layout.addWidget(qlabel)
        layout.addWidget(qlabe2)
        layout.addWidget(qlabe3)
        self.set_music_title(qlabel_music_name)
        self.set_music_title(qlabel_music_singer)
        self.set_music_title(qlabel_music_style)
        self.set_music_title(qlabel_music_time)
        if(flag==0):
            self.set_music_title(qlabel_music_num)
        self.set_music_title(qlabel_music_score)
        self.set_button(qlabel)
        self.set_button(qlabe2)
        self.set_button(qlabe3)
        layout.setSpacing(15)
        self.music_layout.addRow(h)
        for data in self.local_music_info:
                qlabel_music_name = QLabel(data)
                qlabel_music_singer = QLabel(self.local_music_info[data]['author'])
                qlabel_music_style = QLabel(self.local_music_info[data]['style'])
                qlabel_music_time = QLabel()
                qlabel_music_time.setText(self.process_time(self.local_music_info[data]['time']))
                if(flag==0):
                    qlabel_music_num = QLabel()
                    qlabel_music_num.setText(str(self.history_form_user[data][0]))
                    qlabel_score = QLabel()
                    qlabel_score.setText(str(round(self.history_form_user[data][1], 2)))
                else:
                    qlabel_score = QLabel()
                    qlabel_score.setText(str(8))
                score_button=my_widget.my_pushbutton_love(data)
                score_button.clicked.connect(self.get_score)

                play_button=my_widget.my_pushbutton_play(data,self.local_music_info[data]['download_path'])
                play_button.clicked.connect(self.play_music)

                if(flag!=2):
                    fav_button = my_widget.my_favorite(data)
                    fav_button.clicked.connect(self.add_fav)

                if(flag==2):
                    del_button = my_widget.my_favorite_del(data)
                    del_button.clicked.connect(self.del_fav)

                h= QWidget()
                layout = QHBoxLayout()
                h.setLayout(layout)
                layout.addWidget(qlabel_music_name)
                layout.addWidget(qlabel_music_singer)
                layout.addWidget(qlabel_music_style)
                layout.addWidget(qlabel_music_time)
                if(flag==0):
                    layout.addWidget(qlabel_music_num)
                layout.addWidget(qlabel_score)
                layout.addWidget(play_button)
                if(flag!=2):
                    layout.addWidget(fav_button)
                if(flag==2):
                    layout.addWidget(del_button)
                layout.addWidget(score_button)
                self.set_music_content2(qlabel_music_name)
                self.set_music_content3(qlabel_music_singer)
                self.set_music_content(qlabel_music_style)
                self.set_music_content(qlabel_music_time)
                if (flag == 0):
                    self.set_music_content(qlabel_music_num)
                self.set_music_content(qlabel_score)
                self.set_button(play_button)
                if (flag != 2):
                    self.set_button2(fav_button)
                if (flag == 2):
                    self.set_button2(del_button)
                self.set_button(score_button)
                layout.setSpacing(15)
                qlabel_music_name.setToolTip(data)
                qlabel_music_singer.setToolTip(self.local_music_info[data]['author'])
                self.music_layout.addRow(h)
                self.music_count = self.music_count + 1
    def show_sousuo(self):#输入音乐列表，展示结果.
        self.clear_music_form()
        self.music_form_info.setText('搜索结果')
        self.music_count = 0
        qlabel_music_name = QLabel('音乐标题')
        qlabel_music_singer = QLabel('歌手')
        qlabel_music_style = QLabel('歌曲类型')
        qlabel_music_time = QLabel('时长')
        qlabe1 = QLabel('')
        qlabe2 = QLabel('')
        h = QWidget()
        layout = QHBoxLayout()
        h.setLayout(layout)
        layout.addWidget(qlabel_music_name)
        layout.addWidget(qlabel_music_singer)
        layout.addWidget(qlabel_music_style)
        layout.addWidget(qlabel_music_time)
        layout.addWidget(qlabe1)
        layout.addWidget(qlabe2)
        layout.setSpacing(25)
        self.set_sousuo_title(qlabel_music_name)
        self.set_sousuo_title(qlabel_music_singer)
        self.set_sousuo_title(qlabel_music_style)
        self.set_sousuo_title(qlabel_music_time)
        self.set_button(qlabe1)
        self.set_button(qlabe2)
        self.music_layout.addRow(h)
        for data in self.local_music_info:
            qlabel_music_name = QLabel(data)
            qlabel_music_singer = QLabel(self.local_music_info[data]['author'])
            qlabel_music_style = QLabel(self.local_music_info[data]['style'])

            qlabel_music_time = QLabel()
            qlabel_music_time.setText(self.process_time(self.local_music_info[data]['time']))

            play_button = my_widget.my_pushbutton_play(data,self.local_music_info[data]['download_path'])
            play_button.clicked.connect(self.play_music)

            fav_button = my_widget.my_favorite(data)
            fav_button.clicked.connect(self.add_fav)

            h = QWidget()
            layout = QHBoxLayout()
            h.setLayout(layout)
            layout.addWidget(qlabel_music_name)
            layout.addWidget(qlabel_music_singer)
            layout.addWidget(qlabel_music_style)
            layout.addWidget(qlabel_music_time)
            layout.addWidget(play_button)
            layout.addWidget(fav_button)
            layout.setSpacing(25)
            self.set_sousuo_content2(qlabel_music_name)
            self.set_sousuo_content3(qlabel_music_singer)
            self.set_sousuo_content(qlabel_music_style)
            self.set_sousuo_content(qlabel_music_time)
            self.set_button(play_button)
            self.set_button2(fav_button)
            qlabel_music_name.setToolTip(data)
            qlabel_music_singer.setToolTip(self.local_music_info[data]['author'])
            self.music_layout.addRow(h)
            self.music_count = self.music_count + 1
    def set_sousuo_title(self,btn):
        btn.setFixedWidth(80)
        btn.setStyleSheet("color:#bababa")
    def set_music_title(self,btn):
        btn.setFixedWidth(60)
        btn.setStyleSheet("color:#bababa")
    def set_sousuo_content(self, btn):
        btn.setFixedWidth(80)
        btn.setStyleSheet('''
                        QLabel{color:#bababa;
                        
                        }
                                        ''')
    def set_music_content(self, btn):
        btn.setFixedWidth(60)
        btn.setStyleSheet('''
                        QLabel{color:#bababa;

                        }
                                        ''')
    def set_sousuo_content2(self,btn):
        btn.setFixedWidth(80)
        btn.setStyleSheet('''
                    QLabel{color:white;}
                    QToolTip{color:white;border:0px;}
                    ''')
    def set_music_content2(self,btn):
        btn.setFixedWidth(60)
        btn.setStyleSheet('''
                    QLabel{color:white;}
                    QToolTip{color:white;border:0px;}
                    ''')
    def set_sousuo_content3(self,btn):
        btn.setFixedWidth(80)
        btn.setStyleSheet('''
                    QLabel{color:#bababa;}
                    QLabel:hover{color:white;}
                    QToolTip{color:white;border:0px;}
                    ''')
    def set_music_content3(self,btn):
        btn.setFixedWidth(60)
        btn.setStyleSheet('''
                    QLabel{color:#bababa;}
                    QLabel:hover{color:white;}
                    QToolTip{color:white;border:0px;}
                    ''')
    def set_button(self,btn):
        btn.setFixedWidth(30)
        btn.setStyleSheet('''
                            QPushButton{color:#bababa;
                            }
                            QPushButton:hover{color:white;font:bold;}
                        ''')
    def set_button2(self,btn):
        btn.setFixedWidth(30)
        btn.setStyleSheet('''
                            QPushButton{color:#ff2c07;
                            }
                            QPushButton:hover{color:red;font:bold;}
                        ''')
    def process_time(self,second):
        min=int(second/60)
        sec=second%60
        return str(min)+':'+str(sec)
    def clear_music_form(self):#移除form布局
        for i in range(self.music_count+1):
            self.music_layout.removeRow(0)
    def get_user_history_form(self):#获得用户历史歌单
        self.history_form_user,self.history_form_info=self.mongo.get_user_music(self.ID)
    def get_user_fav_form(self):#获得用户收藏歌单
        self.fav_form_user,self.fav_form_info=self.mongo.get_user_music_fav(self.ID)
    def get_recommend(self,music_list):#获得推荐的歌单数据
        return self.mongo.get_recommend_form(music_list)
    def play_music(self):#播放音乐
        btn=self.sender()
        self.music_name=btn.music_name
        address=btn.music_address
        self.music_name_label.setText(self.music_name)
        self.mongo.update_music(self.ID, self.music_name)
        url = QUrl.fromLocalFile(address)
        content=QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
    def pause_music(self):#暂停和播放音乐
        btn = self.sender()
        if(btn.flag==True):
            self.player.pause()
        else:
            self.player.play()
        btn.auto_change()

    def set_dateDuration(self,duration):#设置进度条范围
        self.right_process_bar.setRange(0,duration)
        self.right_process_bar.setEnabled(duration>0)
    def update_position(self,position):#实时计时器
        self.right_process_bar.setValue(position)
    def find_music_singer(self):
        text=self.sousuo_input.text()
        out,singer_info=self.mongo.get_sousuo(text)
        if(len(out)==0):
            self.statusbar.showMessage('没有搜索到相关信息', 3000)
        else:
            self.local_music_info=out
            self.show_sousuo()
            if(singer_info!=None):
                self.music_form_info.setText(singer_info)
    def play_next(self):#播放下一首歌
        music = self.music_name
        music_list = list(self.local_music_info)
        index_name = music_list.index(music)
        if (index_name == (len(music_list) - 1)):
            index_name = 0
        else:
            index_name = index_name + 1
        self.music_name = music_list[index_name]
        address = self.local_music_info[self.music_name]['download_path']
        self.music_name_label.setText(self.music_name)
        self.mongo.update_music(self.ID, self.music_name)
        url = QUrl.fromLocalFile(address)
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def play_before(self):#播放上一首歌
        music=self.music_name
        music_list = list(self.local_music_info)
        index_name = music_list.index(music)
        if (index_name == 0):
            index_name = -1
        else:
            index_name = index_name - 1
        self.music_name = music_list[index_name]
        address = self.local_music_info[self.music_name]['download_path']
        self.music_name_label.setText(self.music_name)
        self.mongo.update_music(self.ID, self.music_name)
        url = QUrl.fromLocalFile(address)
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
    def get_score(self):#更新分数
        btn=self.sender()
        d, okPressed = QInputDialog.getDouble(self, "评分", "分数(1-10):", 10)
        self.mongo.update_score(self.ID,btn.music_name,d)
    def add_fav(self):
        btn = self.sender()
        music_name = btn.music_name
        self.mongo.insert_fav(self.ID,music_name)
        self.statusbar.showMessage("已关注", 3000)
    def del_fav(self):
        btn = self.sender()
        music_name = btn.music_name
        self.mongo.delete_fav(self.ID,music_name)
        self.statusbar.showMessage("已取消关注", 3000)
        self.get_user_fav_form()
        self.local_music_info = self.fav_form_info
        self.show_music_form(2)

    def trayIcon(self):
        self.tray = QtWidgets.QSystemTrayIcon()  # 创建托盘
        self.tray.setIcon(QtGui.QIcon('tubiao//icon.png'))  # 设置托盘图标
        self.tray.activated.connect(self.iconActivated)  # 托盘图标被激活
        self.tray.setToolTip(u'个性化音乐推荐系统')
        trayMenu = QtWidgets.QMenu()  # 创建托盘的右键菜单
        RestoreAction = QtWidgets.QAction(u'最小化/恢复',self)
        RestoreAction.triggered.connect(self.doubleclick)
        PauseAction = QtWidgets.QAction(u'暂停',self)
        PauseAction.triggered.connect(self.player.pause)
        PlayAction = QtWidgets.QAction(u'播放', self)
        PlayAction.triggered.connect(self.player.play)
        NextAction = QtWidgets.QAction(u'下一首',self)
        NextAction.triggered.connect(self.play_next)
        BeforeAction = QtWidgets.QAction(u'上一首', self)
        BeforeAction.triggered.connect(self.play_before)
        QuitAction = QtWidgets.QAction(u'退出',self)
        QuitAction.triggered.connect(self.sys_quit)
        trayMenu.addAction(RestoreAction)
        trayMenu.addAction(PauseAction)
        trayMenu.addAction(PlayAction)
        trayMenu.addAction(NextAction)
        trayMenu.addAction(BeforeAction)
        trayMenu.addAction(QuitAction)
        self.tray.setContextMenu(trayMenu)  # 把tpMenu设定为托盘的右键菜单
        self.tray.show()
        self.tray.showMessage("添加到托盘", "可以最小化到托盘", icon=0)

    def iconActivated(self, reason):
        if (reason == QtWidgets.QSystemTrayIcon.DoubleClick):  # 双击 显示或隐藏窗口
            self.doubleclick()
        elif (reason == QtWidgets.QSystemTrayIcon.Trigger):  # 单击  #<code>MiddleClick</code>  中键双击
            pass

    def doubleclick(self):
        if self.isMinimized() or not self.isVisible():
            # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
            self.showNormal()
            self.activateWindow()
        else:
            # 若不是最小化，则最小化
            self.hide()
            self.tray.show()
            self.tray.showMessage("","已最小化到托盘",icon=0)

    def sys_quit(self):
        self.hide()
        self.tray.show()
        self.tray.showMessage("","已退出程序",icon=0)
        time.sleep(3)
        self.tray.deleteLater()
        qApp.quit()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,
                                               '',
                                               "是否要最小化程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Yes
                                               )
        if reply == QtWidgets.QMessageBox.Yes:
            event.ignore()
            self.hide()
            self.tray.show()
            self.tray.showMessage("","已最小化到托盘",icon=0)
        else:
            self.sys_quit()

class work_algorithm_1(QtCore.QThread,QtCore.QObject):#推荐算法一，工作线程
    qt_signal = QtCore.pyqtSignal(str,list)

    def __init__(self, ID,parent=None):
        super(work_algorithm_1, self).__init__(parent)
        self.ID=ID

    def run(self):
        model=algorithms.my_model_nmf()
        model.init_datebase()
        model.train_model()
        song_list=model.recommed_song(self.ID)
        self.qt_signal.emit('已经完成协同过滤推荐',song_list)
class work_algorithm_2(QtCore.QThread,QtCore.QObject):#推荐算法二，工作线程
    qt_signal = QtCore.pyqtSignal(str,list)

    def __init__(self, ID,parent=None):
        super(work_algorithm_2, self).__init__(parent)
        self.ID=ID

    def run(self):
        model=algorithms.my_model_knn()
        model.init_datebase()
        song_list=model.recommend_Logistic(self.ID)
        self.qt_signal.emit('已经完成内容推荐',song_list)
app = QtWidgets.QApplication(sys.argv)

denglu_MainWindow=QtWidgets.QMainWindow()
denglu_ui=denglu_gui(denglu_MainWindow)
denglu_ui.show()


yindao_MainWindow=QtWidgets.QMainWindow()
yindao_ui=yindao_gui(yindao_MainWindow)

zhuce_MainWindow=QtWidgets.QMainWindow()
zhuce_ui=registered_gui(zhuce_MainWindow)

MainWindow1 = QtWidgets.QMainWindow()
main_gui=main_gui(MainWindow1)

zhuce_ui._signal.connect(denglu_ui.show_gui)
zhuce_ui._signal_back.connect(denglu_ui.show_gui)
denglu_ui._signal_zhuce.connect(zhuce_ui.show_gui)
denglu_ui._signal_yindao.connect(yindao_ui.show_init)
yindao_ui._signal.connect(main_gui.show_gui_yindao)

denglu_ui._signal.connect(main_gui.show_gui)
sys.exit(app.exec_())
