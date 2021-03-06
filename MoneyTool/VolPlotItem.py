# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
import pyqtgraph as pg
from CustomViewBox import CustomViewBox
from CandlestickItem import CandlestickItem
from TimeAxisItem import TimeAxisItem
import datetime as dt
from pyqtgraph.Point import Point

from pyqtgraph.Qt import QtCore

class VolPlotItem(pg.PlotItem):
    def __init__(self):
        vb = CustomViewBox()
        self.m_timeAxis = TimeAxisItem({}, orientation='bottom')
        pg.PlotItem.__init__(self, viewBox=vb, name='PlotVol', axisItems={'bottom': self.m_timeAxis})

        # 属性设置
        self.setMenuEnabled(False)
        self.setClipToView(True)
        self.showGrid(True, True)
        self.setDownsampling(mode='peak')
        self.hideButtons()
        self.setRange(xRange=(0, 1), yRange=(0, 1))
        self.setMaximumHeight(200)
        self.setXLink('PlotOI')

        self.hideAxis('left')
        self.showAxis('right')
        # self.hideAxis('bottom')
        self.getAxis('right').setWidth(60)
        self.getAxis('right').setStyle(tickFont=QFont("Roman times", 10, QFont.Bold))
        self.getAxis('right').setPen(color=(255, 255, 255, 255), width=0.8)

        # 添加子组件及设置
        self.m_candle = CandlestickItem()
        self.m_volVLine = pg.InfiniteLine(angle=90, movable=False)
        self.m_volHLine = pg.InfiniteLine(angle=0, movable=False)
        self.m_volTextPrice = pg.TextItem('', anchor=(1, 1))
        self.m_textVolume = pg.TextItem('lastBarVolume', anchor=(1, 0))
        self.addItem(self.m_candle)
        self.addItem(self.m_volVLine)
        self.addItem(self.m_volHLine)
        self.addItem(self.m_volTextPrice)
        self.addItem(self.m_textVolume, ignoreBounds=True)

        self.m_volVLine.setPos(0)
        self.m_volHLine.setPos(0)
        self.m_volVLine.setZValue(0)
        self.m_volHLine.setZValue(0)
        self.m_volTextPrice.setZValue(2)
        self.m_textVolume.setZValue(2)

        # 字期组件
        self.m_textDate = pg.TextItem('date', anchor=(1, 1))
        self.m_textDate.setZValue(2)
        self.addItem(self.m_textDate, ignoreBounds=True)

        self.m_volYAxis = 0
        self.m_volShowHLine = False
        self.m_xAxis = 0
        self.m_yAxis = 0

    # 刷新K线
    def updateCandle(self, _data=None, _redraw=False):
        self.m_candle.generatePicture(_data, _redraw)

    # 移动
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
            tickDatetime = data['date']
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

        # 十字标时间
        if (isinstance(tickDatetime, dt.datetime)):
            dateText = dt.datetime.strftime(tickDatetime, '%Y-%m-%d')
        else:
            dateText = ""
        self.m_textDate.setHtml(
            '<div style="text-align: center">\
                <span style="color: yellow; font-size: 20px; font-weight:bold">%s</span>\
            </div>' \
            % (dateText))

        oiRightAxisWidth = self.getAxis('right').width()
        oiBottomAxisHeight = self.getAxis('bottom').height()
        oiOffset = QtCore.QPointF(oiRightAxisWidth, oiBottomAxisHeight)
        oiBottomRigt = self.vb.mapSceneToView(self.m_volRect.bottomRight() - oiOffset)

        # 修改对称方式防止遮挡
        midAxis = int(len(self.m_datas) / 2)
        self.m_textDate.anchor = Point((1, 1)) if _xAxis > midAxis else Point((0, 1))
        self.m_textDate.setPos(_xAxis, oiBottomRigt.y())

    # 更新时间轴
    def update_xdict(self, _xdict):
        self.m_timeAxis.update_xdict(_xdict)

    # 设置数据
    def setDatas(self, _datas):
        self.m_datas = _datas

    def setYAxis(self, _yAxis):
        self.m_volYAxis = _yAxis

    def setShowHLine(self, _showHLine):
        self.m_volShowHLine = _showHLine



