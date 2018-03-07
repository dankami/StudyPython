# -*- coding: utf-8 -*-
import pyqtgraph as pg
import numpy as np
from PyQt4.QtGui import *

########################################################################
# 时间序列，横坐标支持
########################################################################
class TimeAxisItem(pg.AxisItem):
    """时间序列横坐标支持"""

    # 初始化
    # ----------------------------------------------------------------------
    def __init__(self, xdict, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.m_minVal = 0
        self.m_maxVal = 0
        self.m_xdict = xdict
        self.m_valuesX = np.asarray(xdict.keys())
        self.m_stringsX = xdict.values()
        self.setPen(color=(255, 255, 255, 255), width=0.8)
        self.setStyle(tickFont=QFont("Roman times", 10, QFont.Bold), autoExpandTextSpace=True)

    # 更新坐标映射表
    # ----------------------------------------------------------------------
    def update_xdict(self, xdict):
        self.m_xdict.update(xdict)
        self.m_valuesX = np.asarray(self.m_xdict.keys())
        self.m_stringsX = self.m_xdict.values()

    # 将原始横坐标转换为时间字符串,第一个坐标包含日期
    # ----------------------------------------------------------------------
    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            vs = v * scale
            if vs in self.m_valuesX:
                vstr = self.m_stringsX[np.abs(self.m_valuesX - vs).argmin()]
                vstr = vstr.strftime('%Y-%m-%d %H:%M:%S')
            else:
                vstr = ""
            strings.append(vstr)
        return strings