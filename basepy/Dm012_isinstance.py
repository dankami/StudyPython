# -*- coding: utf-8 -*-

class Myclass:
    pass

if __name__ == '__main__':
    print 'hello'
    test = Myclass()
    # 检查一个变量是否为此类型
    print isinstance(test, Myclass)