#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

print '就算被包含也会执行，这是脚本语言的特性'

#脚本语言没有真正的入口，所以用__name__来区分。否则在被包含时就被执行
if __name__ == '__main__':
    print 'Hello world'