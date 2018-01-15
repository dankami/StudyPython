#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

import numpy as np

if __name__ == "__main__":
    print np.version.version

    print np.array([1, 2, 3, 4])
    print np.array((1.2, 2, 3, 4))
    print type(np.array((1.2, 2, 3, 4)))

    print np.array([[1, 2], [3, 4]])
    print np.array((1.2, 2, 3, 4), dtype=np.int32)

    print np.arange(15)
    print type(np.arange(15))
    print np.linspace(1, 3, 9)

    print np.zeros((3, 4))
    print np.ones((3, 4))
    print np.eye(3)

    testNp = np.zeros((2, 2, 2))
    print testNp
    print testNp.ndim  # 数组的维数
    print testNp.shape
    print testNp.size
    print testNp.dtype
    print testNp.itemsize