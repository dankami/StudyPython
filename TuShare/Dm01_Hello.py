# -*- coding: utf-8 -*-

import tushare as ts
import os
import time

# 根据股票编号保存K线历史数据
def saveHistData(_code):
    print '下载：', _code
    data = ts.get_hist_data(_code)  # 一次性获取全部日k线数据
    if not data is None:
        print '保存：', _code
        data.to_csv('hist/%s.csv'%(_code))
        print '保存完成'

# 根据目标文件夹下文件名保存K线复权数据
def saveQHistDataByDir(filepath, _startCode = 0):
#遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath,fi)
        if os.path.isdir(fi_d):
            saveQHistDataByDir(fi_d, _startCode)
        else:
            code = fi[0:len(fi)-4]
            if int(code) > int(_startCode):
                saveQHistData(code)


# 根据股票编号保存K线复权数据
def saveQHistData(_code):
    print '下载：', _code
    try:
        data = ts.get_h_data(_code, start='2017-01-01', end='2018-03-08')  # 获取前复权数据
    except IOError:
        print "Error: 什么鬼，不能连续下载的？等下重新下载看看"
        for i in range(120):
            time.sleep(1)
            print '等待时间：%d' % (i + 1)
        saveQHistData(_code)
    else:
        if not data is None:
            print '保存：', _code
            data.to_csv('qhist/%s.csv' % (_code))
            print '保存完成'



if __name__ == '__main__':
    # for i in range(1000):
        # saveHistData('000%03d' % (i))
        # saveHistData('001%03d' % (i))
        # saveHistData('002%03d' % (i))
        # saveHistData('600%03d' % (i))
        # saveHistData('601%03d' % (i))
        # saveHistData('603%03d' % (i))

    # data = ts.get_h_data('002337')  # 一次性获取全部日k线数据
    # print data
    # saveQHistDataByDir('hist', '600004')

    # data = ts.get_h_data('600005', start='2017-01-01', end='2018-03-08')


    print '三安光电 股票统计'
    data = ts.get_hist_data('600703')
    print data
    allRow = len(data)
    print '一共交易：', allRow
    zeroCount = float(0)
    oneCount = float(0)
    towCount = float(0)
    threeCount = float(0)
    fourCount = float(0)
    fiveCount = float(0)
    sixCount = float(0)
    sevenCount = float(0)
    eightCount = float(0)
    nineCount = float(0)
    tenCount = float(0)
    nZeroCount = float(0)
    nOneCount = float(0)
    nTowCount = float(0)
    nThreeCount = float(0)
    nFourCount = float(0)
    nFiveCount = float(0)
    nSixCount = float(0)
    nSevenCount = float(0)
    nEightCount = float(0)
    nNineCount = float(0)
    nTenCount = float(0)

    # testlist = [-11, -9, -8, -7, -6, -5, -4, -3, -2, -1, -0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # for t in testlist:
    #     p_change = t
    for index in data.index:
        p_change = data.loc[index].p_change

        if p_change <= -10:
            nTenCount = nTenCount + 1

        if p_change <= -9 and p_change > -10:
            nNineCount = nNineCount + 1

        if p_change <= -8 and p_change > -9:
            nEightCount = nEightCount + 1

        if p_change <= -7 and p_change > -8:
            nSevenCount = nSevenCount + 1

        if p_change <= -6 and p_change > -7:
            nSixCount = nSixCount + 1

        if p_change <= -5 and p_change > -6:
            nFiveCount = nFiveCount + 1

        if p_change <= -4 and p_change > -5:
            nFourCount = nFourCount + 1

        if p_change <= -3 and p_change > -4:
            nThreeCount = nThreeCount + 1

        if p_change <= -2 and p_change > -3:
            nTowCount = nTowCount + 1

        if p_change <= -1 and p_change > -2:
            nOneCount = nOneCount + 1

        if p_change < 0 and p_change > -1:
            nZeroCount = nZeroCount + 1

        if p_change >= 0 and p_change < 1:
            zeroCount = zeroCount + 1

        if p_change >= 1 and p_change < 2:
            oneCount = oneCount + 1

        if p_change >= 2 and p_change < 3:
            towCount = towCount + 1

        if p_change >= 3 and p_change < 4:
            threeCount = threeCount + 1

        if p_change >= 4 and p_change < 5:
            fourCount = fourCount + 1

        if p_change >= 5 and p_change < 6:
            fiveCount = fiveCount + 1

        if p_change >= 6 and p_change < 7:
            sixCount = sixCount + 1

        if p_change >= 7 and p_change < 8:
            sevenCount = sevenCount + 1

        if p_change >= 8 and p_change < 9:
            eightCount = eightCount + 1

        if p_change >= 9 and p_change < 10:
            nineCount = nineCount + 1

        if p_change >= 10:
            tenCount = tenCount + 1

    # print 'tenCount = ', tenCount
    # print 'nineCount = ', nineCount
    # print 'eightCount = ', eightCount
    # print 'sevenCount = ', sevenCount
    # print 'sixCount = ', sixCount
    # print 'fiveCount = ', fiveCount
    # print 'fourCount = ', fourCount
    # print 'threeCount = ', threeCount
    # print 'towCount = ', towCount
    # print 'oneCount = ', oneCount
    # print 'zeroCount = ', zeroCount
    # print 'nZeroCount = ', nZeroCount
    # print 'nOneCount = ', nOneCount
    # print 'nTowCount = ', nTowCount
    # print 'nThreeCount = ', nThreeCount
    # print 'nFourCount = ', nFourCount
    # print 'nFiveCount = ', nFiveCount
    # print 'nSixCount = ', nSixCount
    # print 'nSevenCount = ', nSevenCount
    # print 'nEightCount = ', nEightCount
    # print 'nNineCount = ', nNineCount
    # print 'nTenCount = ', nTenCount

    print '10% = ', tenCount/allRow * 100 
    print ' 9% = ', nineCount/allRow * 100 
    print ' 8% = ', eightCount/allRow * 100 
    print ' 7% = ', sevenCount/allRow * 100 
    print ' 6% = ', sixCount/allRow * 100 
    print ' 5% = ', fiveCount/allRow * 100 
    print ' 4% = ', fourCount/allRow * 100 
    print ' 3% = ', threeCount/allRow * 100 
    print ' 2% = ', towCount/allRow * 100 
    print ' 1% = ', oneCount/allRow * 100 
    print ' 0% = ', zeroCount/allRow * 100 
    print ' -0% = ', nZeroCount/allRow * 100 
    print ' -1% = ', nOneCount/allRow * 100 
    print ' -2% = ', nTowCount/allRow * 100 
    print ' -3% = ', nThreeCount/allRow * 100 
    print ' -4% = ', nFourCount/allRow * 100 
    print ' -5% = ', nFiveCount/allRow * 100 
    print ' -6% = ', nSixCount/allRow * 100 
    print ' -7% = ', nSevenCount/allRow * 100 
    print ' -8% = ', nEightCount/allRow * 100 
    print ' -9% = ', nNineCount/allRow * 100 
    print '-10% = ', nTenCount/allRow * 100 

