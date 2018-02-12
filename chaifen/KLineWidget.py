# -*- coding: utf-8 -*-
"""
Python K线模块,包含十字光标和鼠标键盘交互
Support By 量投科技(http://www.quantdo.com.cn/)
"""


# Qt相关和十字光标
from PyQt4.QtGui import *
from PyQt4 import QtGui,QtCore
from Crosshair import Crosshair
import pyqtgraph as pg
# 其他
import numpy as np
import pandas as pd
from functools import partial
from datetime import datetime
from collections import deque

# 自己
from KeyWraper import KeyWraper
from CustomViewBox import CustomViewBox
from TimeAxisItem import TimeAxisItem
from CandlestickItem import CandlestickItem

# 字符串转换
#---------------------------------------------------------------------------------------
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

########################################################################
class KLineWidget(QtGui.QWidget):
    """用于显示价格走势图"""
    #----------------------------------------------------------------------
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # 当前序号
        self.m_index    = None    # 下标
        self.m_countK   = 60      # 显示的Ｋ线范围

        # 缓存数据
        self.m_datas    = []
        self.m_listBar  = []
        self.m_listVol  = []
        self.m_listHigh = []
        self.m_listLow  = []
        self.m_listSig  = []
        self.m_listOpenInterest = []
        self.m_arrows   = []

        # 所有K线上信号图
        self.m_allColor = deque(['blue', 'green', 'yellow', 'white'])
        self.m_sigData  = {}
        self.m_sigColor = {}
        self.m_sigPlots = {}

        # 所副图上信号图
        self.m_allSubColor = deque(['blue', 'green', 'yellow', 'white'])
        self.m_subSigData  = {}
        self.m_subSigColor = {}
        self.m_subSigPlots = {}

        # 初始化完成
        self.m_initCompleted = False

        # 调用函数
        self.initUi()

    #----------------------------------------------------------------------
    #  初始化相关 
    #----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle(u'K线工具')
        # 主图
        self.m_plotWidget = pg.PlotWidget()
        # 界面布局
        self.m_pgLayout = pg.GraphicsLayout(border=(100, 100, 100))
        self.m_pgLayout.setContentsMargins(10, 10, 10, 10)
        self.m_pgLayout.setSpacing(0)
        self.m_pgLayout.setBorder(color=(255, 255, 255, 255), width=0.8)
        self.m_pgLayout.setZValue(0)
        self.m_pgTitle = self.m_pgLayout.addLabel(u'')
        self.m_plotWidget.setCentralItem(self.m_pgLayout)
        # 设置横坐标
        xdict = {}
        self.m_timeAxis = TimeAxisItem(xdict, orientation='bottom')
        # 初始化子图
        self.initplotKline()
        self.initplotVol()  
        self.initplotOI()
        # 注册十字光标
        self.m_crosshair = Crosshair(self)
        self.m_views = [self.m_plotWidget.centralWidget.getItem(i + 1, 0) for i in range(3)]
        self.m_crosshair.setViews(self.m_views)
        self.m_proxy = pg.SignalProxy(self.m_plotWidget.scene().sigMouseMoved, rateLimit=360, slot=self.pwMouseMoved)
        # 设置界面
        self.m_vbLayout = QtGui.QVBoxLayout()
        self.m_vbLayout.addWidget(self.m_plotWidget)
        self.setLayout(self.m_vbLayout)
        # 初始化完成
        self.m_initCompleted = True

    # pg组件监听鼠标事件
    def pwMouseMoved(self, _event):
        self.m_crosshair.onMouseMoved(_event)
        # self.m_crosshair.sayHello()

    #----------------------------------------------------------------------
    def makePI(self,name):
        """生成PlotItem对象"""
        vb = CustomViewBox()
        plotItem = pg.PlotItem(viewBox = vb, name=name, axisItems={'bottom': self.m_timeAxis})
        plotItem.setMenuEnabled(False)
        plotItem.setClipToView(True)
        plotItem.hideAxis('left')
        plotItem.showAxis('right')
        plotItem.setDownsampling(mode='peak')
        plotItem.setRange(xRange = (0,1),yRange = (0,1))
        plotItem.getAxis('right').setWidth(60)
        plotItem.getAxis('right').setStyle(tickFont = QFont("Roman times",10,QFont.Bold))
        plotItem.getAxis('right').setPen(color=(255, 255, 255, 255), width=0.8)
        plotItem.showGrid(True,True)
        plotItem.hideButtons()
        return plotItem

    #----------------------------------------------------------------------
    def initplotVol(self):
        """初始化成交量子图"""
        self.pwVol  = self.makePI('PlotVol')
        self.volume = CandlestickItem(self.m_listVol)
        self.pwVol.addItem(self.volume)
        self.pwVol.setMaximumHeight(150)
        self.pwVol.setXLink('PlotOI')
        self.pwVol.hideAxis('bottom')

        self.m_pgLayout.nextRow()
        self.m_pgLayout.addItem(self.pwVol)

    #----------------------------------------------------------------------
    def initplotKline(self):
        """初始化K线子图"""
        self.pwKL = self.makePI('PlotKL')
        self.candle = CandlestickItem(self.m_listBar)
        self.pwKL.addItem(self.candle)
        self.pwKL.setXLink('PlotOI')
        self.pwKL.hideAxis('bottom')

        self.m_pgLayout.nextRow()
        self.m_pgLayout.addItem(self.pwKL)

    #----------------------------------------------------------------------
    def initplotOI(self):
        """初始化持仓量子图"""
        self.pwOI = self.makePI('PlotOI')
        self.curveOI = self.pwOI.plot()

        self.m_pgLayout.nextRow()
        self.m_pgLayout.addItem(self.pwOI)

    #----------------------------------------------------------------------
    #  画图相关 
    #----------------------------------------------------------------------
    def plotVol(self,redraw=False,xmin=0,xmax=-1):
        """重画成交量子图"""
        if self.m_initCompleted:
            self.volume.generatePicture(self.m_listVol[xmin:xmax], redraw)   # 画成交量子图

    #----------------------------------------------------------------------
    def plotKline(self,redraw=False,xmin=0,xmax=-1):
        """重画K线子图"""
        if self.m_initCompleted:
            self.candle.generatePicture(self.m_listBar[xmin:xmax], redraw)   # 画K线
            self.plotMark()                             # 显示开平仓信号位置

    #----------------------------------------------------------------------
    def plotOI(self,xmin=0,xmax=-1):
        """重画持仓量子图"""
        if self.m_initCompleted:
            self.curveOI.setData(self.m_listOpenInterest[xmin:xmax] + [0], pen='w', name="OpenInterest")

    #----------------------------------------------------------------------
    def addSig(self,sig,main=True):
        """新增信号图"""
        if main:
            if sig in self.m_sigPlots:
                self.pwKL.removeItem(self.m_sigPlots[sig])
            self.m_sigPlots[sig] = self.pwKL.plot()
            self.m_sigColor[sig] = self.m_allColor[0]
            self.m_allColor.append(self.m_allColor.popleft())
        else:
            if sig in self.m_subSigPlots:
                self.pwOI.removeItem(self.m_subSigPlots[sig])
            self.m_subSigPlots[sig] = self.pwOI.plot()
            self.m_subSigColor[sig] = self.m_allSubColor[0]
            self.m_allSubColor.append(self.m_allSubColor.popleft())

    #----------------------------------------------------------------------
    def showSig(self,datas,main=True,clear=False):
        """刷新信号图"""
        if clear:
            self.clearSig(main)
            if datas and not main:
                sigDatas = np.array(datas.values()[0])
                self.m_listOpenInterest = sigDatas
                self.m_datas['openInterest'] = sigDatas
                self.plotOI(0,len(sigDatas))
        if main:
            for sig in datas:
                self.addSig(sig,main)
                self.m_sigData[sig] = datas[sig]
                self.m_sigPlots[sig].setData(datas[sig], pen=self.m_sigColor[sig][0], name=sig)
        else:
            for sig in datas:
                self.addSig(sig,main)
                self.m_subSigData[sig] = datas[sig]
                self.m_subSigPlots[sig].setData(datas[sig], pen=self.m_subSigColor[sig][0], name=sig)

    #----------------------------------------------------------------------
    def plotMark(self):
        """显示开平仓信号"""
        # 检查是否有数据
        if len(self.m_datas)==0:
            return
        for arrow in self.m_arrows:
            self.pwKL.removeItem(arrow)
        # 画买卖信号
        for i in range(len(self.m_listSig)):
            # 无信号
            if self.m_listSig[i] == 0:
                continue
            # 买信号
            elif self.m_listSig[i] > 0:
                arrow = pg.ArrowItem(pos=(i, self.m_datas[i]['low']), angle=90, brush=(255, 0, 0))
            # 卖信号
            elif self.m_listSig[i] < 0:
                arrow = pg.ArrowItem(pos=(i, self.m_datas[i]['high']), angle=-90, brush=(0, 255, 0))
            self.pwKL.addItem(arrow)
            self.m_arrows.append(arrow)

    #----------------------------------------------------------------------
    def updateAll(self):
        """
        手动更新所有K线图形，K线播放模式下需要
        """
        datas = self.m_datas
        self.volume.update()
        self.candle.update()
        def update(view,low,high):
            vRange = view.viewRange()
            xmin = max(0,int(vRange[0][0]))
            xmax = max(0,int(vRange[0][1]))
            xmax = min(xmax,len(datas))
            if len(datas)>0 and xmax > xmin:
                ymin = min(datas[xmin:xmax][low])
                ymax = max(datas[xmin:xmax][high])
                view.setRange(yRange = (ymin,ymax))
            else:
                view.setRange(yRange = (0,1))
        update(self.pwKL.getViewBox(),'low','high')
        update(self.pwVol.getViewBox(),'volume','volume')

    #----------------------------------------------------------------------
    def plotAll(self,redraw=True,xMin=0,xMax=-1):
        """
        重画所有界面
        redraw ：False=重画最后一根K线; True=重画所有
        xMin,xMax : 数据范围
        """
        xMax = len(self.m_datas) if xMax < 0 else xMax
        self.m_countK = xMax - xMin
        self.m_index = int((xMax + xMin) / 2)
        self.pwOI.setLimits(xMin=xMin,xMax=xMax)
        self.pwKL.setLimits(xMin=xMin,xMax=xMax)
        self.pwVol.setLimits(xMin=xMin,xMax=xMax)
        self.plotKline(redraw,xMin,xMax)                       # K线图
        self.plotVol(redraw,xMin,xMax)                         # K线副图，成交量
        self.plotOI(0, len(self.m_datas))                         # K线副图，持仓量
        self.refresh()

    #----------------------------------------------------------------------
    def refresh(self):
        """
        刷新三个子图的现实范围
        """   
        datas   = self.m_datas
        minutes = int(self.m_countK / 2)
        xmin    = max(0, self.m_index - minutes)
        xmax    = xmin+2*minutes
        self.pwOI.setRange(xRange = (xmin,xmax))
        self.pwKL.setRange(xRange = (xmin,xmax))
        self.pwVol.setRange(xRange = (xmin,xmax))

    #----------------------------------------------------------------------
    #  快捷键相关 
    #----------------------------------------------------------------------

    # 重载方法keyPressEvent(self,event),即按键按下事件方法
    # ----------------------------------------------------------------------
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.onUp()
        elif event.key() == QtCore.Qt.Key_Down:
            self.onDown()
        elif event.key() == QtCore.Qt.Key_Left:
            self.onLeft()
        elif event.key() == QtCore.Qt.Key_Right:
            self.onRight()
        elif event.key() == QtCore.Qt.Key_PageUp:
            self.onPre()
        elif event.key() == QtCore.Qt.Key_PageDown:
            self.onNxt()


    def onNxt(self):
        """跳转到下一个开平仓点"""
        if len(self.m_listSig)>0 and not self.m_index is None:
            datalen = len(self.m_listSig)
            self.m_index+=1
            while self.m_index < datalen and self.m_listSig[self.m_index] == 0:
                self.m_index+=1
            self.refresh()
            x = self.m_index
            y = self.m_datas[x]['close']
            self.m_crosshair.signal.emit((x, y))

    #----------------------------------------------------------------------
    def onPre(self):
        """跳转到上一个开平仓点"""
        if  len(self.m_listSig)>0 and not self.m_index is None:
            self.m_index-=1
            while self.m_index > 0 and self.m_listSig[self.m_index] == 0:
                self.m_index-=1
            self.refresh()
            x = self.m_index
            y = self.m_datas[x]['close']
            self.m_crosshair.signal.emit((x, y))

    #----------------------------------------------------------------------
    def onDown(self):
        """放大显示区间"""
        self.m_countK = min(len(self.m_datas), int(self.m_countK * 1.2) + 1)
        self.refresh()
        if len(self.m_datas)>0:
            x = self.m_index - self.m_countK / 2 + 2 if int(self.m_crosshair.m_xAxis) < self.m_index - self.m_countK / 2 + 2 else int(self.m_crosshair.m_xAxis)
            x = self.m_index + self.m_countK / 2 - 2 if x > self.m_index + self.m_countK / 2 - 2 else x
            y = self.m_datas[x][2]
            self.m_crosshair.signal.emit((x, y))

    #----------------------------------------------------------------------
    def onUp(self):
        """缩小显示区间"""
        self.m_countK = max(3, int(self.m_countK / 1.2) - 1)
        self.refresh()
        if len(self.m_datas)>0:
            x = self.m_index - self.m_countK / 2 + 2 if int(self.m_crosshair.m_xAxis) < self.m_index - self.m_countK / 2 + 2 else int(self.m_crosshair.m_xAxis)
            x = self.m_index + self.m_countK / 2 - 2 if x > self.m_index + self.m_countK / 2 - 2 else x
            y = self.m_datas[x]['close']
            self.m_crosshair.signal.emit((x, y))

    #----------------------------------------------------------------------
    def onLeft(self):
        """向左移动"""
        if len(self.m_datas)>0 and int(self.m_crosshair.m_xAxis)>2:
            x = int(self.m_crosshair.m_xAxis) - 1
            y = self.m_datas[x]['close']
            if x <= self.m_index-self.m_countK/2+2 and self.m_index>1:
                self.m_index -= 1
                self.refresh()
            self.m_crosshair.signal.emit((x, y))

    #----------------------------------------------------------------------
    def onRight(self):
        """向右移动"""
        if len(self.m_datas)>0 and int(self.m_crosshair.m_xAxis)<len(self.m_datas)-1:
            x = int(self.m_crosshair.m_xAxis) + 1
            y = self.m_datas[x]['close']
            if x >= self.m_index+int(self.m_countK/2)-2:
                self.m_index += 1
                self.refresh()
            self.m_crosshair.signal.emit((x, y))
    
    #----------------------------------------------------------------------
    # 界面回调相关
    #----------------------------------------------------------------------
    def onPaint(self):
        """界面刷新回调"""
        view = self.pwKL.getViewBox()
        vRange = view.viewRange()
        xmin = max(0,int(vRange[0][0]))
        xmax = max(0,int(vRange[0][1]))
        self.m_index  = int((xmin + xmax) / 2) + 1

    #----------------------------------------------------------------------
    def resignData(self,datas):
        """更新数据，用于Y坐标自适应"""
        self.m_crosshair.m_datas = datas
        def viewXRangeChanged(low,high,self):
            vRange = self.viewRange()
            xmin = max(0,int(vRange[0][0]))
            xmax = max(0,int(vRange[0][1]))
            xmax = min(xmax,len(datas))
            if len(datas)>0 and xmax > xmin:
                ymin = min(datas[xmin:xmax][low])
                ymax = max(datas[xmin:xmax][high])
                self.setRange(yRange = (ymin,ymax))
            else:
                self.setRange(yRange = (0,1))

        view = self.pwKL.getViewBox()
        view.sigXRangeChanged.connect(partial(viewXRangeChanged,'low','high'))

        view = self.pwVol.getViewBox()
        view.sigXRangeChanged.connect(partial(viewXRangeChanged,'volume','volume'))

        view = self.pwOI.getViewBox()
        view.sigXRangeChanged.connect(partial(viewXRangeChanged,'openInterest','openInterest'))

    #----------------------------------------------------------------------
    # 数据相关
    #----------------------------------------------------------------------
    def clearData(self):
        """清空数据"""
        # 清空数据，重新画图
        self.time_index = []
        self.m_listBar = []
        self.m_listVol = []
        self.m_listLow = []
        self.m_listHigh = []
        self.m_listOpenInterest = []
        self.m_listSig = []
        self.m_sigData = {}
        self.m_datas = None

    #----------------------------------------------------------------------
    def clearSig(self,main=True):
        """清空信号图形"""
        # 清空信号图
        if main:
            for sig in self.m_sigPlots:
                self.pwKL.removeItem(self.m_sigPlots[sig])
            self.m_sigData  = {}
            self.m_sigPlots = {}
        else:
            for sig in self.m_subSigPlots:
                self.pwOI.removeItem(self.m_subSigPlots[sig])
            self.m_subSigData  = {}
            self.m_subSigPlots = {}

    #----------------------------------------------------------------------
    def updateSig(self,sig):
        """刷新买卖信号"""
        self.m_listSig = sig
        self.plotMark()

    #----------------------------------------------------------------------
    def onBar(self, bar, nWindow = 20):
        """
        新增K线数据,K线播放模式
        nWindow : 最大数据窗口
        """
        # 是否需要更新K线
        newBar = False if len(self.m_datas) > 0 and bar.datetime == self.m_datas[-1].datetime else True
        nrecords = len(self.m_datas) if newBar else len(self.m_datas) - 1
        bar.openInterest = np.random.randint(0,3) if bar.openInterest==np.inf or bar.openInterest==-np.inf else bar.openInterest
        recordVol = (nrecords,bar.volume,0,0,bar.volume) if bar.close < bar.open else (nrecords,0,bar.volume,0,bar.volume)
        if newBar and any(self.m_datas):
            self.m_datas.resize(nrecords + 1, refcheck=0)
            self.m_listBar.resize(nrecords + 1, refcheck=0)
            self.m_listVol.resize(nrecords + 1, refcheck=0)
        elif any(self.m_datas):
            self.m_listLow.pop()
            self.m_listHigh.pop()
            self.m_listOpenInterest.pop()
        if any(self.m_datas):
            self.m_datas[-1]   = (bar.datetime, bar.open, bar.close, bar.low, bar.high, bar.volume, bar.openInterest)
            self.m_listBar[-1] = (nrecords, bar.open, bar.close, bar.low, bar.high)
            self.m_listVol[-1] = recordVol
        else:
            self.m_datas     = np.rec.array([(datetime, bar.open, bar.close, bar.low, bar.high, bar.volume, bar.openInterest)], \
                                            names=('datetime','open','close','low','high','volume','openInterest'))
            self.m_listBar   = np.rec.array([(nrecords, bar.open, bar.close, bar.low, bar.high)], \
                                            names=('datetime','open','close','low','high'))
            self.m_listVol   = np.rec.array([recordVol], names=('datetime', 'open', 'close', 'low', 'high'))
            self.resignData(self.m_datas)
        self.m_timeAxis.update_xdict({nrecords:bar.datetime})
        self.m_listLow.append(bar.low)
        self.m_listHigh.append(bar.high)
        self.m_listOpenInterest.append(bar.openInterest)
        xMax = nrecords+1
        xMin = max(0,nrecords-nWindow)
        if not newBar:
            self.updateAll()
        self.plotAll(False,xMin,xMax)
        self.m_crosshair.signal.emit((None, None))

    #----------------------------------------------------------------------
    def loadData(self, datas):
        """
        载入pandas.DataFrame数据
        datas : 数据格式，cols : datetime, open, close, low, high
        """
        # 设置中心点时间
        self.m_index = 0
        # 绑定数据，更新横坐标映射，更新Y轴自适应函数，更新十字光标映射
        datas.insert(1,'time_int',np.array(range(len(datas.index))))
        #datas['time_int'] = np.array(range(len(datas.index)))
        self.m_datas = datas[['open', 'close', 'low', 'high', 'volume', 'openInterest']].to_records()
        self.m_timeAxis.m_xdict={}
        xdict = dict(enumerate(datas.index.tolist()))
        self.m_timeAxis.update_xdict(xdict)
        self.resignData(self.m_datas)
        # 更新画图用到的数据
        self.m_listBar          = datas[['time_int', 'open', 'close', 'low', 'high']].to_records(False)
        self.m_listHigh         = list(datas['high'])
        self.m_listLow          = list(datas['low'])
        self.m_listOpenInterest = list(datas['openInterest'])
        # 成交量颜色和涨跌同步，K线方向由涨跌决定
        datas0                = pd.DataFrame()
        datas0['open']        = datas.apply(lambda x:0 if x['close'] >= x['open'] else x['volume'],axis=1)  
        datas0['close']       = datas.apply(lambda x:0 if x['close'] <  x['open'] else x['volume'],axis=1) 
        datas0['low']         = 0
        datas0['high']        = datas['volume']
        datas0['time_int']    = np.array(range(len(datas.index)))
        self.m_listVol          = datas0[['time_int', 'open', 'close', 'low', 'high']].to_records(False)
        # 调用画图函数
        self.plotAll(True, 0, len(self.m_datas))


