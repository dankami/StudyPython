#coding=utf-8

import tushare as ts

if __name__ == '__main__':
    print(ts.__version__)
    df = ts.get_hist_data('000001')
    df.to_json("res/MoneyMachine/000001.json")
    df.to_excel("res/MoneyMachine/000001.xlsx")
    print("下载数据完成")

    # # 获取大盘大概数据
    # df = ts.get_index()
    # print(df)

