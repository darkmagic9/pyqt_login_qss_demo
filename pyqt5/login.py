#!/usr/bin/env python
# -*- coding: utf-8
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QLineEdit,QDialog,QMessageBox,QAction)
from PyQt5.QtGui import QCursor,QFont,QIcon
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        self.setWindowIcon(QIcon('qt.png'))
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowMinimizeButtonHint)

        self.setWindowTitle(u"鱿鱼")
        self.setFixedSize(300, 400)
        self.setObjectName('principal')
        self.createGUI()
    def createGUI(self):
        self.frame_window = QWidget(self)
        self.frame_window.setGeometry(0, 0, 300, 40)
        self.frame_window.setObjectName('frame_window')

        self.title_frame = QLabel(self.frame_window)
        self.title_frame.setGeometry(0, 0, 300, 40)
        self.title_frame.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.title_frame.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.title_frame.setText(u"鱿鱼白名单")
        self.title_frame.setObjectName('title_frame')

        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 300, 400)
        self.container.setObjectName('container')

        # buttons
        clsfont = self.font() or QFont()
        clsfont.setFamily('Webdings')
        self.button_close = QPushButton('r', self.container, font=clsfont)
        self.button_close.setGeometry(260, 0, 40, 40)
        self.button_close.setObjectName('button_close')

        self.button_login = QPushButton(self.container)
        self.button_login.setGeometry(20, 300, 260, 40)
        self.button_login.setText(u'登录')
        self.button_login.setObjectName('button_login')
        self.button_login.setCursor(QCursor(Qt.PointingHandCursor))

        self.line_username = QLineEdit(self.container)
        self.line_username.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.line_username.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.line_username.setGeometry(20, 180, 260, 40)
        self.line_username.setPlaceholderText(u'用户名')
        self.line_username.setObjectName('line_username')
        self.ac_username = QAction()
        self.ac_username.setIcon(QIcon('username.png'))
        self.line_username.addAction(self.ac_username,QLineEdit.LeadingPosition)

        self.line_password = QLineEdit(self.container)
        self.line_password.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.line_password.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.line_password.setGeometry(20, 230, 260, 40)
        self.line_password.setEchoMode(QLineEdit.Password)
        self.line_password.setPlaceholderText(u'密码')
        self.line_password.setObjectName('line_password')
        self.ac1_password = QAction()
        self.ac1_password.setIcon(QIcon('password.png'))
        self.ac2_password = QAction()
        self.ac2_password.setToolTip('显示密码')
        self.ac2_password.setIcon(QIcon('show_pw.png'))
        self.line_password.addAction(self.ac1_password, QLineEdit.LeadingPosition)
        self.line_password.addAction(self.ac2_password, QLineEdit.TrailingPosition)

        # conexiones
        self.button_close.clicked.connect(self.close)
        self.ac2_password.triggered.connect(self.show_pass)
        self.button_login.clicked.connect(self.handleLogin)
        # 初始化焦点位于哪个控件上
        self.button_login.setFocus()   #获取焦点
    def handleLogin(self):
        # self.accept()  # 关键
        if (self.line_username.text() == 'admin' and self.line_password.text() == '123456'):
            self.accept()  # 关键
        else:
            QMessageBox.warning(
                self, u'提示', u'用户或密码错误',QMessageBox.Ok)
    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Return):
            self.handleLogin()
    def show_pass(self):
        if self.line_password.echoMode() == QLineEdit.Password:
            self.line_password.setEchoMode(QLineEdit.Normal)
        else:
            self.line_password.setEchoMode(QLineEdit.Password)
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myapp = Login()
    myapp.show()

    with open('main.css', 'r') as css:
        StyleSheet = css.read()
    # app.setStyle("cleanlooks")
    app.setStyleSheet(StyleSheet)
    sys.exit(app.exec_())