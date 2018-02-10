# -*- coding: utf-8 -*-

import pyqtgraph as pg
from PyQt4 import QtGui,QtCore


########################################################################
# K线图形对象
########################################################################
class CandlestickItem(pg.GraphicsObject):
    """K线图形对象"""

    # 初始化
    #----------------------------------------------------------------------
    def __init__(self, data):
        """初始化"""
        pg.GraphicsObject.__init__(self)
        # 数据格式: [ (time, open, close, low, high),...]
        self.m_data = data
        # 只重画部分图形，大大提高界面更新速度
        self.m_rect = None
        self.m_picture = None
        self.setFlag(self.ItemUsesExtendedStyleOption)
        # 画笔和画刷
        w = 0.4
        self.m_offset   = 0
        self.m_low      = 0
        self.m_high     = 1
        self.m_picture  = QtGui.QPicture()
        self.m_pictures = []
        self.m_bPen     = pg.mkPen(color=(0, 240, 240, 255), width=w * 2)
        self.m_bBrush   = pg.mkBrush((0, 240, 240, 255))
        self.m_rPen     = pg.mkPen(color=(255, 60, 60, 255), width=w * 2)
        self.m_rBrush   = pg.mkBrush((255, 60, 60, 255))
        self.m_rBrush.setStyle(QtCore.Qt.NoBrush)
        # 刷新K线
        self.generatePicture(self.m_data)


    # 画K线
    #----------------------------------------------------------------------
    def generatePicture(self,data=None,redraw=False):
        """重新生成图形对象"""
        # 重画或者只更新最后一个K线
        if redraw:
            self.m_pictures = []
        elif self.m_pictures:
            self.m_pictures.pop()
        w = 0.4
        bPen   = self.m_bPen
        bBrush = self.m_bBrush
        rPen   = self.m_rPen
        rBrush = self.m_rBrush
        low,high = (data[0]['low'],data[0]['high']) if len(data)>0 else (0,1)
        for (t, open0, close0, low0, high0) in data:
            if t >= len(self.m_pictures):
                picture = QtGui.QPicture()
                p = QtGui.QPainter(picture)
                low,high = (min(low,low0),max(high,high0))
                # 下跌蓝色（实心）, 上涨红色（空心）
                pen,brush,pmin,pmax = (bPen,bBrush,close0,open0)\
                    if open0 > close0 else (rPen,rBrush,open0,close0)
                p.setPen(pen)
                p.setBrush(brush)
                # 画K线方块和上下影线
                if open0 == close0:
                    p.drawLine(QtCore.QPointF(t-w,open0), QtCore.QPointF(t+w, close0))
                else:
                    p.drawRect(QtCore.QRectF(t-w, open0, w*2, close0-open0))
                if pmin  > low0:
                    p.drawLine(QtCore.QPointF(t,low0), QtCore.QPointF(t, pmin))
                if high0 > pmax:
                    p.drawLine(QtCore.QPointF(t,pmax), QtCore.QPointF(t, high0))
                p.end()
                self.m_pictures.append(picture)
        self.m_low, self.m_high = low, high

    # 手动重画
    #----------------------------------------------------------------------
    def update(self):
        if not self.scene() is None:
            self.scene().update()

    # 自动重画
    #----------------------------------------------------------------------
    def paint(self, painter, opt, w):
        rect = opt.exposedRect
        xmin,xmax = (max(0,int(rect.left())),min(int(len(self.m_pictures)), int(rect.right())))
        if not self.m_rect == (rect.left(), rect.right()) or self.m_picture is None:
            self.m_rect = (rect.left(), rect.right())
            self.m_picture = self.createPic(xmin, xmax)
            self.m_picture.play(painter)
        elif not self.m_picture is None:
            self.m_picture.play(painter)


    # 缓存图片
    #----------------------------------------------------------------------
    def createPic(self,xmin,xmax):
        picture = QtGui.QPicture()
        p = QtGui.QPainter(picture)
        [pic.play(p) for pic in self.m_pictures[xmin:xmax]]
        p.end()
        return picture

    # 定义边界
    #----------------------------------------------------------------------
    def boundingRect(self):
        return QtCore.QRectF(0, self.m_low, len(self.m_pictures), (self.m_high - self.m_low))