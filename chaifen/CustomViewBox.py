# -*- coding: utf-8 -*-
import pyqtgraph as pg
from PyQt4 import QtCore

########################################################################
# 选择缩放功能支持
########################################################################
class CustomViewBox(pg.ViewBox):
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        # 拖动放大模式
        # self.setMouseMode(self.RectMode)

    ## 右键自适应
    # ----------------------------------------------------------------------
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()