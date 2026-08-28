import mss
import psutil, os

p = psutil.Process(os.getpid())
start = p.memory_info().rss

def capture():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct.grab(monitor)

for _ in range(1000):
    capture()

print("Leak:", p.memory_info().rss - start)
