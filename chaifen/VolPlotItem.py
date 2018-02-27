# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
import pyqtgraph as pg
from CustomViewBox import CustomViewBox
from TimeAxisItem import TimeAxisItem

import datetime as dt
from pyqtgraph.Qt import QtCore
from pyqtgraph.Point import Point

class VolPlotItem(pg.PlotItem):
    def __init__(self):
        vb = CustomViewBox()
        # 设置横坐标
        xdict = {}
        self.m_timeAxis = TimeAxisItem(xdict, orientation='bottom')
        pg.PlotItem.__init__(self, viewBox=vb, name='PlotVol', axisItems={'bottom': self.m_timeAxis})
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

        # 十字光标
        self.m_volYAxis = 0
        self.m_volShowHLine = False
        self.m_volTextPrice = pg.TextItem('', anchor=(1, 1))
        self.m_volVLine = pg.InfiniteLine(angle=90, movable=False)
        self.m_volHLine = pg.InfiniteLine(angle=0, movable=False)
        self.m_textVolume = pg.TextItem('lastBarVolume', anchor=(1, 0))
        self.m_textVolume.setZValue(2)

        self.m_volTextPrice.setZValue(2)
        self.m_volVLine.setPos(0)
        self.m_volHLine.setPos(0)
        self.m_volVLine.setZValue(0)
        self.m_volHLine.setZValue(0)
        self.addItem(self.m_volVLine)
        self.addItem(self.m_volHLine)
        self.addItem(self.m_volTextPrice)
        self.addItem(self.m_textVolume, ignoreBounds=True)

        self.m_xAxis = 0
        self.m_yAxis = 0

    def setYAxis(self, _yAxis):
        self.m_volYAxis = _yAxis

    def setShowHLine(self, _showHLine):
        self.m_volShowHLine = _showHLine

    # 设置数据
    def setDatas(self, _datas):
        self.m_datas = _datas

    # 设置master
    def setMaster(self, _master):
        self.m_master = _master


    # ----------------------------------------------------------------------
    def moveTo(self, _xAxis, _yAxis):

        _xAxis = self.m_xAxis if _xAxis is None else int(_xAxis)
        _yAxis = self.m_yAxis if _yAxis is None else int(_yAxis)

        self.m_volRect = self.sceneBoundingRect()

        self.m_xAxis = _xAxis
        self.m_yAxis = _yAxis


        self.m_volVLine.setPos(_xAxis)
        if self.m_volShowHLine:
            self.m_volHLine.setPos(self.m_volYAxis)
            self.m_volHLine.show()
        else:
            self.m_volHLine.hide()


        # vol相关
        if self.m_datas is None:
            return
        try:
            # 获取K线数据
            data = self.m_datas[_xAxis]
            volume = data['volume']
        except Exception, e:
            return

        self.m_textVolume.setHtml(
            '<div style="text-align: right">\
                <span style="color: white; font-size: 20px;">VOL : %.3f</span>\
            </div>' \
            % (volume))

        volRightAxisWidth = self.getAxis('right').width()
        volBottomAxisHeight = 20  # self.m_oiView.getAxis('bottom').height()
        volOffset = QtCore.QPointF(volRightAxisWidth, volBottomAxisHeight)
        volTopLeft = self.vb.mapSceneToView(self.m_volRect.topLeft())
        volBottomRight = self.vb.mapSceneToView(self.m_volRect.bottomRight() - volOffset)
        self.m_textVolume.setPos(volBottomRight.x(), volTopLeft.y())


        if self.m_volShowHLine:
            self.m_volTextPrice.setHtml(
                '<div style="text-align: right">\
                     <span style="color: yellow; font-size: 20px;">\
                       %0.3f\
                     </span>\
                 </div>' \
                % (self.m_volYAxis) )
            self.m_volTextPrice.setPos(volBottomRight.x(), self.m_volYAxis)
            self.m_volTextPrice.show()
        else:
            self.m_volTextPrice.hide()

    # 更新时间轴
    def update_xdict(self, _xdict):
        self.m_timeAxis.update_xdict(_xdict)



