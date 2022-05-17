import timeit
from time import perf_counter as pc

c = {'id': 123, 'a': 'test', 'b': 567}
for i in range(1,1000000):
    c[str(i)] = 'test'

def f1():
    global c
    if '23543' in c: return True

	
def f2():
    global c
    if '53543' in c and '4213' in c: return True

print(f1())
print(f2())

# first way
print(timeit.timeit('f1()', 'from __main__ import f1', number=100000))
print(timeit.timeit('f2()', 'from __main__ import f2', number=100000))

# second way
t0 = pc()
for i in range(100000):
    f1()
print(pc()-t0)
