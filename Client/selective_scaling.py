import cv2 
import imutils
import numpy as np
import pandas as pd
import sys
from skimage.measure import compare_ssim
import time
import json
import os 

def decode_fourcc(v):
  v = int(v)
  return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

def find_send(x, y, w, h, send_dict, image_dict):
    rect_point_list = [(x,y),(x+w,y),(x,y+h),(x+w, y+h)]
    keys = list(image_dict.keys())
    for i in rect_point_list:
        for j in keys:
            if((i[0] > image_dict[j][0][1] and i[0] < image_dict[j][1][1]) and ( i[1] > image_dict[j][0][0] and i[1] < image_dict[j][1][0])) :
                send_dict[j] = 1
    return send_dict

def blur_and_show_bro(old_frame,send_dict,image_dict,height,width,fc,scale):
    cp = 1
    for i in list(send_dict.keys()):
        if(send_dict[i]==1):
            start_row,start_col = image_dict[i][0][0], image_dict[i][0][1]
            end_row, end_col = image_dict[i][1][0], image_dict[i][1][1]
            temp_image = old_frame[start_row:end_row, start_col:end_col]
            # print(temp_image.shape)
            if(scale != 1):
                temp_image = cv2.resize(temp_image, (428//scale, 360//scale), interpolation = cv2.INTER_AREA)
            fil = fold+"tes/Frame" + str(fc) + "_" + str(cp) +  ".jpg"
            tex =  "Frame" + str(fc) + "_" + str(cp) +  ".jpg" + "|" + json.dumps(image_dict[i]) + "\n"
            f.write(tex)
            out.write(temp_image)
            cv2.imwrite(fil,temp_image)
            cp = cp + 1
    return old_frame



video = cv2.VideoCapture(sys.argv[1])
scale = int(sys.argv[2])
fold = sys.argv[3]
fps = inp.get(cv2.CAP_PROP_FPS)
cod = decode_fourcc(inp.get(cv2.CAP_PROP_FOURCC))
os.system("mkdir "+fold+"tes")
f = open(fold + "/map.txt","w")
if(not video.isOpened()):
    print("Could not open video")
    sys.exit()
skip = 1
skipped = 0
ok, old_frame = video.read()
height, width = old_frame.shape[:2]
ref1 = cv2.resize(old_frame, (1280//scale, 720//scale),interpolation = cv2.INTER_AREA)
cv2.imwrite(fold+"/ref.jpg",ref1)
if(not ok):
    print('Cannot read video file')
    sys.exit()
fgbg = cv2.createBackgroundSubtractorMOG2()
flag = 0
# image_dict = {
#         1:[(0, 0),(height//2, width//3)],
#         2:[(0, width//3),(height//2, 2*width//3)],
#         3:[(0, 2*width//3),(height//2, width)],
#         4:[(height//2,0),(height, width//3)],
#         5:[(height//2, width//3),(height, 2*width//3)],
#         6:[(height//2, 2*width//3), (height, width)]
# }
image_dict = {
        1:[(0, 0),(360, 428)],
        2:[(0, 424),(360, 852)],
        3:[(0, 852),(360, 1280)],
        4:[(360,0),(720, 428)],
        5:[(360, 424),(720, 852)],
        6:[(360, 852), (720, 1280)]
}
# print(image_dict)
if scale == 1:
    out = cv2.VideoWriter(fold+"/res."+os.path.splitext(os.path.basename(sys.argv[1]))[1],cv2.VideoWriter_fourcc(*cod), fps, (428,360))
else:
    out = cv2.VideoWriter(fold+"/res."+os.path.splitext(os.path.basename(sys.argv[1]))[1],cv2.VideoWriter_fourcc(*cod), fps, (428//scale,360//scale))
tot_count = 0
frame_count = 0
while True:
    # time.sleep(1)
    # cv2.line(old_frame, (width//3, 0),(width//3, height), (0,255,0))
    # cv2.line(old_frame, (2*width//3, 0),(2*width//3, height), (0,255,0))
    # cv2.line(old_frame, (0, height//2),(width, height//2), (0,255,0))
    ok, new_frame = video.read()
    if not ok:
        print('Video Processed')
        sys.exit()
    send_dict = {
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0
    }
    gray_old = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    gray_new = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray_old)
    (im2, contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 50:
            continue
            
        #get bounding box from countour
        (x, y, w, h) = cv2.boundingRect(c)
        """crop_img = old_frame[y:y+h, x:x+w]
                                cv2.imshow("cropped",crop_img)"""
        #draw bounding box
        send_dict = find_send(x, y, w, h , send_dict, image_dict)
        # cv2.rectangle(old_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # print(send_dict)
    old_frame = blur_and_show_bro(old_frame,send_dict,image_dict,height,width,frame_count,scale)
    count = 0
    for i in list(send_dict.keys()):
        if(send_dict[i]==1):
            count+=1
    tot_count += count
    frame_count += 1 
    tot_sent = int(tot_count/(6*frame_count)*100)
    tot_savings = 100-tot_sent
    savings = int((len(send_dict)-count)/len(send_dict)*100)
    # cv2.putText(old_frame, "Number of sections to be sent:"+str(count), (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
    # cv2.putText(old_frame, "Percentage savings in this frame:"+str(savings), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
    # cv2.putText(old_frame, "Total savings over all frames so far:"+str(tot_savings), (20,70), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
    # cv2.imshow("Old Frame", old_frame)
    # cv2.imshow("New Frame", new_frame)
    #cv2.imshow("Diff", diff)
    #cv2.imshow("Thresh", thresh)
    # cv2.waitKey(25)
    old_frame = new_frame
video.release()
