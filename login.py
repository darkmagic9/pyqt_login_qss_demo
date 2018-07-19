#!/usr/bin/env python
# -*- coding: utf-8
from PyQt4.QtGui import (
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QCursor,
    QFont,
    QDialog,
    QMessageBox
)
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication
class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(u"鱿鱼")
        self.setFixedSize(300, 400)
        # self.setMaximumSize(300, 400)
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
        self.line_username.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.line_username.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.line_username.setGeometry(20, 180, 260, 40)
        self.line_username.setPlaceholderText(u'请输入用户名           ')
        self.line_username.setObjectName('line_username')

        self.line_password = QLineEdit(self.container)
        self.line_password.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.line_password.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.line_password.setGeometry(20, 230, 260, 40)
        self.line_password.setEchoMode(QLineEdit.Password)
        self.line_password.setPlaceholderText(u'请输入密码             ')
        self.line_password.setObjectName('line_password')

        # conexiones
        self.button_close.clicked.connect(self.close)
        self.button_login.clicked.connect(self.handleLogin)
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