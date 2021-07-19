# RealTimeSuperResolution
### Cost Optimised Video Transfer
----------------------------------------------------

To run this code, please put the client module on the source of the video and the server module on the destination. The destination can also be GDrive in case colab is being used. The upload file has to be changed to drive.py in case of upload to GDrive and the credentials.json and tokens.pickla have to provided. In case the upload is not to GDrive then the .pem file for the server has to be provided. On both destintation and client, their respective dependencies from requirements must be installed. Then on the client run: 
```
$ python opt.py <path_to_video>
```
If the upload is to GDrive path to uploaded zip is not required on the server side:
```
$ python serv.py
```
