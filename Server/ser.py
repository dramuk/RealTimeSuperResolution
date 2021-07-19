import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Activation, Layer, Lambda, PReLU, BatchNormalization, Add
from tensorflow.keras import activations
from tensorflow.keras.optimizers import Adam
import glob
import re
import cv2
import random
from tensorflow.keras import backend as K
import numpy as np
import time
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


K.clear_session()

def sorted_nicely( l ):
  	convert = lambda text: int(text) if text.isdigit() else text
  	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
  	return sorted(l, key = alphanum_key)

def SSIM(y_true, y_pred):
  return tf.reduce_mean(tf.image.ssim(y_true, y_pred, 1.0)) 

def lossf(y_true, y_pred):
  return tf.reduce_mean(keras.losses.MSE(y_true, y_pred)) - tf.reduce_mean(tf.image.ssim(y_true, y_pred, 1.0))    

def PSNR(y_true, y_pred):
    max_pixel = 1.0
    return (10.0 * K.log((max_pixel ** 2) / (K.mean(K.square(y_pred - y_true), axis=-1)))) / 2.303
   
def gener(lr, hr, bs, li):
  print(len(lr))
  for p in range(li):
    r = [random.randrange(0, len(lr), 1) for i in range(bs)] 
    inp = []
    tar = []
    for i in r:
      inp.append(cv2.imread(lr[i])/255.0)
      tar.append(cv2.imread(hr[i])/255.0)
    yield(np.array(inp), np.array(tar))

def dat(lr, hr):
  inp = []
  tar = []
  for i in range(100):
    print(i)
    inp.append(cv2.imread(lr[i])/255.0)
    tar.append(cv2.imread(hr[i])/255.0)
  return(np.array(inp), np.array(tar))

model = Sequential()
model.add(Conv2D(64, 5, padding='same'))
model.add(PReLU(shared_axes=[1,2]))
model.add(Conv2D(64, 3, padding='same'))
model.add(PReLU(shared_axes=[1,2]))
model.add(Conv2D(64, 3, padding='same'))
model.add(PReLU(shared_axes=[1,2]))
model.add(Conv2D(48, 3, padding='same'))
model.add(PReLU(shared_axes=[1,2]))
model.add(Lambda(lambda x:tf.nn.depth_to_space(x,2)))
if conf[1] is '4':
  model.add(Conv2D(48, 3, padding='same'))
  model.add(PReLU(shared_axes=[1,2]))
  model.add(Lambda(lambda x:tf.nn.depth_to_space(x,2)))
model.add(Conv2D(3, 9, padding='same'))
opt = Adam(0.0001)

model.compile(optimizer=opt, loss=lossf, metrics=[PSNR, SSIM, "mean_squared_error"])

model.load_weights("./weights/model_w")

fd = "/content/drive/My Drive/temp/res.mp4"
vid = cv2.VideoCapture(fd)
vr = cv2.VideoWriter("/content/drive/My Drive/upx.mp4",cv2.VideoWriter_fourcc(*'MP4V'), 30, (vcap.get(4)*int(conf[1]), vcap.get(3)*int(conf[1])))
ok, new_frame = vid.read()
tn = time.time()
tp = 0
while ok:
  ti = time.time()
  n = model.predict(np.array([(new_frame/255)]))
  print(time.time() - ti)
  tp = tp + time.time() - ti
  vr.write((n[0]*255).astype(np.uint8))
  ok, new_frame = vid.read()
vr.release()
print(time.time() - tn)
print(tp)