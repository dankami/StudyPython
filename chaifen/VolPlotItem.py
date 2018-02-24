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

        # 十字光标
        self.m_volYAxis = 0
        self.m_volShowHLine = False
        self.m_volTextPrice = pg.TextItem('', anchor=(1, 1))
        self.m_volVLine = pg.InfiniteLine(angle=90, movable=False)
        self.m_volHLine = pg.InfiniteLine(angle=0, movable=False)
        self.m_textVolume = pg.TextItem('lastBarVolume', anchor=(1, 0))
        self.m_textVolume.setZValue(2)

        self.m_volRect = self.m_volView.sceneBoundingRect()
        self.m_volTextPrice.setZValue(2)
        self.m_volVLine.setPos(0)
        self.m_volHLine.setPos(0)
        self.m_volVLine.setZValue(0)
        self.m_volHLine.setZValue(0)
        self.addItem(self.m_volVLine)
        self.addItem(self.m_volHLine)
        self.addItem(self.m_volTextPrice)
        self.addItem(self.m_textVolume, ignoreBounds=True)

    def setYAxis(self, _yAxis):
        self.m_oiYAxis = _yAxis

    def setShowHLine(self, _showHLine):
        self.m_oiShowHLine = _showHLine

    # 设置数据
    def setDatas(self, _datas):
        self.m_datas = _datas

    # 设置master
    def setMaster(self, _master):
        self.m_master = _master

    # ----------------------------------------------------------------------
    # def onMouseMoved(self, _evt):
    #     """鼠标移动回调"""
    #     pos = _evt[0]
    #     self.m_oiRect = self.sceneBoundingRect()
    #     self.m_oiShowHLine = False
    #     if self.m_oiRect.contains(pos):
    #         mousePoint = self.vb.mapSceneToView(pos)
    #         xAxis = mousePoint.x()
    #         yAxis = mousePoint.y()
    #         self.m_oiYAxis = yAxis
    #         self.m_oiShowHLine = True
    #         self.moveTo(xAxis, yAxis)

    # ----------------------------------------------------------------------
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

        # 显示所有的主图技术指标
        html = u'<div style="text-align: right">'
        for sig in self.m_master.m_subSigData:
            val = self.m_master.m_subSigData[sig][_xAxis]
            col = self.m_master.m_subSigColor[sig]
            html += u'<span style="color: %s;  font-size: 20px;">&nbsp;&nbsp;%s：%.2f</span>' % (col, sig, val)
        html += u'</div>'
        self.m_textSubSig.setHtml(html)

        self.m_textDate.setHtml(
            '<div style="text-align: center">\
                <span style="color: yellow; font-size: 20px;">%s</span>\
            </div>' \
            % (datetimeText))

        oiRightAxisWidth = self.getAxis('right').width()
        oiBottomAxisHeight = self.getAxis('bottom').height()
        oiOffset = QtCore.QPointF(oiRightAxisWidth, oiBottomAxisHeight)
        oiTopLeft = self.vb.mapSceneToView(self.m_oiRect.topLeft())
        oiBottomRigt = self.vb.mapSceneToView(self.m_oiRect.bottomRight() - oiOffset)

        # 修改对称方式防止遮挡
        self.m_textDate.anchor = Point((1, 1)) if _xAxis > self.m_master.m_index else Point((0, 1))
        self.m_textDate.setPos(_xAxis, oiBottomRigt.y())
        self.m_textSubSig.setPos(oiBottomRigt.x(), oiTopLeft.y())

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



