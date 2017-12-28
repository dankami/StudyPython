#coding=utf-8

# 取款机
from pyecharts import Bar

if __name__ == '__main__':
    import tushare as ts
    # myData = ts.get_hist_data('600848')  # 一次性获取全部日k线数据
    # myData = ts.get_hist_data('600848', start='2015-01-05', end='2015-01-09') # 设定时间
    # myData = ts.get_hist_data(code = 'hs300')
    # print(myData)

    bar = Bar("我的第一个图表", "这里是副标题")
    bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
    bar.show_config()
    bar.render()
