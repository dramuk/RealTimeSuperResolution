import sys
import os
import cv2
import numpy as np
import json 


os.system("unzip -q temp.zip")
os.system("rm temp.zip")
f = open("temp/conf.txt")
conf = f.read()
conf = conf.split(" ")

os.system("mkdir temp2")
os.system("mkdir temp1")

if(conf[2] is "N" and conf[1] is '1'):
	os.system("cp " + "temp/"+conf[0] + " ./"+conf[0])
	os.system("rm -rf temp")
	os.system("rm -rf temp2")
	os.system("rm -rf temp1")
	sys.exit()

elif(conf[2] is "Y"):
	os.system("unzip -q temptes.zip")
	os.system("rm temptes.zip")
	if conf[1] is '1':
		os.system("cp -a temp/*.jpg temp2")
		os.system("cp -a temptes/*.jpg temp2")
	else:
		os.system("python ups.py temp " + conf[1] + " temp2")
	fl = open("temp/map.txt")
	ref = cv2.imread("temp/ref.jpg")
	frm = 2
	cv2.imwrite("temp1/frame0.jpg", ref)
	for line in fl:
		s = line.split("|")
		fc = int(s[0][5:-6])
		if(fc == frm):
			cv2.imwrite("temp1/frame" + str(fc-1) + ".jpg",ref)
			frm = frm + 1
		if(fc < frm):
			tp = json.loads(s[1])
			# print(tp)
			# print(s[0])
			ref[int(tp[0][0]):int(tp[1][0]), int(tp[0][1]):int(tp[1][1])] = cv2.imread("temp2/"+s[0])
	cv2.imwrite("temp1/frame" + str(fc) + ".jpg",ref)
		

else:
	inp = cv2.VideoCapture("temp/res.mp4")
	ok = True
	fc = 1
	while ok:
		ok, new_frame = inp.read()
		cv2.imwrite("temp2/frame" + int(fc) + ".jpg", new_frame)
		fc = fc + 1
	os.system("python ser.py")

os.system("rm -rf temp")
os.system("rm -rf temptes")
os.system("rm -rf temp2")

os.system("python vid.py temp1 " + conf[0] )
os.system("rm -rf temp1")

	
