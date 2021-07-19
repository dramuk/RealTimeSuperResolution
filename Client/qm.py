import cv2 
import imutils
import numpy as np
import pandas as pd
import sys
from skimage.measure import compare_ssim
import time

def variance_of_laplacian(image, img1):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	t = cv2.Laplacian(image, cv2.CV_64F) 
	t1 = t - cv2.Laplacian(img1, cv2.CV_64F)
	tll = 100 * (np.size(t1[(t1 >= 5) | (t1 <= -5)])/2 + np.size(t[(t >= 5) | (t <= -5)])/2)/np.size(t[t!=0])
	tll = tll + (100 - tll)//2
	return tll

video = cv2.VideoCapture(sys.argv[1])
if(not video.isOpened()):
	print("Could not open video")
	sys.exit()
ok, old_frame = video.read()

if(not ok):
	print('Cannot read video file')
	sys.exit()
height, width = old_frame.shape[:2]
fgbg = cv2.createBackgroundSubtractorMOG2()
flag = 0
fm = 0
fc = 0
while True:
	#time.sleep(1)
	fc = fc + 1
	ok, new_frame = video.read()
	if not ok:
		break;
	gray_old = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
	gray_new = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
	fm = fm + variance_of_laplacian(gray_new, gray_old)
	old_frame = new_frame
fm = fm / fc
print("Quality = ",fm)
video.release()