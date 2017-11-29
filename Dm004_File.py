#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

import os
def gci(filepath):
#遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath,fi)
        if os.path.isdir(fi_d):
            gci(fi_d)
        else:
            print fi_d

if __name__ == "__main__":
    gci("res\dm04")
