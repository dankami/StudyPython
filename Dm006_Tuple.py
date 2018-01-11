#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

if __name__ == "__main__":
    print("hello")
    tuple = (1, 2, 3, "adb") #只读
    print(tuple[1])
    print(tuple[-1])
    print(tuple[-2])
    # tuple[1] = 3 #报错