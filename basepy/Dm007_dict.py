#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

if __name__ == "__main__":
    dict = {}
    dict['one'] = "This is one"
    dict[2] = "This is two"

    tinydict = {'k1': 'john1', 'k2': 673.2, 'k3': 'sales3'}

    print dict['one']  # 输出键为'one' 的值
    print dict[2]  # 输出键为 2 的值
    print tinydict  # 输出完整的字典
    print tinydict.keys()  # 输出所有键
    print tinydict.values()  # 输出所有值