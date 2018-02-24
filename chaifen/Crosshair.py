# encoding: UTF-8

import PyQt4
import pyqtgraph as pg
import datetime as dt

from pyqtgraph.Qt import QtCore
from pyqtgraph.Point import Point


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

        self.m_yAxises = [0 for i in range(2)]
        self.m_showHLine = [False for i in range(2)]
        self.m_textPrices = [pg.TextItem('', anchor=(1, 1)) for i in range(2)]

        self.m_vLines = [pg.InfiniteLine(angle=90, movable=False) for i in range(2)]
        self.m_hLines = [pg.InfiniteLine(angle=0, movable=False) for i in range(2)]

        # oi部分
        self.m_oiYAxis = 0
        self.m_oiLeftX = 0
        self.m_oiShowHLine = False
        self.m_oiTextPrice = pg.TextItem('', anchor=(1, 1))
        self.m_oiVLine = pg.InfiniteLine(angle=90, movable=False)
        self.m_oiHLine = pg.InfiniteLine(angle=0, movable=False)
        self.m_textDate = pg.TextItem('date', anchor=(1, 1))
        self.m_textSubSig = pg.TextItem('lastSubSigInfo', anchor=(1, 0))
        self.m_textDate.setZValue(2)
        self.m_textSubSig.setZValue(2)

        # mid 在y轴动态跟随最新价显示最新价和最新时间
        self.m_textInfo = pg.TextItem('lastBarInfo')
        self.m_textSig = pg.TextItem('lastSigInfo', anchor=(1, 0))
        self.m_textVolume = pg.TextItem('lastBarVolume', anchor=(1, 0))

        self.m_textInfo.setZValue(2)
        self.m_textSig.setZValue(2)
        self.m_textVolume.setZValue(2)
        self.m_textInfo.border = pg.mkPen(color=(230, 255, 0, 255), width=1.2)

        # 跨线程刷新界面支持
        self.signal.connect(self.update)
        self.signalInfo.connect(self.plotInfo)

    # 设置数据
    def setDatas(self, _datas):
        self.m_datas = _datas

    # 设置UI
    def setViews(self, _views):
        self.m_views = _views
        self.m_rects = [self.m_views[i].sceneBoundingRect() for i in range(2)]
        for i in range(2):
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
        self.m_views[1].addItem(self.m_textVolume, ignoreBounds=True)

    # 设置oi
    def setOIPlotItem(self, _item):
        self.m_oiView = _item
        self.m_oiRect = self.m_oiView.sceneBoundingRect()
        self.m_oiTextPrice.setZValue(2)
        self.m_oiVLine.setPos(0)
        self.m_oiHLine.setPos(0)
        self.m_oiVLine.setZValue(0)
        self.m_oiHLine.setZValue(0)
        self.m_oiView.addItem(self.m_oiVLine)
        self.m_oiView.addItem(self.m_oiHLine)
        self.m_oiView.addItem(self.m_oiTextPrice)
        self.m_oiView.addItem(self.m_textDate, ignoreBounds=True)
        self.m_oiView.addItem(self.m_textSubSig, ignoreBounds=True)

    # ----------------------------------------------------------------------
    def update(self, _pos):
        """刷新界面显示"""
        xAxis, yAxis = _pos
        xAxis, yAxis = (self.m_xAxis, self.m_yAxis) if xAxis is None else (xAxis, yAxis)
        self.moveTo(xAxis, yAxis)

    # ----------------------------------------------------------------------
    def onMouseMoved(self, _evt):
        """鼠标移动回调"""
        pos = _evt[0]
        self.m_rects = [self.m_views[i].sceneBoundingRect() for i in range(2)]
        xAxis = None
        yAxis = None
        for i in range(2):
            self.m_showHLine[i] = False
            if self.m_rects[i].contains(pos):
                mousePoint = self.m_views[i].vb.mapSceneToView(pos)
                xAxis = mousePoint.x()
                yAxis = mousePoint.y()
                self.m_yAxises[i] = yAxis
                self.m_showHLine[i] = True

        # oi部分
        self.m_oiRect = self.m_oiView.sceneBoundingRect()
        self.m_oiShowHLine = False
        if self.m_oiRect.contains(pos):
            mousePoint = self.m_oiView.vb.mapSceneToView(pos)
            xAxis = mousePoint.x()
            yAxis = mousePoint.y()
            self.m_oiYAxis = yAxis
            self.m_oiShowHLine = True

        self.moveTo(xAxis, yAxis)

    # ----------------------------------------------------------------------
    def moveTo(self, xAxis, yAxis):
        xAxis, yAxis = (self.m_xAxis, self.m_yAxis) if xAxis is None else (int(xAxis), yAxis)
        self.m_rects = [self.m_views[i].sceneBoundingRect() for i in range(2)]
        self.m_oiRect = self.m_oiView.sceneBoundingRect()
        if not xAxis or not yAxis:
            return
        self.m_xAxis = xAxis
        self.m_yAxis = yAxis
        self.vhLinesSetXY(xAxis, yAxis)
        self.plotInfo(xAxis, yAxis)

    # ----------------------------------------------------------------------
    def vhLinesSetXY(self, xAxis, yAxis):
        """水平和竖线位置设置"""
        for i in range(2):
            self.m_vLines[i].setPos(xAxis)
            if self.m_showHLine[i]:
                self.m_hLines[i].setPos(yAxis if i == 0 else self.m_yAxises[i])
                self.m_hLines[i].show()
            else:
                self.m_hLines[i].hide()

        # oi部分
        self.m_oiVLine.setPos(xAxis)
        if self.m_oiShowHLine:
            self.m_oiHLine.setPos(self.m_oiYAxis)
            self.m_oiHLine.show()
        else:
            self.m_oiHLine.hide()

    # ----------------------------------------------------------------------
    def plotInfo(self, _xAxis, _yAxis):
        """
        被嵌入的plotWidget在需要的时候通过调用此方法显示K线信息
        """
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


        self.m_textVolume.setHtml(
            '<div style="text-align: right">\
                <span style="color: white; font-size: 20px;">VOL : %.3f</span>\
            </div>' \
            % (volume))
        # 坐标轴宽度
        rightAxisWidth = self.m_views[0].getAxis('right').width()
        bottomAxisHeight = 20 #self.m_oiView.getAxis('bottom').height()
        offset = QtCore.QPointF(rightAxisWidth, bottomAxisHeight)

        # 各个顶点
        topLeftList = [self.m_views[i].vb.mapSceneToView(self.m_rects[i].topLeft()) for i in range(2)]
        bottomRightList = [self.m_views[i].vb.mapSceneToView(self.m_rects[i].bottomRight() - offset) for i in range(2)]


        # 显示价格
        for i in range(2):
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

        self.m_textVolume.setPos(bottomRightList[1].x(), topLeftList[1].y())



        # oi部分
        if self.m_datas is None:
            return
        try:
            # 获取K线数据
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

        oiRightAxisWidth = self.m_oiView.getAxis('right').width()
        oiBottomAxisHeight = self.m_oiView.getAxis('bottom').height()
        oiOffset = QtCore.QPointF(oiRightAxisWidth, oiBottomAxisHeight)
        oiTopLeft = self.m_oiView.vb.mapSceneToView(self.m_oiRect.topLeft())
        oiBottomRigt = self.m_oiView.vb.mapSceneToView(self.m_oiRect.bottomRight() - oiOffset)

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

