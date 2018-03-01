# -*- coding: utf-8 -*-



lambFunc=lambda x:x+1

#以上lambda等同于以下函数
def func(x):
    return(x+1)

if __name__ == '__main__':
    print(func(1))
    # 2
    print(func(2))
    # 3

    print(lambFunc(1))
    # 2
    print(lambFunc(2))
    # 3

    #应用
    from functools import reduce

    foo = [2, 18, 9, 22, 17, 24, 8, 12, 27]

    print (list(filter(lambda x: x % 3 == 0, foo)))
    # [18, 9, 24, 12, 27]

    print (list(map(lambda x: x * 2 + 10, foo)))
    # [14, 46, 28, 54, 44, 58, 26, 34, 64]

    print (reduce(lambda x, y: x + y, foo))
    # 139