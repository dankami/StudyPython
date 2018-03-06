# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
import pyqtgraph as pg
from CustomViewBox import CustomViewBox
from TimeAxisItem import TimeAxisItem

import datetime as dt
from pyqtgraph.Qt import QtCore
from pyqtgraph.Point import Point

class OIPlotItem(pg.PlotItem):
    def __init__(self):
        vb = CustomViewBox()
        # 设置横坐标
        xdict = {}
        self.m_timeAxis = TimeAxisItem(xdict, orientation='bottom')
        pg.PlotItem.__init__(self, viewBox=vb, name='PlotOI', axisItems={'bottom': self.m_timeAxis})

        # 属性设置
        self.setMenuEnabled(False)
        self.setClipToView(True)
        self.setDownsampling(mode='peak')
        self.setRange(xRange=(0, 1), yRange=(0, 1))
        self.showGrid(True, True)
        self.hideButtons()

        self.hideAxis('left')
        self.showAxis('right')
        self.getAxis('right').setWidth(60)
        self.getAxis('right').setStyle(tickFont=QFont("Roman times", 10, QFont.Bold))
        self.getAxis('right').setPen(color=(255, 255, 255, 255), width=0.8)

        # 组件及属性设置
        self.m_oiRect = self.sceneBoundingRect()
        self.m_oiVLine = pg.InfiniteLine(angle=90, movable=False)
        self.m_oiHLine = pg.InfiniteLine(angle=0, movable=False)
        self.m_oiTextPrice = pg.TextItem('', anchor=(1, 1))
        self.addItem(self.m_oiVLine)
        self.addItem(self.m_oiHLine)
        self.addItem(self.m_oiTextPrice)
        self.m_oiVLine.setPos(0)
        self.m_oiHLine.setPos(0)
        self.m_oiVLine.setZValue(0)
        self.m_oiHLine.setZValue(0)
        self.m_oiTextPrice.setZValue(2)

        # 字期组件
        self.m_textDate = pg.TextItem('date', anchor=(1, 1))
        self.m_textDate.setZValue(2)
        self.addItem(self.m_textDate, ignoreBounds=True)

        # 参数
        self.m_oiYAxis = 0
        self.m_oiLeftX = 0
        self.m_oiShowHLine = False
        self.m_xAxis = 0
        self.m_yAxis = 0

    # 移动
    def moveTo(self, xAxis, yAxis):
        xAxis, yAxis = (self.m_xAxis, self.m_yAxis) if xAxis is None else (int(xAxis), yAxis)
        self.m_oiRect = self.sceneBoundingRect()
        if not xAxis or not yAxis:
            return
        self.m_xAxis = xAxis
        self.m_yAxis = yAxis
        self.vhLinesSetXY(xAxis, yAxis)
        self.plotInfo(xAxis, yAxis)

    # ----------------------------------------------------------------------
    def vhLinesSetXY(self, xAxis, yAxis):
        """水平和竖线位置设置"""
        self.m_oiVLine.setPos(xAxis)
        if self.m_oiShowHLine:
            self.m_oiHLine.setPos(self.m_oiYAxis)
            self.m_oiHLine.show()
        else:
            self.m_oiHLine.hide()

    # ----------------------------------------------------------------------
    def plotInfo(self, _xAxis, _yAxis):
        if self.m_datas is None:
            return
        try:
            # 获取K线数据
            data = self.m_datas[_xAxis]
            tickDatetime = data['datetime']
        except Exception, e:
            return

        if (isinstance(tickDatetime, dt.datetime)):
            datetimeText = dt.datetime.strftime(tickDatetime, '%Y-%m-%d %H:%M:%S')
        else:
            datetimeText = ""

        self.m_textDate.setHtml(
            '<div style="text-align: center">\
                <span style="color: yellow; font-size: 20px; font-weight:bold">%s</span>\
            </div>' \
            % (datetimeText))

        oiRightAxisWidth = self.getAxis('right').width()
        oiBottomAxisHeight = self.getAxis('bottom').height()
        oiOffset = QtCore.QPointF(oiRightAxisWidth, oiBottomAxisHeight)
        oiBottomRigt = self.vb.mapSceneToView(self.m_oiRect.bottomRight() - oiOffset)

        # 修改对称方式防止遮挡
        midAxis = int(len(self.m_datas) / 2)
        self.m_textDate.anchor = Point((1, 1)) if _xAxis > midAxis else Point((0, 1))
        self.m_textDate.setPos(_xAxis, oiBottomRigt.y())

        if self.m_oiShowHLine:
            self.m_oiTextPrice.setHtml(
                '<div style="text-align: right">\
                     <span style="color: yellow; font-size: 20px;">\
                       %0.3f\
                     </span>\
                 </div>' \
                % (self.m_oiYAxis))
            self.m_oiTextPrice.setPos(oiBottomRigt.x(), self.m_oiYAxis)
            self.m_oiTextPrice.show()
        else:
            self.m_oiTextPrice.hide()

    # 更新时间轴
    def update_xdict(self, _xdict):
        self.m_timeAxis.update_xdict(_xdict)

    # 设置数据
    def setDatas(self, _datas):
        self.m_datas = _datas

    def setYAxis(self, _yAxis):
        self.m_oiYAxis = _yAxis

    def setShowHLine(self, _showHLine):
        self.m_oiShowHLine = _showHLine



