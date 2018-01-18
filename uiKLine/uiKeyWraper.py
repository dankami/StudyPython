# -*- coding: utf-8 -*-

########################################################################
# 键盘鼠标功能
########################################################################

from PyQt4 import QtGui, QtCore

class KeyWraper(QtGui.QWidget):
    """键盘鼠标功能支持的元类"""

    # 初始化
    # ----------------------------------------------------------------------
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setMouseTracking(True)

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

    # 重载方法mousePressEvent(self,event),即鼠标点击事件方法
    # ----------------------------------------------------------------------
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.onRClick(event.pos())
        elif event.button() == QtCore.Qt.LeftButton:
            self.onLClick(event.pos())
        event.accept()

    # 重载方法mouseReleaseEvent(self,event),即鼠标点击事件方法
    # ----------------------------------------------------------------------
    def mouseRelease(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.onRRelease(event.pos())
        elif event.button() == QtCore.Qt.LeftButton:
            self.onLRelease(event.pos())
        self.releaseMouse()

    # 重载方法wheelEvent(self,event),即滚轮事件方法
    # ----------------------------------------------------------------------
    def wheelEvent(self, event):
        if event.delta() > 0:
            self.onUp()
        else:
            self.onDown()

    # 重载方法paintEvent(self,event),即拖动事件方法
    # ----------------------------------------------------------------------
    def paintEvent(self, event):
        self.onPaint()

    # PgDown键
    # ----------------------------------------------------------------------
    def onNxt(self):
        pass

    # PgUp键
    # ----------------------------------------------------------------------
    def onPre(self):
        pass

    # 向上键和滚轮向上
    # ----------------------------------------------------------------------
    def onUp(self):
        pass

    # 向下键和滚轮向下
    # ----------------------------------------------------------------------
    def onDown(self):
        pass

    # 向左键
    # ----------------------------------------------------------------------
    def onLeft(self):
        pass

    # 向右键
    # ----------------------------------------------------------------------
    def onRight(self):
        pass

    # 鼠标左单击
    # ----------------------------------------------------------------------
    def onLClick(self, pos):
        pass

    # 鼠标右单击
    # ----------------------------------------------------------------------
    def onRClick(self, pos):
        pass

    # 鼠标左释放
    # ----------------------------------------------------------------------
    def onLRelease(self, pos):
        pass

    # 鼠标右释放
    # ----------------------------------------------------------------------
    def onRRelease(self, pos):
        pass

    # 画图
    # ----------------------------------------------------------------------
    def onPaint(self):
        pass
