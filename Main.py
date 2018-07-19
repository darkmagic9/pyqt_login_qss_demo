#!/usr/bin/env python
# -*- coding: utf-8
from PyQt4.QtGui import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QFont,
    QGroupBox,
    QCheckBox,
    QLineEdit,
    QTextBrowser,
)
from PyQt4.QtCore import Qt, QThread, pyqtSignal
from PyQt4.QtGui import QApplication
import httplib, re, datetime, time
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import (
    DescribeSecurityGroupsRequest,
    DescribeSecurityGroupAttributeRequest,
    AuthorizeSecurityGroupRequest,
    RevokeSecurityGroupRequest)
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceIPArrayListRequest
from aliyunsdkrds.request.v20140815 import ModifySecurityIpsRequest

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(u"鱿鱼")
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
        self.title_frame.setFont(QFont("微软雅黑", 20, QFont.Bold))
        self.title_frame.setText(u" 鱿鱼-阿里云白名单设置")
        self.title_frame.setObjectName('title_frame')
        # buttons
        clsfont = self.font() or QFont()
        clsfont.setFamily('Webdings')
        self.button_close = QPushButton('r', self.frame_window, font=clsfont)
        self.button_close.setGeometry(760, 0, 40, 40)
        self.button_close.setObjectName('button_close')
        self.button_close.setToolTip(u'关闭')
        self.button_close.enterEvent(self.button_close.setCursor(Qt.PointingHandCursor))
        self.button_min = QPushButton('0', self.frame_window, font=clsfont)
        self.button_min.setGeometry(720, 0, 40, 40)
        self.button_min.setObjectName('button_min')
        self.button_min.setToolTip(u'最小化')
        self.button_min.enterEvent(self.button_min.setCursor(Qt.PointingHandCursor))
        ###左边选择栏部分
        self.GroupBox_checkbox = QGroupBox(self)
        self.GroupBox_checkbox.setTitle(u'选择白名单组')
        self.GroupBox_checkbox.setGeometry(10, 50, 200, 540)
        self.ecs_test = QCheckBox(u'测试环境服务器', self.GroupBox_checkbox)
        self.ecs_test.enterEvent(self.ecs_test.setCursor(Qt.PointingHandCursor))
        self.ecs_test.setChecked(True)
        self.ecs_test.setGeometry(20, 30, 150, 30)
        self.rds_mysql = QCheckBox(u'MySQL数据库', self.GroupBox_checkbox)
        self.rds_mysql.enterEvent(self.rds_mysql.setCursor(Qt.PointingHandCursor))
        self.rds_mysql.setChecked(True)
        self.rds_mysql.setGeometry(20, 60, 150, 30)
        self.rds_sqlserver = QCheckBox(u'SQLServer数据库', self.GroupBox_checkbox)
        self.rds_sqlserver.enterEvent(self.rds_sqlserver.setCursor(Qt.PointingHandCursor))
        self.rds_sqlserver.setChecked(True)
        self.rds_sqlserver.setGeometry(20, 90, 150, 30)
        ###右边IP设置部分
        self.GroupBox_ipset = QGroupBox(self)
        self.GroupBox_ipset.setTitle(u'公网IP配置')
        self.GroupBox_ipset.setGeometry(220, 50, 570, 200)
        self.label_outip = QLabel(self.GroupBox_ipset, objectName="label_outip")
        self.label_outip.setText(u'公网IP:')
        self.label_outip.setGeometry(15, 30, 75, 30)
        self.line_outip = QLineEdit(self.GroupBox_ipset)
        self.line_outip.setMinimumWidth(200)
        self.line_outip.setGeometry(85, 30, 150, 30)
        self.line_outip.setFont(QFont("Timers", 13, QFont.Bold))
        self.line_outip.setStyleSheet("color:green")
        self.button_getip = QPushButton(u'自动获取公网IP', self.GroupBox_ipset, objectName="button_getip")
        self.button_getip.setToolTip(u'从ip138上抓取本机公网IP')
        self.button_getip.enterEvent(self.button_getip.setCursor(Qt.PointingHandCursor))
        self.button_getip.setGeometry(300, 30, 110, 30)
        self.button_setup = QPushButton(u'添加', self.GroupBox_ipset, objectName="button_setup")
        self.button_setup.enterEvent(self.button_setup.setCursor(Qt.PointingHandCursor))
        self.button_setup.setToolTip(u'将该IP添加至已选白名单组中')
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
        self.line_outip.clear()
        self.button_getip.setEnabled(False)
        self.th_get_ip = GETIP()
        self.th_get_ip.ip_line_Signal.connect(self.show_ip_info)
        self.th_get_ip.start()
    def show_ip_info(self,ip=None,status=1):
        self.button_getip.setEnabled(True)
        if status:
            self.line_outip.setText(ip)
        else:
            self.browser_text.append(ip)
    def setup(self):
        myip = self.line_outip.text()
        if myip and validate_ip(myip):
            check_list = []
            if self.ecs_test.isChecked():
                check_list.append('ecs_test')
            if self.rds_mysql.isChecked():
                check_list.append('rds_mysql')
            if self.rds_sqlserver.isChecked():
                check_list.append('rds_sqlserver')
            if len(check_list) == 0:
                self.browser_text.append(u'没什么事可做的~')
            else:
                self.button_setup.setEnabled(False)
                self.th_setup = SETIP(myip, check_list)
                self.th_setup.text_browser_Signal.connect(self.show_text)
                self.th_setup.start()
        else:
            self.browser_text.append(u'请填入正确的IP地址！')
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

class GETIP(QThread):
    ip_line_Signal = pyqtSignal(str,int)
    def __init__(self, parent=None):
        super(GETIP,self).__init__(parent)
    def run(self):
        try:
            ip = get_out_ip()
            if ip:
                self.ip_line_Signal.emit(ip,1)
            else:
                self.ip_line_Signal.emit(u'未能获取到外网IP',0)
        except Exception as e:
            # print(e)
            self.ip_line_Signal.emit(u'内部错误: '+e,0)
class SETIP(QThread):
    text_browser_Signal = pyqtSignal(str,int)
    def __init__(self, ip, check_list, parent=None):
        super(SETIP,self).__init__(parent)
        self.ip = ip
        self.check_list = check_list
    def run(self):
        for ch in self.check_list:
            try:
                if ch == 'ecs_test':
                    sg = ECS_SG(AccessKey="123", AccessSecret="abc",
                            RegionId="cn-hangzhou")
                    clt = sg.clt()
                    request1 = sg.describeSecurityGroupAttributeRequest(SecurityGroupId='456',
                                                                        NicType='intranet', Direction='all')
                    response1 = clt.do_action_with_exception(request1)
                    if str(self.ip) in response1:
                        self.text_browser_Signal.emit(u'该IP:{0}已经存在ECS安全组中'.format(self.ip), 0)
                    else:
                        SourceIp = str(self.ip) + '/22'
                        request2 = sg.authorizeSecurityGroupRequest(SecurityGroupId='456',
                                                                    IpProtocol='all',
                                                                    PortRange='-1/-1', SourceCidrIp=SourceIp,
                                                                    NicType='intranet',
                                                                    Policy='accept', Priority='1',
                                                                    Description='auto add')
                        response2 = clt.do_action_with_exception(request2)
                        self.text_browser_Signal.emit(u'已将{0}添加至ECS安全组'.format(self.ip), 0)
                elif ch == 'rds_mysql':
                    rdswi = RDS_WhiteIP(AccessKey="123", AccessSecret="abc",
                                        RegionId="cn-hangzhou")
                    clt = rdswi.clt()
                    request1 = rdswi.describeDBInstanceIPArrayListRequest(DBInstanceId='456')
                    response1 = clt.do_action_with_exception(request1)
                    if str(self.ip) in response1:
                        self.text_browser_Signal.emit(u'该IP:{0}已经存在RDS_MySQL白名单中'.format(self.ip), 0)
                    else:
                        request2 = rdswi.modifySecurityIpsRequest(DBInstanceId='456',
                                                                  DBInstanceIPArrayName='ops',
                                                                  SecurityIps=str(self.ip), ModifyMode='Append')
                        response2 = clt.do_action_with_exception(request2)
                        self.text_browser_Signal.emit(u'已将{0}添加至RDS_MySQL白名单中'.format(self.ip), 0)
                elif ch == 'rds_sqlserver':
                    rdswi = RDS_WhiteIP(AccessKey="123", AccessSecret="abc",
                                       RegionId="cn-hangzhou")
                    clt = rdswi.clt()
                    request1 = rdswi.describeDBInstanceIPArrayListRequest(DBInstanceId='456')
                    response1 = clt.do_action_with_exception(request1)
                    if str(self.ip) in response1:
                        self.text_browser_Signal.emit(u'该IP:{0}已经存在RDS_MySQL白名单中'.format(self.ip), 0)
                    else:
                        request2 = rdswi.modifySecurityIpsRequest(DBInstanceId='456',
                                                                  DBInstanceIPArrayName='ops',
                                                                  SecurityIps=str(self.ip), ModifyMode='Append')
                        response2 = clt.do_action_with_exception(request2)
                        self.text_browser_Signal.emit(u'已将{0}添加至RDS_SQLServer白名单中'.format(self.ip), 0)

            except Exception as e:
                # print(e)
                self.text_browser_Signal.emit(u'内部错误: '+e, 0)
        self.text_browser_Signal.emit(u'处理完毕。', 1)
class ECS_SG:
    def __init__(self, AccessKey, AccessSecret, RegionId):
        '''连接参数
            RegionId: cn-qingdao/cn-beijing/cn-zhangjiakou/cn-huhehaote/cn-hangzhou/cn-shanghai/cn-shenzhen
        '''
        #
        self.AccessKey = AccessKey
        self.AccessSecret = AccessSecret
        self.RegionId = RegionId

    def clt(self):
        '''创建连接
        '''
        return AcsClient(self.AccessKey, self.AccessSecret, self.RegionId)
    def describeSecurityGroupsRequest(self):
        '''查询您创建的安全组的基本信息，例如安全组 ID 和安全组描述等。返回列表按照安全组 ID 降序排列.
        '''
        request = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
        request.set_PageNumber(1)
        request.set_PageSize(50)
        request.set_accept_format('json')
        return request

    def describeSecurityGroupAttributeRequest(self, SecurityGroupId, NicType='intranet', Direction='all'):
        '''查询某个安全组详情
        '''
        request = DescribeSecurityGroupAttributeRequest.DescribeSecurityGroupAttributeRequest()
        request.set_SecurityGroupId(SecurityGroupId)
        request.set_NicType(NicType)
        request.set_Direction(Direction)
        request.set_accept_format('json')
        return request

    def authorizeSecurityGroupRequest(self, SecurityGroupId, IpProtocol, PortRange, SourceCidrIp, NicType='internet', Policy='accept', Priority='1', Description=None):
        """增加一条安全组入方向规则
        """
        request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        request.set_SecurityGroupId(SecurityGroupId)
        request.set_NicType(NicType)
        request.set_IpProtocol(IpProtocol)
        request.set_PortRange(PortRange)
        request.set_SourceCidrIp(SourceCidrIp)
        request.set_Policy(Policy)
        request.set_Priority(Priority)
        request.set_Description(Description)
        request.set_accept_format('json')
        return request

    def revokeSecurityGroupRequest(self, SecurityGroupId, IpProtocol, PortRange, NicType='internet', Policy='accept', Priority='1'):
        '''删除一条安全组入方向规则
        '''
        request = RevokeSecurityGroupRequest.RevokeSecurityGroupRequest()
        request.set_SecurityGroupId(SecurityGroupId)
        request.set_NicType(NicType)
        request.set_IpProtocol(IpProtocol)
        request.set_PortRange(PortRange)
        request.set_Policy(Policy)
        request.set_Priority(Priority)
        request.set_accept_format('json')
        return request
class RDS_WhiteIP:
    def __init__(self, AccessKey, AccessSecret, RegionId):
        '''连接参数
            RegionId: cn-qingdao/cn-beijing/cn-zhangjiakou/cn-huhehaote/cn-hangzhou/cn-shanghai/cn-shenzhen
        '''
        self.AccessKey = AccessKey
        self.AccessSecret = AccessSecret
        self.RegionId = RegionId

    def clt(self):
        '''创建连接
        '''
        return AcsClient(self.AccessKey, self.AccessSecret, self.RegionId)

    def describeDBInstanceIPArrayListRequest(self,DBInstanceId):
        '''查询实例白名单.
        '''
        request = DescribeDBInstanceIPArrayListRequest.DescribeDBInstanceIPArrayListRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_accept_format('json')
        return request

    def modifySecurityIpsRequest(self,DBInstanceId,DBInstanceIPArrayName='ops',SecurityIps=None,ModifyMode='Append'):
        '''
        修改ip白名单
        '''
        request = ModifySecurityIpsRequest.ModifySecurityIpsRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_DBInstanceIPArrayName(DBInstanceIPArrayName)
        request.set_SecurityIps(SecurityIps)
        request.set_ModifyMode(ModifyMode)
        request.set_accept_format('json')
        return request
def get_out_ip():
    try:
        import datetime
        host = '{0}.ip138.com'.format(datetime.datetime.now().year)
        http = httplib.HTTPConnection(host, timeout=5)
        http.request('GET', '/ic.asp')
        response = http.getresponse()
        # print(response.status)
        out = response.read()
        regex = re.compile(
            ur"((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))",
            re.M | re.S | re.I)
        ip = re.search(regex, out).group(0)
        # print ip
        # time.sleep(3)
        return ip
    except Exception as e:
        print(e)
        return None
    finally:
        if http:
            http.close()
def validate_ip(ip_str):
    sep = ip_str.split('.')
    if len(sep) != 4:
        return False
    for i,x in enumerate(sep):
        try:
            int_x = int(x)
            if int_x < 0 or int_x > 255:
                return False
        except ValueError, e:
            return False
    return True

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