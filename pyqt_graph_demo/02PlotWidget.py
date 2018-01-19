# -*- coding: utf-8 -*-
"""
Demonstrates use of PlotWidget class. This is little more than a
GraphicsView with a PlotItem placed in its center.
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys

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
    curve = plotWidget.plot(data2, clickable=False)

    curve.setPen('w')  # white pen

    mainWin.show()


    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()