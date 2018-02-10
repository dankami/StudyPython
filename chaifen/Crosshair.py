# encoding: UTF-8
import sys,os
import PyQt4
import pyqtgraph as pg
import datetime as dt          
import numpy as np
import traceback

from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point

########################################################################
# 十字光标支持
########################################################################
class Crosshair(PyQt4.QtCore.QObject):
    """
    此类给pg.PlotWidget()添加crossHair功能,PlotWidget实例需要初始化时传入
    """
    signal = QtCore.pyqtSignal(type(tuple([])))
    signalInfo = QtCore.pyqtSignal(float,float)
    #----------------------------------------------------------------------
    def __init__(self, _parent, _master):
        """Constructor"""
        self.m_view = _parent
        self.m_master = _master
        super(Crosshair, self).__init__()

        self.m_xAxis = 0
        self.m_yAxis = 0

        self.m_datas = None

        self.m_yAxises    = [0 for i in range(3)]
        self.m_leftX      = [0 for i in range(3)]
        self.m_showHLine  = [False for i in range(3)]
        self.m_textPrices = [pg.TextItem('', anchor=(1, 1)) for i in range(3)]
        self.m_views      = [_parent.centralWidget.getItem(i + 1, 0) for i in range(3)]
        self.m_rects      = [self.m_views[i].sceneBoundingRect() for i in range(3)]
        self.m_vLines     = [pg.InfiniteLine(angle=90, movable=False) for i in range(3)]
        self.m_hLines     = [pg.InfiniteLine(angle=0, movable=False) for i in range(3)]
        
        #mid 在y轴动态跟随最新价显示最新价和最新时间
        self.m_textDate   = pg.TextItem('date', anchor=(1, 1))
        self.m_textInfo   = pg.TextItem('lastBarInfo')
        self.m_textSig    = pg.TextItem('lastSigInfo', anchor=(1, 0))
        self.m_textSubSig = pg.TextItem('lastSubSigInfo', anchor=(1, 0))
        self.m_textVolume = pg.TextItem('lastBarVolume', anchor=(1, 0))

        self.m_textDate.setZValue(2)
        self.m_textInfo.setZValue(2)
        self.m_textSig.setZValue(2)
        self.m_textSubSig.setZValue(2)
        self.m_textVolume.setZValue(2)
        self.m_textInfo.border = pg.mkPen(color=(230, 255, 0, 255), width=1.2)
        
        for i in range(3):
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
        self.m_views[2].addItem(self.m_textDate, ignoreBounds=True)
        self.m_views[2].addItem(self.m_textSubSig, ignoreBounds=True)
        self.proxy = pg.SignalProxy(self.m_view.scene().sigMouseMoved, rateLimit=360, slot=self.__mouseMoved)
        # 跨线程刷新界面支持
        self.signal.connect(self.update)
        self.signalInfo.connect(self.plotInfo)

    #----------------------------------------------------------------------
    def update(self,pos):
        """刷新界面显示"""
        xAxis,yAxis = pos
        xAxis,yAxis = (self.m_xAxis, self.m_yAxis) if xAxis is None else (xAxis, yAxis)
        self.moveTo(xAxis,yAxis)
        
    #----------------------------------------------------------------------
    def __mouseMoved(self,evt):
        """鼠标移动回调"""
        pos = evt[0]  
        self.m_rects = [self.m_views[i].sceneBoundingRect() for i in range(3)]
        for i in range(3):
            self.m_showHLine[i] = False
            if self.m_rects[i].contains(pos):
                mousePoint = self.m_views[i].vb.mapSceneToView(pos)
                xAxis = mousePoint.x()
                yAxis = mousePoint.y()    
                self.m_yAxises[i] = yAxis
                self.m_showHLine[i] = True
                self.moveTo(xAxis,yAxis)

    #----------------------------------------------------------------------
    def moveTo(self,xAxis,yAxis):
        xAxis,yAxis = (self.m_xAxis, self.m_yAxis) if xAxis is None else (int(xAxis), yAxis)
        self.m_rects  = [self.m_views[i].sceneBoundingRect() for i in range(3)]
        if not xAxis or not yAxis:
            return
        self.m_xAxis = xAxis
        self.m_yAxis = yAxis
        self.vhLinesSetXY(xAxis,yAxis)
        self.plotInfo(xAxis,yAxis)

    #----------------------------------------------------------------------
    def vhLinesSetXY(self,xAxis,yAxis):
        """水平和竖线位置设置"""
        for i in range(3):
            self.m_vLines[i].setPos(xAxis)
            if self.m_showHLine[i]:
                self.m_hLines[i].setPos(yAxis if i == 0 else self.m_yAxises[i])
                self.m_hLines[i].show()
            else:
                self.m_hLines[i].hide()

    #----------------------------------------------------------------------
    def plotInfo(self,xAxis,yAxis):        
        """
        被嵌入的plotWidget在需要的时候通过调用此方法显示K线信息
        """
        if self.m_datas is None:
            return
        try:
            # 获取K线数据
            data            = self.m_datas[xAxis]
            lastdata        = self.m_datas[xAxis - 1]
            tickDatetime    = data['datetime']
            openPrice       = data['open']
            closePrice      = data['close']
            lowPrice        = data['low']
            highPrice       = data['high']
            volume          = data['volume']
            openInterest    = data['openInterest']
            preClosePrice   = lastdata['close']
        except Exception, e:
            return
            
        if(isinstance(tickDatetime,dt.datetime)):
            datetimeText = dt.datetime.strftime(tickDatetime,'%Y-%m-%d %H:%M:%S')
            dateText     = dt.datetime.strftime(tickDatetime,'%Y-%m-%d')
            timeText     = dt.datetime.strftime(tickDatetime,'%H:%M:%S')
        else:
            datetimeText = ""
            dateText     = ""
            timeText     = ""

        # 显示所有的主图技术指标
        html = u'<div style="text-align: right">'
        for sig in self.m_master.m_sigData:
            val = self.m_master.m_sigData[sig][xAxis]
            col = self.m_master.m_sigColor[sig]
            html+= u'<span style="color: %s;  font-size: 20px;">&nbsp;&nbsp;%s：%.2f</span>' %(col,sig,val)
        html+=u'</div>' 
        self.m_textSig.setHtml(html)

        # 显示所有的主图技术指标
        html = u'<div style="text-align: right">'
        for sig in self.m_master.m_subSigData:
            val = self.m_master.m_subSigData[sig][xAxis]
            col = self.m_master.m_subSigColor[sig]
            html+= u'<span style="color: %s;  font-size: 20px;">&nbsp;&nbsp;%s：%.2f</span>' %(col,sig,val)
        html+=u'</div>' 
        self.m_textSubSig.setHtml(html)

        
        # 和上一个收盘价比较，决定K线信息的字符颜色
        cOpen     = 'red' if openPrice  > preClosePrice else 'green'
        cClose    = 'red' if closePrice > preClosePrice else 'green'
        cHigh     = 'red' if highPrice  > preClosePrice else 'green'
        cLow      = 'red' if lowPrice   > preClosePrice else 'green'
            
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
                            </div>'\
                                % (dateText,timeText,cOpen,openPrice,cHigh,highPrice,\
                                    cLow,lowPrice,cClose,closePrice,volume))             
        self.m_textDate.setHtml(
                            '<div style="text-align: center">\
                                <span style="color: yellow; font-size: 20px;">%s</span>\
                            </div>'\
                                % (datetimeText))   

        self.m_textVolume.setHtml(
                            '<div style="text-align: right">\
                                <span style="color: white; font-size: 20px;">VOL : %.3f</span>\
                            </div>'\
                                % (volume))   
        # 坐标轴宽度
        rightAxisWidth = self.m_views[0].getAxis('right').width()
        bottomAxisHeight = self.m_views[2].getAxis('bottom').height()
        offset = QtCore.QPointF(rightAxisWidth,bottomAxisHeight)

        # 各个顶点
        tl = [self.m_views[i].vb.mapSceneToView(self.m_rects[i].topLeft()) for i in range(3)]
        br = [self.m_views[i].vb.mapSceneToView(self.m_rects[i].bottomRight() - offset) for i in range(3)]

        # 显示价格
        for i in range(3):
            if self.m_showHLine[i]:
                self.m_textPrices[i].setHtml(
                        '<div style="text-align: right">\
                             <span style="color: yellow; font-size: 20px;">\
                               %0.3f\
                             </span>\
                         </div>'\
                        % (yAxis if i==0 else self.m_yAxises[i]))
                self.m_textPrices[i].setPos(br[i].x(), yAxis if i == 0 else self.m_yAxises[i])
                self.m_textPrices[i].show()
            else:
                self.m_textPrices[i].hide()

        
        # 设置坐标
        self.m_textInfo.setPos(tl[0])
        self.m_textSig.setPos(br[0].x(), tl[0].y())
        self.m_textSubSig.setPos(br[2].x(), tl[2].y())
        self.m_textVolume.setPos(br[1].x(), tl[1].y())

        # 修改对称方式防止遮挡
        self.m_textDate.anchor = Point((1, 1)) if xAxis > self.m_master.m_index else Point((0, 1))
        self.m_textDate.setPos(xAxis, br[2].y())
