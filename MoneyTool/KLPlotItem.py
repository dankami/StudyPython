# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
import pyqtgraph as pg
from CustomViewBox import CustomViewBox
from CandlestickItem import CandlestickItem

import datetime as dt
from pyqtgraph.Qt import QtCore

class KLPlotItem(pg.PlotItem):
    def __init__(self):
        vb = CustomViewBox()
        pg.PlotItem.__init__(self, viewBox=vb, name='PlotKL')

        # 属性设置
        self.setMenuEnabled(False)
        self.setClipToView(True)
        self.showGrid(True, True)
        self.setDownsampling(mode='peak')
        self.hideButtons()
        self.setRange(xRange=(0, 1), yRange=(0, 1))
        self.setXLink('PlotOI')

        self.hideAxis('left')
        self.hideAxis('bottom')
        self.showAxis('right')
        self.getAxis('right').setWidth(60)
        self.getAxis('right').setStyle(tickFont=QFont("Roman times", 10, QFont.Bold))
        self.getAxis('right').setPen(color=(255, 255, 255, 255), width=0.8)

        # 添加子组件及设置
        self.m_candle = CandlestickItem() # K线图组件
        self.m_klTextPrice = pg.TextItem('', anchor=(1, 1)) # 十字光标相关
        self.m_klVLine = pg.InfiniteLine(angle=90, movable=False)
        self.m_klHLine = pg.InfiniteLine(angle=0, movable=False)
        self.m_textInfo = pg.TextItem('lastBarInfo') # K线数据显示
        self.addItem(self.m_candle)
        self.addItem(self.m_klTextPrice)
        self.addItem(self.m_klVLine)
        self.addItem(self.m_klHLine)
        self.addItem(self.m_textInfo, ignoreBounds=True)
        self.m_klTextPrice.setZValue(2)
        self.m_klVLine.setZValue(0)
        self.m_klHLine.setZValue(0)
        self.m_klVLine.setPos(0)
        self.m_klHLine.setPos(0)
        self.m_textInfo.setZValue(2)
        self.m_textInfo.border = pg.mkPen(color=(230, 255, 0, 255), width=1.2)

        # 数据
        self.m_xAxis = 0
        self.m_yAxis = 0
        self.m_datas = None
        self.m_klYAxise = 0
        self.m_klShowHLine = False
        self.m_klRect = self.sceneBoundingRect()

    # 刷新K线
    def updateCandle(self, _data=None, _redraw=False):
        self.m_candle.generatePicture(_data, _redraw)

    # 移动
    def moveTo(self, _xAxis, _yAxis):

        _xAxis = self.m_xAxis if _xAxis is None else int(_xAxis)
        _yAxis = self.m_yAxis if _yAxis is None else int(_yAxis)

        self.m_klRect = self.sceneBoundingRect()

        self.m_xAxis = _xAxis
        self.m_yAxis = _yAxis

        self.m_klVLine.setPos(_xAxis)
        if self.m_klShowHLine:
            self.m_klHLine.setPos(_yAxis)
            self.m_klHLine.show()
        else:
            self.m_klHLine.hide()

        if self.m_datas is None:
            return
        try:
            # 获取K线数据
            data = self.m_datas[_xAxis]
            lastdata = self.m_datas[_xAxis - 1]
            tickDate = data['date']
            openPrice = data['open']
            closePrice = data['close']
            lowPrice = data['low']
            highPrice = data['high']
            volume = data['volume']
            preClosePrice = lastdata['close']
        except Exception, e:
            return

        if (isinstance(tickDate, dt.datetime)):
            dateText = dt.datetime.strftime(tickDate, '%Y-%m-%d')
        else:
            dateText = ""

        # 和上一个收盘价比较，决定K线信息的字符颜色
        cOpen = 'red' if openPrice > preClosePrice else 'green'
        cClose = 'red' if closePrice > preClosePrice else 'green'
        cHigh = 'red' if highPrice > preClosePrice else 'green'
        cLow = 'red' if lowPrice > preClosePrice else 'green'

        self.m_textInfo.setHtml(
            u'<div style="text-align: center; background-color:#000">\
                <span style="color: white;  font-size: 16px;">日期</span><br>\
                <span style="color: yellow; font-size: 16px;">%s</span><br>\
                <span style="color: white;  font-size: 16px;">开盘</span><br>\
                <span style="color: %s;     font-size: 16px;">%.3f</span><br>\
                <span style="color: white;  font-size: 16px;">最高</span><br>\
                <span style="color: %s;     font-size: 16px;">%.3f</span><br>\
                <span style="color: white;  font-size: 16px;">最低</span><br>\
                <span style="color: %s;     font-size: 16px;">%.3f</span><br>\
                <span style="color: white;  font-size: 16px;">收盘</span><br>\
                <span style="color: %s;     font-size: 16px;">%.3f</span><br>\
                <span style="color: white;  font-size: 16px;">成交量</span><br>\
                <span style="color: yellow; font-size: 16px;">%.3f</span><br>\
            </div>' \
            % (dateText, cOpen, openPrice, cHigh, highPrice, \
               cLow, lowPrice, cClose, closePrice, volume))

        # 坐标轴宽度
        klRightAxisWidth = self.getAxis('right').width()
        klBottomAxisHeight = 20  # self.m_oiView.getAxis('bottom').height()
        klOffset = QtCore.QPointF(klRightAxisWidth, klBottomAxisHeight)

        # 各个顶点
        klTopLeft = self.vb.mapSceneToView(self.m_klRect.topLeft())
        klBottomRight = self.vb.mapSceneToView(self.m_klRect.bottomRight() - klOffset)

        # 显示价格
        if self.m_klShowHLine:
            self.m_klTextPrice.setHtml(
                '<div style="text-align: right">\
                     <span style="color: yellow; font-size: 20px;">\
                       %0.3f\
                     </span>\
                 </div>' \
                % (_yAxis))
            self.m_klTextPrice.setPos(klBottomRight.x(), _yAxis)
            self.m_klTextPrice.show()
        else:
            self.m_klTextPrice.hide()

        # 设置坐标
        self.m_textInfo.setPos(klTopLeft)

    # 设置数据
    def setDatas(self, _datas):
        self.m_datas = _datas

    def setYAxis(self, _yAxis):
        self.m_volYAxis = _yAxis

    def setShowHLine(self, _showHLine):
        self.m_klShowHLine = _showHLine

    # 获取横坐标
    def getXAxis(self):
        return self.m_xAxis




