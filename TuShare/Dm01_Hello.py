# -*- coding: utf-8 -*-

import tushare as ts

if __name__ == '__main__':
    data = ts.get_hist_data('600104')  # 一次性获取全部日k线数据
    print data
    data.to_csv('600104.csv')
    data.to_json('600104.json')
    data.to_excel('600104.xlsx')