import mss
import psutil, os

p = psutil.Process(os.getpid())
sct = mss.mss()
monitor = sct.monitors[1]
start = p.memory_info().rss

def f():
    s = sct.grab(monitor)
    del s

for _ in range(1000):
    f()

print('Leak:', p.memory_info().rss - start)
