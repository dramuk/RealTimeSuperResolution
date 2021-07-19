import cv2
import numpy as np
import glob
import sys
import re
 
img_array = []
fl = glob.glob(sys.argv[1]+"/*.jpg")
def sorted_nicely( l ):
  	convert = lambda text: int(text) if text.isdigit() else text
  	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
  	return sorted(l, key = alphanum_key)
c = 1
fl = sorted_nicely(fl)
size = ()
for filename in fl:
	img = cv2.imread(filename)
	height, width, layers = img.shape
	img_array.append(img)
	size = (width,height)
	c = c + 1

out = cv2.VideoWriter(sys.argv[2],cv2.VideoWriter_fourcc(*'H264'), 30, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()