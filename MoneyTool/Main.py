# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtGui import *
import pandas as pd
from KLineWidget import KLineWidget

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
    ui.resize(1280, 720)
    ui.show()
    # ui.m_pgTitle.setText('rb1701', size='20pt')
    ui.loadData(pd.DataFrame.from_csv('data2.csv'))
    app.exec_()