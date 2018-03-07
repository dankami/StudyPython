# -*- coding: utf-8 -*-

import datetime
import time

# '2015-08-28 16:43:37.283' --> 1440751417.283
# 或者 '2015-08-28 16:43:37' --> 1440751417.0
def string2timestamp(strValue):
    try:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        print timeStamp
        return timeStamp
    except ValueError as e:
        print e
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        print timeStamp
        return timeStamp

# 1440751417.283 --> '2015-08-28 16:43:37.283'
def timestamp2string(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        # 2015-08-28 16:43:37.283000'
        return str1
    except Exception as e:
        print e
        return ''

''' 时间戳格式化说明
python中时间日期格式化符号：
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
'''


if __name__ == '__main__':
    print '================ 时间戳 ==============='
    # 时间戳
    print "time.time(): %f " % time.time()  #float
    lt = time.localtime(time.time()) #时间元组
    print lt
    asct = time.asctime(lt)  # 字符串
    print asct

    # 格式化成2016-03-20 11:45:39形式
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 格式化成Sat Mar 28 22:24:24 2016形式
    print time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())

    # 将格式字符串转换为时间戳
    a = "Sat Mar 28 22:24:24 2016"
    print time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y"))

    print time.mktime(time.strptime('2017-01-01', '%Y-%m-%d'))

    # 字期
    print '============== 字期 =============='
    i = datetime.datetime.now()
    print ("当前的日期和时间是 %s" % i)
    print ("ISO格式的日期和时间是 %s" % i.isoformat())
    print ("当前的年份是 %s" % i.year)
    print ("当前的月份是 %s" % i.month)
    print ("当前的日期是  %s" % i.day)
    print ("dd/mm/yyyy 格式是  %s/%s/%s" % (i.day, i.month, i.year))
    print ("当前小时是 %s" % i.hour)
    print ("当前分钟是 %s" % i.minute)
    print ("当前秒是  %s" % i.second)


