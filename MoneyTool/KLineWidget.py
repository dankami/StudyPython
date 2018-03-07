# -*- coding: utf-8 -*-
"""
Python K线模块,包含十字光标和鼠标键盘交互
Support By 量投科技(http://www.quantdo.com.cn/)
"""


# Qt相关和十字光标
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
# 其他
import numpy as np
import pandas as pd
from functools import partial

# 自己
from KLPlotItem import KLPlotItem
from VolPlotItem import VolPlotItem
from OIPlotItem import OIPlotItem

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
        self.m_midIndex    = None    # 下标
        self.m_countK   = 60      # 显示的Ｋ线范围

        # 缓存数据
        self.m_datas    = []
        self.m_listBar  = []
        self.m_listVol  = []
        self.m_listSig  = []
        self.m_listOpenInterest = []
        self.m_arrows   = []

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
        self.m_pgTitle = self.m_pgLayout.addLabel(u'量化分析工具', size='20pt')
        self.m_plotWidget.setCentralItem(self.m_pgLayout)
        # self.m_plotWidget.centralWidget.getItem(0, 0).setText(u'原来是你', size='20pt')

        # 初始化子图
        self.m_klPlotItem = KLPlotItem()
        self.m_pgLayout.nextRow()
        self.m_pgLayout.addItem(self.m_klPlotItem)

        self.m_volPlotItem = VolPlotItem()
        self.m_pgLayout.nextRow()
        self.m_pgLayout.addItem(self.m_volPlotItem)

        # self.m_oiPlotItem = OIPlotItem()
        # self.m_curveOI = self.m_oiPlotItem.plot()
        # self.m_pgLayout.nextRow()
        # self.m_pgLayout.addItem(self.m_oiPlotItem)

        # 注册鼠标事件
        self.m_proxy = pg.SignalProxy(self.m_plotWidget.scene().sigMouseMoved, rateLimit=360, slot=self.pwMouseMoved)
        # 设置界面
        self.m_vbLayout = QtGui.QVBoxLayout()
        self.m_vbLayout.addWidget(self.m_plotWidget)
        self.setLayout(self.m_vbLayout)
        # 初始化完成
        self.m_initCompleted = True

    # pg组件监听鼠标事件
    def pwMouseMoved(self, _event):
        pos = _event[0]
        xAxis = None
        yAxis = None
        klRect = self.m_klPlotItem.sceneBoundingRect()
        volRect = self.m_volPlotItem.sceneBoundingRect()
        # oiRect = self.m_oiPlotItem.sceneBoundingRect()
        self.m_klPlotItem.setShowHLine(False)
        self.m_volPlotItem.setShowHLine(False)
        # self.m_oiPlotItem.setShowHLine(False)
        if klRect.contains(pos):
            mousePoint = self.m_klPlotItem.vb.mapSceneToView(pos)
            xAxis = mousePoint.x()
            yAxis = mousePoint.y()
            self.m_klPlotItem.setYAxis(yAxis)
            self.m_klPlotItem.setShowHLine(True)
        if volRect.contains(pos):
            mousePoint = self.m_volPlotItem.vb.mapSceneToView(pos)
            xAxis = mousePoint.x()
            yAxis = mousePoint.y()
            self.m_volPlotItem.setYAxis(yAxis)
            self.m_volPlotItem.setShowHLine(True)
        # if oiRect.contains(pos):
        #     mousePoint = self.m_oiPlotItem.vb.mapSceneToView(pos)
        #     xAxis = mousePoint.x()
        #     yAxis = mousePoint.y()
        #     self.m_oiPlotItem.setYAxis(yAxis)
        #     self.m_oiPlotItem.setShowHLine(True)

        self.moveTo(xAxis, yAxis)

    # 移动坐标
    def moveTo(self, _xAxis, _yAxis):
        self.m_klPlotItem.moveTo(_xAxis, _yAxis)
        self.m_volPlotItem.moveTo(_xAxis, _yAxis)
        # self.m_oiPlotItem.moveTo(_xAxis, _yAxis)

    #----------------------------------------------------------------------
    #  画图相关 
    #----------------------------------------------------------------------
    def plotVol(self,redraw=False,xmin=0,xmax=-1):
        """重画成交量子图"""
        if self.m_initCompleted:
            self.m_volPlotItem.updateCandle(self.m_listVol[xmin:xmax], redraw)   # 画成交量子图

    #----------------------------------------------------------------------
    def plotKline(self,redraw=False,xmin=0,xmax=-1):
        """重画K线子图"""
        if self.m_initCompleted:
            self.m_klPlotItem.updateCandle(self.m_listBar[xmin:xmax], redraw)   # 画K线
            self.plotMark()                             # 显示开平仓信号位置

    #----------------------------------------------------------------------
    def plotOI(self,xmin=0,xmax=-1):
        """重画持仓量子图"""
        # if self.m_initCompleted:
        #     self.m_curveOI.setData(self.m_listOpenInterest[xmin:xmax] + [0], pen='w', name="OpenInterest")

    #----------------------------------------------------------------------
    def plotMark(self):
        """显示开平仓信号"""
        # 检查是否有数据
        if len(self.m_datas)==0:
            return
        for arrow in self.m_arrows:
            self.m_klPlotItem.removeItem(arrow)
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
            self.m_klPlotItem.addItem(arrow)
            self.m_arrows.append(arrow)

    #----------------------------------------------------------------------
    def plotAll(self,redraw=True,xMin=0,xMax=-1):
        """
        重画所有界面
        redraw ：False=重画最后一根K线; True=重画所有
        xMin,xMax : 数据范围
        """
        xMax = len(self.m_datas) if xMax < 0 else xMax
        self.m_countK = xMax - xMin
        self.m_midIndex = int((xMax + xMin) / 2)
        self.m_klPlotItem.setLimits(xMin=xMin, xMax=xMax)
        self.m_volPlotItem.setLimits(xMin=xMin, xMax=xMax)
        # self.m_oiPlotItem.setLimits(xMin=xMin, xMax=xMax)
        self.plotKline(redraw,xMin,xMax)                       # K线图
        self.plotVol(redraw,xMin,xMax)                         # K线副图，成交量
        self.plotOI(0, len(self.m_datas))                         # K线副图，持仓量
        self.refresh()

    #----------------------------------------------------------------------
    def refresh(self):
        """
        刷新三个子图的现实范围
        """   
        minutes = int(self.m_countK / 2)
        xmin    = max(0, self.m_midIndex - minutes)
        xmax    = xmin+2*minutes
        self.m_klPlotItem.setRange(xRange = (xmin, xmax))
        self.m_volPlotItem.setRange(xRange = (xmin, xmax))
        # self.m_oiPlotItem.setRange(xRange=(xmin, xmax))

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

    # 重载方法wheelEvent(self,event),即滚轮事件方法
    # ----------------------------------------------------------------------
    def wheelEvent(self, event):
        if event.delta() > 0:
            self.onUp()
        else:
            self.onDown()

    def onNxt(self):
        """跳转到下一个开平仓点"""
        if len(self.m_listSig)>0 and not self.m_midIndex is None:
            datalen = len(self.m_listSig)
            self.m_midIndex+=1
            while self.m_midIndex < datalen and self.m_listSig[self.m_midIndex] == 0:
                self.m_midIndex+=1
            self.refresh()
            x = self.m_midIndex
            y = self.m_datas[x]['close']
            self.moveTo(x, y)

    #----------------------------------------------------------------------
    def onPre(self):
        """跳转到上一个开平仓点"""
        if  len(self.m_listSig)>0 and not self.m_midIndex is None:
            self.m_midIndex-=1
            while self.m_midIndex > 0 and self.m_listSig[self.m_midIndex] == 0:
                self.m_midIndex-=1
            self.refresh()
            x = self.m_midIndex
            y = self.m_datas[x]['close']
            self.moveTo(x, y)

    #----------------------------------------------------------------------
    def onDown(self):
        """放大显示区间"""
        self.m_countK = min(len(self.m_datas), int(self.m_countK * 1.2) + 1)
        self.refresh()
        if len(self.m_datas)>0:
            x = self.m_midIndex - self.m_countK / 2 + 2 if int(self.m_klPlotItem.getXAxis()) < self.m_midIndex - self.m_countK / 2 + 2 else int(self.m_klPlotItem.getXAxis())
            x = self.m_midIndex + self.m_countK / 2 - 2 if x > self.m_midIndex + self.m_countK / 2 - 2 else x
            y = self.m_datas[x][2]
            self.moveTo(x, y)

    #----------------------------------------------------------------------
    def onUp(self):
        """缩小显示区间"""
        self.m_countK = max(3, int(self.m_countK / 1.2) - 1)
        self.refresh()
        if len(self.m_datas)>0:
            x = self.m_midIndex - self.m_countK / 2 + 2 if int(self.m_klPlotItem.getXAxis()) < self.m_midIndex - self.m_countK / 2 + 2 else int(self.m_klPlotItem.getXAxis())
            x = self.m_midIndex + self.m_countK / 2 - 2 if x > self.m_midIndex + self.m_countK / 2 - 2 else x
            y = self.m_datas[x]['close']
            self.moveTo(x, y)

    #----------------------------------------------------------------------
    def onLeft(self):
        """向左移动"""
        if len(self.m_datas)>0 and int(self.m_klPlotItem.getXAxis())>2:
            x = int(self.m_klPlotItem.getXAxis()) - 1
            y = self.m_datas[x]['close']
            if x <= self.m_midIndex-self.m_countK/2+2 and self.m_midIndex>1:
                self.m_midIndex -= 1
                self.refresh()
            self.moveTo(x, y)

    #----------------------------------------------------------------------
    def onRight(self):
        """向右移动"""
        if len(self.m_datas)>0 and int(self.m_klPlotItem.getXAxis())<len(self.m_datas)-1:
            x = int(self.m_klPlotItem.getXAxis()) + 1
            y = self.m_datas[x]['close']
            if x >= self.m_midIndex+int(self.m_countK/2)-2:
                self.m_midIndex += 1
                self.refresh()
            self.moveTo(x, y)
    
    #----------------------------------------------------------------------
    # 界面回调相关
    #----------------------------------------------------------------------
    def onPaint(self):
        """界面刷新回调"""
        view = self.m_klPlotItem.getViewBox()
        vRange = view.viewRange()
        xmin = max(0,int(vRange[0][0]))
        xmax = max(0,int(vRange[0][1]))
        self.m_midIndex  = int((xmin + xmax) / 2) + 1

    #----------------------------------------------------------------------
    def loadData(self, datas):
        print datas
        """
        载入pandas.DataFrame数据
        datas : 数据格式，cols : datetime, open, close, low, high
        """
        # 设置中心点时间
        self.m_midIndex = 0
        # 绑定数据，更新横坐标映射，更新Y轴自适应函数，更新十字光标映射
        datas.insert(1,'time_int',np.array(range(len(datas.index))))
        self.m_datas = datas[['open', 'close', 'low', 'high', 'volume', 'openInterest']].to_records()
        xdict = dict(enumerate(datas.index.tolist()))
        # self.m_oiPlotItem.update_xdict(xdict)
        self.m_volPlotItem.update_xdict(xdict)
        self.resignData(self.m_datas)
        # 更新画图用到的数据
        self.m_listBar          = datas[['time_int', 'open', 'close', 'low', 'high']].to_records(False)
        self.m_listOpenInterest = list(datas['openInterest'])
        # 成交量颜色和涨跌同步，K线方向由涨跌决定
        datas0                = pd.DataFrame()
        datas0['open']        = datas.apply(lambda x:0 if x['close'] >= x['open'] else x['volume'],axis='columns')
        datas0['close']       = datas.apply(lambda x:0 if x['close'] <  x['open'] else x['volume'],axis='columns')
        datas0['low']         = 0
        datas0['high']        = datas['volume']
        datas0['time_int']    = np.array(range(len(datas.index)))
        self.m_listVol        = datas0[['time_int', 'open', 'close', 'low', 'high']].to_records(False)
        # 调用画图函数
        self.plotAll(True, 0, len(self.m_datas))

    #----------------------------------------------------------------------
    def resignData(self, _datas):
        """更新数据，用于Y坐标自适应"""
        self.m_klPlotItem.setDatas(_datas)
        self.m_volPlotItem.setDatas(_datas)
        # self.m_oiPlotItem.setDatas(_datas)
        def viewXRangeChanged(low,high,self):
            vRange = self.viewRange()
            xmin = max(0,int(vRange[0][0]))
            xmax = max(0,int(vRange[0][1]))
            xmax = min(xmax, len(_datas))
            if len(_datas)>0 and xmax > xmin:
                ymin = min(_datas[xmin:xmax][low])
                ymax = max(_datas[xmin:xmax][high])
                self.setRange(yRange = (ymin,ymax))
            else:
                self.setRange(yRange = (0,1))

        view = self.m_klPlotItem.getViewBox()
        view.sigXRangeChanged.connect(partial(viewXRangeChanged,'low','high'))

        view = self.m_volPlotItem.getViewBox()
        view.sigXRangeChanged.connect(partial(viewXRangeChanged,'volume','volume'))

        # view = self.m_oiPlotItem.getViewBox()
        # view.sigXRangeChanged.connect(partial(viewXRangeChanged,'openInterest','openInterest'))

    #----------------------------------------------------------------------
    # 数据相关
    #----------------------------------------------------------------------
    def clearData(self):
        """清空数据"""
        # 清空数据，重新画图
        self.time_index = []
        self.m_listBar = []
        self.m_listVol = []
        self.m_listOpenInterest = []
        self.m_listSig = []
        self.m_datas = None


