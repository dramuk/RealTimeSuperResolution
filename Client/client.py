import sys
import os
import cv2
import time 


if __name__ == '__main__':
    # st = time.time()
    # main(sys.argv[1])
    # t = time.time() - st
    # print("Time taken to upload =", t, "seconds")
    vid = sys.argv[1]
    scale = sys.argv[2]
    sel = sys.argv[3]
    inp = cv2.VideoCapture(vid)
    siz = os.stat(vid).st_size
    siz = siz*inp.get(cv2.CAP_PROP_FPS)/inp.get(cv2.CAP_PROP_FRAME_COUNT)
    siz = siz/(1024)
    print("Bitrate =", siz, 'KB/s')
    le = inp.get(cv2.CAP_PROP_FRAME_COUNT)/inp.get(cv2.CAP_PROP_FPS)
    print("Length =", le ,"s")
    st = time.time()
    os.system("mkdir temp")
    print(os.path.basename(vid) + " " + scale + " " + sel)
    f = open("temp/conf.txt","w")
    f.write(os.path.basename(vid) + " " + scale + " " + sel)
    f.close()
    if scale is '1' and sel is 'N':
        os.system("cp " + vid + " " + "temp/")
    elif sel is "N":
        os.system("python3 down.py " + vid + " " + scale + " temp")
    else:
        os.system("python3 selective_scaling.py " + vid + " " + scale + " temp")
        os.system("zip -r -q -X temptes.zip temptes")
    os.system("zip -r -q -X temp.zip temp")
    t = time.time() - st
    print("Time taken to process =", t/2, "seconds")
    print("Size of Original Video =",os.stat(vid).st_size/1024,"KB")
    print("Size of Total Upload =",os.stat("temp.zip").st_size/1024,"KB")
    # os.system("python3 qm.py " + vid)
    print("Uploading")
    st = time.time()
    os.system("python3 upload.py temp.zip")
    t = time.time() - st
    print("Time taken to upload =", t, "seconds")
    if sel is 'Y':
        main("temptes.zip")
        os.system("rm -rf temptes")
        os.system("rm temptes.zip")
    os.system("rm -rf temp")
    os.system("rm temp.zip")


    