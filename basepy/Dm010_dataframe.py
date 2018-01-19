# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

if __name__ == "__main__":
    df = pd.DataFrame([1, 2, 3, 4, 5], columns=['cols'], index=['a', 'b', 'c', 'd', 'e'])
    print df

    df2 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], columns=['col1', 'col2', 'col3'], index=['a', 'b', 'c', 'd'])
    print df2

    df3 = pd.DataFrame(np.array([[1, 2], [3, 4]]), columns=['col1', 'col2'], index=['a', 'b'])
    print df3

    df4 = pd.DataFrame({'col1': [1, 3], 'col2': [2, 4]}, index=['a', 'b'])
    print df4

    # 基本操作
    print df2.index
    print df2.columns

    # 访问多行数据，索引参数为一个列表对象
    print df2.loc[['a', 'c']]
    print df2.loc[df2.index[1:3]]

    # 访问列数据
    print df2[['col1', 'col3']]


    #### 计算 #####

    # DataFrame元素求和
    # 默认是对每列元素求和
    print df2.sum()
    # 行求和
    print df2.sum(1)

    # 对每个元素乘以２
    print df2.apply(lambda x: x * 2)

    # 对每个元素求平方(支持ndarray一样的向量化操作)
    print df2 ** 2


    ### 列扩充 ####
    # 对DataFrame对象进行列扩充
    df2 = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['col1', 'col2', 'col3'], index=['a', 'b'])
    df2['col4'] = ['cnn', 'rnn']
    print df2

    # 也可以通过一个新的DataFrame对象来定义一个新列,索引自动对应
    addData = pd.DataFrame(['MachineLearning', 'DeepLearning'], index=['a', 'b'])
    df2['col5'] = addData
    print addData
    print df2

    ### 行扩充 ###
    # 行进行扩充
    print df2.append(
        pd.DataFrame({'col1': 7, 'col2': 8, 'col3': 9, 'col4': 'rcnn', 'col5': 'ReinforcementLearning'}, index=['c']))


    ### 注意！###
    # 如果在进行　行扩充时候没有，指定ｉｎｄｅｘ的参数，索引会被数字取代
    print df2.append({'col1': 10, 'col2': 11, 'col3': 12, 'col4': 'frnn', 'col5': 'DRL'}, ignore_index=True)

    # 以上的行扩充，并没有真正修改，df2这个DataFrame对象，除非
    df2 = df2.append(
        pd.DataFrame({'col1': 7, 'col2': 8, 'col3': 9, 'col4': 'rcnn', 'col5': 'ReinforcementLearning'}, index=['c']))
    print df2

    print df2.loc[['a']]

    ### DataFrame对象的合并 ###
    # DataFrame 对象的合并
    df_a = pd.DataFrame(['wang', 'jing', 'hui', 'is', 'a', 'master'], columns=['col6'],
                        index=['a', 'b', 'c', 'd', 'e', 'f'])
    print df_a
    # 默认合并,只保留dfb中的全部索引
    dfb = pd.DataFrame([1, 2, 4, 5, 6, 7], columns=['col1'], index=['a', 'b', 'c', 'd', 'f', 'g'])
    print dfb.join(df_a)

    # 默认合并之接受索引已经存在的值
    # 通过指定参数 how，指定合并的方式
    print dfb.join(df_a, how='inner')  # 合并两个DataFrame对象的交集

    # 合并两个DataFrame对象的并集
    print dfb.join(df_a, how='outer')

    # 列太多时，打印会分行
    testdf = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4']], columns=['open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change', 'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'turnover'], index=['1'])
    print testdf
