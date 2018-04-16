#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

import pandas as pd

#脚本语言没有真正的入口，所以用__name__来区分。否则在被包含时就被执行
if __name__ == '__main__':
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], columns=['col1', 'col2', 'col3'],
                       index=['a', 'b', 'c', 'd'])

    print df
    print df[df.col1 > 1]
    print df[(df.col1 > 1) & (df.col1 < 10)]
    print df[df.index == 'a']
    list = ['a', 'b']
    print df[df.index.isin(list)]

    # 删除nan数据
    df.dropna(axis=1, how='all')  # 列，所有的去除
    df.dropna(axis=0, how='any')  # 行，只要一个就去除

