#coding=utf-8

# 取款机
import tushare as ts

if __name__ == '__main__':

    # myData = ts.get_hist_data('600848')  # 一次性获取全部日k线数据
    # myData = ts.get_hist_data('600848', start='2015-01-05', end='2015-01-09') # 设定时间
    # myData = ts.get_hist_data(code = 'hs300')
    # print(myData)
    df = ts.get_tick_data('601398', date='2018-01-02')
    # print(df.head(10))

    bAmount = 0
    sAmount = 0
    xAmount = 0
    allAmount = 0
    dfLen = len(df)
    for i in range(dfLen):
        moneyData = df.iloc[i]
        allAmount = allAmount + moneyData.amount
        if moneyData.type == "买盘" :
            bAmount = bAmount + moneyData.amount
        elif moneyData.type == "卖盘":
            sAmount = sAmount + moneyData.amount
        else:
            xAmount = xAmount + moneyData.amount

    print(allAmount)
    print(sAmount + bAmount + xAmount)
    print(sAmount)
    print(bAmount)
    print(xAmount)





