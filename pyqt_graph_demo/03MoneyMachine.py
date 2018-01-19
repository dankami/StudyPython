# -*- coding: utf-8 -*-
"""
终于入门了python绘表，开始分析赚钱了
"""
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys
import tushare as ts

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':

    # QtGui.QApplication.setGraphicsSystem('raster')
    app = QtGui.QApplication([])

    mainWin = QtGui.QMainWindow()       #主窗口
    centerWidget = QtGui.QWidget()      #中心组件
    boxLayout = QtGui.QVBoxLayout()     #中心组件布局
    plotWidget = pg.PlotWidget()        #pg组件

    mainWin.setWindowTitle('pyqtgraph example: PlotWidget')
    mainWin.resize(800, 800)
    mainWin.setCentralWidget(centerWidget)
    centerWidget.setLayout(boxLayout)
    boxLayout.addWidget(plotWidget)

    plotWidget.setLabel('left', 'Value', units='我是y轴')
    plotWidget.setLabel('bottom', 'Time', units='我是x轴')
    plotWidget.setXRange(10, 11)
    plotWidget.setYRange(10, 12)

    data1 = np.random.normal(size=100) # 随机数据
    data2 = np.array([11, 12, 13, 14])
    webData = ts.get_hist_data('600036', start='2017-12-01',end='2018-01-18')
    print webData

    # webData.index.name = "hello"  # 修改 index命名
    # print webData.loc[webData.index[1:3]] # 打印多行
    npOpen = webData.open
    npOpen = npOpen.sort_index(ascending=True)
    npClose = webData.close
    npClose = npClose.sort_index(ascending=True)

    lineOpen = plotWidget.plot(npOpen, clickable=False)
    lineOpen.setPen('w')  # white pen
    lineClose = plotWidget.plot(npClose, clickable=False)
    lineClose.setPen('r')

    mainWin.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()