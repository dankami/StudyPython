#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

from pandas import DataFrame
import pandas as pd
import numpy as np


#脚本语言没有真正的入口，所以用__name__来区分。否则在被包含时就被执行
if __name__ == '__main__':
    df = DataFrame(np.random.randn(4, 5), columns=['A', 'B', 'C', 'D', 'E'])
    print df
    df['Col_sum'] = df.apply(lambda x: x.sum(), axis=1)
    print df
    df.loc['Row_sum'] = df.apply(lambda x: x.sum())
    print df

    opeDf = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['col1', 'col2', 'col3'], index=['a', 'b'])
    print opeDf
    print opeDf['col1'].sum()


