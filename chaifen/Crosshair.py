# encoding: UTF-8

import PyQt4
import pyqtgraph as pg
import datetime as dt

from pyqtgraph.Qt import QtCore

########################################################################
# 十字光标支持
########################################################################
class Crosshair(PyQt4.QtCore.QObject):
    """
    此类给pg.PlotWidget()添加crossHair功能,PlotWidget实例需要初始化时传入
    """
    # signal = QtCore.pyqtSignal(type(tuple([])))
    # signalInfo = QtCore.pyqtSignal(float, float)

    # ----------------------------------------------------------------------
    def __init__(self, _master):
        """Constructor"""
        self.m_master = _master
        super(Crosshair, self).__init__()





    # 设置数据
    # def setDatas(self, _datas):
    #     self.m_datas = _datas
    #
    # # 设置UI
    # def setklView(self, _view):
    #     self.m_klView = _view
    #


    # def setYAxis(self, _index, _yAxis):
    #     self.m_yAxises[_index] = _yAxis
    #
    # def setShowHLine(self, _index, _showHLine):
    #     self.m_showHLine[_index] = _showHLine

    # ----------------------------------------------------------------------
    # def moveTo(self, _xAxis, _yAxis):



