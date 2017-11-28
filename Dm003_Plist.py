# -*- coding: UTF-8 -*-
# 先安装biplist
from mylib.biplist import *

#写入
# plist = {'aKey':'aValue',
#          '0':1.322,
#          'now':datetime.now(),
#          'list':[1,2,3],
#          'tuple':('a','b','c')
#          }
# try:
#     writePlist(plist, "res/dm03/example.plist", False)
# except (InvalidPlistException, NotBinaryPlistException), e:
#     print "Something bad happened:", e

#读取
try:
    plist = readPlist("res/dm03/hall_res_1.plist")
    print type(plist)
    print plist
    frames = plist.get('frames')
    print frames.keys()
except (InvalidPlistException, NotBinaryPlistException), e:
    print "Not a plist:", e