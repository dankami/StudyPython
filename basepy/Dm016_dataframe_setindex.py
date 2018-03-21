#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

from pandas import DataFrame
import pandas as pd
import numpy as np


#脚本语言没有真正的入口，所以用__name__来区分。否则在被包含时就被执行
if __name__ == '__main__':
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], columns=['col1', 'col2', 'col3'],
                       index=['a', 'b', 'c', 'd'])
    print df
    print '用col1替换index'
    df = df.set_index(df['col1'])
    print df