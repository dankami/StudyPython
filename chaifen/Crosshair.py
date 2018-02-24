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
    signal = QtCore.pyqtSignal(type(tuple([])))
    signalInfo = QtCore.pyqtSignal(float, float)

    # ----------------------------------------------------------------------
    def __init__(self, _master):
        """Constructor"""
        self.m_master = _master
        super(Crosshair, self).__init__()

        self.m_xAxis = 0
        self.m_yAxis = 0

        self.m_datas = None

        self.m_yAxises = [0 for i in range(1)]
        self.m_showHLine = [False for i in range(1)]
        self.m_textPrices = [pg.TextItem('', anchor=(1, 1)) for i in range(1)]
        self.m_vLines = [pg.InfiniteLine(angle=90, movable=False) for i in range(1)]
        self.m_hLines = [pg.InfiniteLine(angle=0, movable=False) for i in range(1)]

        # mid 在y轴动态跟随最新价显示最新价和最新时间
        self.m_textInfo = pg.TextItem('lastBarInfo')
        self.m_textSig = pg.TextItem('lastSigInfo', anchor=(1, 0))

        self.m_textInfo.setZValue(2)
        self.m_textSig.setZValue(2)
        self.m_textInfo.border = pg.mkPen(color=(230, 255, 0, 255), width=1.2)

        # vol相关
        self.m_volYAxis = 0
        self.m_volShowHLine = False
        self.m_volTextPrice = pg.TextItem('', anchor=(1, 1))
        self.m_volVLine = pg.InfiniteLine(angle=90, movable=False)
        self.m_volHLine = pg.InfiniteLine(angle=0, movable=False)
        self.m_textVolume = pg.TextItem('lastBarVolume', anchor=(1, 0))
        self.m_textVolume.setZValue(2)

    # 设置数据
    def setDatas(self, _datas):
        self.m_datas = _datas

    # 设置UI
    def setViews(self, _views):
        self.m_views = _views
        self.m_rects = [self.m_views[i].sceneBoundingRect() for i in range(1)]
        for i in range(1):
            self.m_textPrices[i].setZValue(2)
            self.m_vLines[i].setPos(0)
            self.m_hLines[i].setPos(0)
            self.m_vLines[i].setZValue(0)
            self.m_hLines[i].setZValue(0)
            self.m_views[i].addItem(self.m_vLines[i])
            self.m_views[i].addItem(self.m_hLines[i])
            self.m_views[i].addItem(self.m_textPrices[i])

        self.m_views[0].addItem(self.m_textInfo, ignoreBounds=True)
        self.m_views[0].addItem(self.m_textSig, ignoreBounds=True)

    def setVolView(self, _view):
        self.m_volView = _view
        self.m_volRect = self.m_volView.sceneBoundingRect()
        self.m_volTextPrice.setZValue(2)
        self.m_volVLine.setPos(0)
        self.m_volHLine.setPos(0)
        self.m_volVLine.setZValue(0)
        self.m_volHLine.setZValue(0)
        self.m_volView.addItem(self.m_volVLine)
        self.m_volView.addItem(self.m_volHLine)
        self.m_volView.addItem(self.m_volTextPrice)
        self.m_volView.addItem(self.m_textVolume, ignoreBounds=True)

    def setYAxis(self, _index, _yAxis):
        self.m_yAxises[_index] = _yAxis

    def setShowHLine(self, _index, _showHLine):
        self.m_showHLine[_index] = _showHLine

    # ----------------------------------------------------------------------
    def moveTo(self, _xAxis, _yAxis):

        _xAxis = self.m_xAxis if _xAxis is None else int(_xAxis)
        _yAxis = self.m_yAxis if _yAxis is None else int(_yAxis)

        self.m_rects = [self.m_views[i].sceneBoundingRect() for i in range(1)]
        self.m_volRect = self.m_volView.sceneBoundingRect()

        self.m_xAxis = _xAxis
        self.m_yAxis = _yAxis

        for i in range(1):
            self.m_vLines[i].setPos(_xAxis)
            if self.m_showHLine[i]:
                self.m_hLines[i].setPos(_yAxis if i == 0 else self.m_yAxises[i])
                self.m_hLines[i].show()
            else:
                self.m_hLines[i].hide()

        self.m_volVLine.setPos(_xAxis)
        if self.m_volShowHLine:
            self.m_volHLine.setPos(self.m_volYAxis)
            self.m_volHLine.show()
        else:
            self.m_volHLine.hide()


        if self.m_datas is None:
            return
        try:
            # 获取K线数据
            data = self.m_datas[_xAxis]
            lastdata = self.m_datas[_xAxis - 1]
            tickDatetime = data['datetime']
            openPrice = data['open']
            closePrice = data['close']
            lowPrice = data['low']
            highPrice = data['high']
            volume = data['volume']
            preClosePrice = lastdata['close']
        except Exception, e:
            return

        if (isinstance(tickDatetime, dt.datetime)):
            dateText = dt.datetime.strftime(tickDatetime, '%Y-%m-%d')
            timeText = dt.datetime.strftime(tickDatetime, '%H:%M:%S')
        else:
            dateText = ""
            timeText = ""

        # 显示所有的主图技术指标
        html = u'<div style="text-align: right">'
        for sig in self.m_master.m_sigData:
            val = self.m_master.m_sigData[sig][_xAxis]
            col = self.m_master.m_sigColor[sig]
            html += u'<span style="color: %s;  font-size: 20px;">&nbsp;&nbsp;%s：%.2f</span>' % (col, sig, val)
        html += u'</div>'
        self.m_textSig.setHtml(html)

        # 和上一个收盘价比较，决定K线信息的字符颜色
        cOpen = 'red' if openPrice > preClosePrice else 'green'
        cClose = 'red' if closePrice > preClosePrice else 'green'
        cHigh = 'red' if highPrice > preClosePrice else 'green'
        cLow = 'red' if lowPrice > preClosePrice else 'green'

        self.m_textInfo.setHtml(
            u'<div style="text-align: center; background-color:#000">\
                <span style="color: white;  font-size: 16px;">日期</span><br>\
                <span style="color: yellow; font-size: 16px;">%s</span><br>\
                <span style="color: white;  font-size: 16px;">时间</span><br>\
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
            % (dateText, timeText, cOpen, openPrice, cHigh, highPrice, \
               cLow, lowPrice, cClose, closePrice, volume))


        # 坐标轴宽度
        rightAxisWidth = self.m_views[0].getAxis('right').width()
        bottomAxisHeight = 20  # self.m_oiView.getAxis('bottom').height()
        offset = QtCore.QPointF(rightAxisWidth, bottomAxisHeight)

        # 各个顶点
        topLeftList = [self.m_views[i].vb.mapSceneToView(self.m_rects[i].topLeft()) for i in range(1)]
        bottomRightList = [self.m_views[i].vb.mapSceneToView(self.m_rects[i].bottomRight() - offset) for i in range(1)]

        # 显示价格
        for i in range(1):
            if self.m_showHLine[i]:
                self.m_textPrices[i].setHtml(
                    '<div style="text-align: right">\
                         <span style="color: yellow; font-size: 20px;">\
                           %0.3f\
                         </span>\
                     </div>' \
                    % (_yAxis if i == 0 else self.m_yAxises[i]))
                self.m_textPrices[i].setPos(bottomRightList[i].x(), _yAxis if i == 0 else self.m_yAxises[i])
                self.m_textPrices[i].show()
            else:
                self.m_textPrices[i].hide()

        # 设置坐标
        self.m_textInfo.setPos(topLeftList[0])
        self.m_textSig.setPos(bottomRightList[0].x(), topLeftList[0].y())

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

        volRightAxisWidth = self.m_volView.getAxis('right').width()
        volBottomAxisHeight = 20  # self.m_oiView.getAxis('bottom').height()
        volOffset = QtCore.QPointF(volRightAxisWidth, volBottomAxisHeight)
        volTopLeft = self.m_volView.vb.mapSceneToView(self.m_volRect.topLeft())
        volBottomRight = self.m_volView.vb.mapSceneToView(self.m_volRect.bottomRight() - volOffset)
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