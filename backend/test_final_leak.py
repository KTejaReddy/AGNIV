import mss
import psutil, os
import cv2
import numpy as np
import gc

p = psutil.Process(os.getpid())
start = p.memory_info().rss

sct = mss.mss()
monitor_idx = 1
monitor = sct.monitors[monitor_idx]

for i in range(1000):
    sct_img = sct.grab(monitor)
    img = np.array(sct_img)
    latest_frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    # explicit deletion
    del sct_img
    del img
    
    if i % 30 == 0:
        gc.collect()

print('Leak:', p.memory_info().rss - start)
