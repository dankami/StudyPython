# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
import pyqtgraph as pg
from CustomViewBox import CustomViewBox
from TimeAxisItem import TimeAxisItem

class OIPlotItem(pg.PlotItem):
    def __init__(self):
        vb = CustomViewBox()
        # 设置横坐标
        xdict = {}
        self.m_timeAxis = TimeAxisItem(xdict, orientation='bottom')
        pg.PlotItem.__init__(self, viewBox=vb, name='PlotOI', axisItems={'bottom': self.m_timeAxis})
        self.setMenuEnabled(False)
        self.setClipToView(True)
        self.hideAxis('left')
        self.showAxis('right')
        self.setDownsampling(mode='peak')
        self.setRange(xRange=(0, 1), yRange=(0, 1))
        self.getAxis('right').setWidth(60)
        self.getAxis('right').setStyle(tickFont=QFont("Roman times", 10, QFont.Bold))
        self.getAxis('right').setPen(color=(255, 255, 255, 255), width=0.8)
        self.showGrid(True, True)
        self.hideButtons()

    def update_xdict(self, _xdict):
        self.m_timeAxis.update_xdict(_xdict)