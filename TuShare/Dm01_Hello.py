# -*- coding: utf-8 -*-

import tushare as ts

def saveHistData(_code):
    print '下载：', _code
    data = ts.get_hist_data(_code)  # 一次性获取全部日k线数据
    if not data is None:
        print '保存：', _code
        data.to_csv('hist/%s.csv'%(_code))
        print '保存完成'

def saveQHistData(_code):
    print '下载：', _code
    data = ts.get_hist_data(_code)  # 一次性获取全部日k线数据
    if not data is None:
        print '保存：', _code
        data.to_csv('qhist/%s.csv'%(_code))
        print '保存完成'

if __name__ == '__main__':
    for i in range(1000):
        saveHistData('000%03d' % (i))
        saveHistData('001%03d' % (i))
        saveHistData('002%03d' % (i))
        saveHistData('600%03d' % (i))
        saveHistData('601%03d' % (i))
        saveHistData('603%03d' % (i))

        # saveQHistData('000%03d' % (i))
        # saveQHistData('001%03d' % (i))
        # saveQHistData('002%03d' % (i))
        # saveQHistData('600%03d' % (i))
        # saveQHistData('601%03d' % (i))
        # saveQHistData('603%03d' % (i))

