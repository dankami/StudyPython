# -*- coding: utf-8 -*-
"""
Python K线模块,包含十字光标和鼠标键盘交互
Support By 量投科技(http://www.quantdo.com.cn/)
"""

import tushare as ts
# Qt相关和十字光标
from PyQt4.QtGui import QApplication
from PyQt4 import QtCore
# 其他
import pandas as pd
from KLineWidget import KLineWidget

# 字符串转换
# ---------------------------------------------------------------------------------------
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


########################################################################
# 功能测试
########################################################################
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 界面设置
    cfgfile = QtCore.QFile('css.qss')
    cfgfile.open(QtCore.QFile.ReadOnly)
    styleSheet = cfgfile.readAll()
    styleSheet = unicode(styleSheet, encoding='utf8')
    app.setStyleSheet(styleSheet)
    # K线界面
    ui = KLineWidget()
    ui.setGeometry(100, 100, 1280, 720)
    ui.show()
    kData = pd.DataFrame.from_csv('data.csv')
    ui.loadData(kData)
    app.exec_()
