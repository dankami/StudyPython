    
def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:",res)
g = foo()
print(next(g))
print("*"*20)
print(next(g))

def consume():
    while True:
        number = yield
        print("开始消费", number)
        
consumer = consume()
next(consumer)
for num in range(0, 100):
    print("开始生产", num)
    consumer.send(num)
