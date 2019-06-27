#!/usr/bin/env python
# -*- coding: utf-8
from PyQt5.QtWidgets import (QMainWindow,QApplication,QWidget,QPushButton,QLabel,QLineEdit,QTextBrowser,QGroupBox,QCheckBox)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThread

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon('qt.png'))
        self.setWindowTitle(u"Mod Application")
        self.setFixedSize(800, 600)
        self.setObjectName('principal')
        self.createGUI()

    def createGUI(self):
        self.frame_window = QWidget(self)
        self.frame_window.setGeometry(0, 0, 800, 40)
        self.frame_window.setObjectName('frame_window')
        self.title_frame = QLabel(self.frame_window)
        self.title_frame.setGeometry(0, 0, 800, 40)
        self.title_frame.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_frame.setFont(QFont("Tahoma", 20, QFont.Bold))
        self.title_frame.setText(u" Mod-Ali cloud white list setting")
        self.title_frame.setObjectName('title_frame')
        # buttons
        clsfont = self.font() or QFont()
        clsfont.setFamily('Webdings')
        self.button_close = QPushButton('r', self.frame_window, font=clsfont)
        self.button_close.setGeometry(760, 0, 40, 40)
        self.button_close.setObjectName('button_close')
        self.button_close.setToolTip(u'Exit')
        self.button_close.enterEvent(self.button_close.setCursor(Qt.PointingHandCursor))
        self.button_min = QPushButton('0', self.frame_window, font=clsfont)
        self.button_min.setGeometry(720, 0, 40, 40)
        self.button_min.setObjectName('button_min')
        self.button_min.setToolTip(u'Minimize')
        self.button_min.enterEvent(self.button_min.setCursor(Qt.PointingHandCursor))
        ###左边选择栏部分
        self.GroupBox_checkbox = QGroupBox(self)
        self.GroupBox_checkbox.setTitle(u'Select whitelist group')
        self.GroupBox_checkbox.setGeometry(10, 50, 200, 540)
        self.ecs_test = QCheckBox(u'Test Server', self.GroupBox_checkbox)
        self.ecs_test.enterEvent(self.ecs_test.setCursor(Qt.PointingHandCursor))
        self.ecs_test.setChecked(True)
        self.ecs_test.setGeometry(20, 30, 150, 30)
        self.rds_mysql = QCheckBox(u'MySQL Database', self.GroupBox_checkbox)
        self.rds_mysql.enterEvent(self.rds_mysql.setCursor(Qt.PointingHandCursor))
        self.rds_mysql.setChecked(True)
        self.rds_mysql.setGeometry(20, 60, 150, 30)
        self.rds_sqlserver = QCheckBox(u'MSSQL Database', self.GroupBox_checkbox)
        self.rds_sqlserver.enterEvent(self.rds_sqlserver.setCursor(Qt.PointingHandCursor))
        self.rds_sqlserver.setChecked(True)
        self.rds_sqlserver.setGeometry(20, 90, 150, 30)
        ###右边IP设置部分
        self.GroupBox_ipset = QGroupBox(self)
        self.GroupBox_ipset.setTitle(u'Public IP Set')
        self.GroupBox_ipset.setGeometry(220, 50, 570, 200)
        self.label_outip = QLabel(self.GroupBox_ipset, objectName="label_outip")
        self.label_outip.setText(u'Public IP:')
        self.label_outip.setGeometry(15, 30, 75, 30)
        self.line_outip = QLineEdit(self.GroupBox_ipset)
        self.line_outip.setMinimumWidth(200)
        self.line_outip.setGeometry(105, 30, 150, 30)
        self.line_outip.setFont(QFont("Timers", 13, QFont.Bold))
        self.line_outip.setStyleSheet("color:green")
        self.button_getip = QPushButton(u'Auto IP', self.GroupBox_ipset, objectName="button_getip")
        self.button_getip.setToolTip(u'Gripping the machine from the public IP network ip138')
        self.button_getip.enterEvent(self.button_getip.setCursor(Qt.PointingHandCursor))
        self.button_getip.setGeometry(315, 30, 110, 30)
        self.button_setup = QPushButton(u'ADD', self.GroupBox_ipset, objectName="button_setup")
        self.button_setup.enterEvent(self.button_setup.setCursor(Qt.PointingHandCursor))
        self.button_setup.setToolTip(u'Add IP to Group')
        self.button_setup.setGeometry(430, 30, 110, 30)
        ###右边消息输出部分
        self.GroupBox_text = QGroupBox(self)
        self.GroupBox_text.setGeometry(220, 260, 570, 330)
        self.browser_text = QTextBrowser(self.GroupBox_text)
        self.browser_text.setGeometry(0, 0, 570, 330)
        self.browser_text.setFont(QFont("Roman times", 12))
        self.browser_text.setObjectName('browser_text')

        # conexiones
        self.button_close.clicked.connect(self.close)
        self.button_min.clicked.connect(self.showMinimized)
        self.button_getip.clicked.connect(self.auto_ip)
        self.button_setup.clicked.connect(self.setup)

    def auto_ip(self):
        pass
    def show_ip_info(self,ip=None,status=1):
        pass
    def setup(self):
        pass
    def show_text(self,text=None, end=0):
        if end:
            self.button_setup.setEnabled(True)
        if text:
            self.browser_text.append(text)
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
    myapp = MainWindow()
    myapp.show()
    with open('main.css' , 'r') as css:
        StyleSheet = css.read()
    # app.setStyle("cleanlooks")
    app.setStyleSheet(StyleSheet)
    sys.exit(app.exec_())