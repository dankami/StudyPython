# -*- coding: utf-8 -*-
import pandas as pd
import tushare as ts

def get3DayAmountDF(_code):

    data = ts.get_hist_data(_code, start = '2018-02-26', end = '2018-02-28') #autype=None
    if not data is None:
        amount = data.sum().open
        return pd.DataFrame([[amount]], columns=['3amount'], index=[_code])
    return None

if __name__ == '__main__':
    amountDF = pd.DataFrame()
    # 深股
    for i in range(1000):
        print 'getData...'
        df = get3DayAmountDF('000%03d' % (i))
        if not df is None:
            amountDF = amountDF.append(df)

    # for i in range(1000):
    #     print '001%03d' % (i)
    # for i in range(1000):
    #     print '002%03d' % (i)
    # # 沪股
    # for i in range(1000):
    #     print '600%03d' % (i)
    # for i in range(1000):
    #     print '601%03d' % (i)
    # for i in range(1000):
    #     print '603%03d' % (i)
    print amountDF

