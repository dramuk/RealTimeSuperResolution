# RealTimeSuperResolution
### Cost Optimised Video Transfer
----------------------------------------------------
This repository deals with implementaion of our novel paper on cost optimized video data transfer and the same can be accessed at 
https://www.academia.edu/50064092/Cost_Optimized_Video_Transfer_using_Real_Time_Super_Resolution_Convolutional_Neural_Networks

To run this code, please put the client module on the source of the video and the server module on the destination. The destination can also be GDrive in case colab is being used. The upload file has to be changed to drive.py in case of upload to GDrive and the credentials.json and tokens.pickla have to provided. In case the upload is not to GDrive then the .pem file for the server has to be provided. On both destintation and client, their respective dependencies from requirements must be installed. Then on the client run: 
```
$ python opt.py <path_to_video>
```
If the upload is to GDrive path to uploaded zip is not required on the server side:
```
$ python serv.py
```


@inproceedings{dramuk,
author = {Lodha, Ishaan, Kolur, Lakshana, Krishnan, Krishnan, Dheenadayalan, Kumar, Sitaram, Dinkar, and Nandi, Sidhartha},
title = {Cost Optimized Video Transfer Using Real Time Super Resolution Convolutional Neural Networks},
year = {2022},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
booktitle = {9th ACM IKDD CODS and 27th COMAD},
numpages = {9},
location = {Bangalore, India},
series = {CODS COMAD 2022}
}
