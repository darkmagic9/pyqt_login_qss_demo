#!/usr/bin/env python
# -*- coding: utf-8
from PyQt4.QtGui import QApplication
from login import Login
from Main import MainWindow
from PyQt4.QtGui import QDialog
if __name__ == '__main__':
    import sys
    from PyQt4.QtCore import QFile, QIODevice, QTextStream, QTextCodec
    import myfile
    cssfile = QFile(':/main.css')
    if not cssfile.open(QIODevice.ReadOnly):
        sys.exit(u'未读取到资源文件')
    stream = QTextStream(cssfile)
    stream.setCodec(QTextCodec.codecForName('UTF-8'))
    cssdata = stream.readAll()
    cssfile.close()
    del stream
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # with open('main.css', 'r') as css:
    #     StyleSheet = css.read()
    app.setStyleSheet(cssdata)
    if Login().exec_() == QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())