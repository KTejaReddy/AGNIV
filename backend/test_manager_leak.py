import mss
import psutil, os
import cv2
import numpy as np

p = psutil.Process(os.getpid())
sct = mss.mss()
start = p.memory_info().rss

for _ in range(1000):
    monitor = sct.monitors[1]
    sct_img = sct.grab(monitor)
    img = np.array(sct_img)
    latest_frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

print('Leak:', p.memory_info().rss - start)
