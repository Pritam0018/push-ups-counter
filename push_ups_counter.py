import cv2
import time
import cvzone
import numpy as np
from cvzone.PoseModule import PoseDetector
cap=cv2.VideoCapture(0)
detector=PoseDetector()
ptime=0
ctime=0
push_ups=0
color=(0,0,255)
dir=0

while True:
    _,img=cap.read()
    img=detector.findPose(img)
    lmList,bbox=detector.findPosition(img,draw=False)
    if lmList:
            a1, img = detector.findAngle(lmList[11][0:2],
                                        lmList[13][0:2],
                                        lmList[15][0:2],
                                        img=img,
                                        color=(0, 0, 255),
                                        scale=10)
            a2, img = detector.findAngle(lmList[16][0:2],
                                        lmList[14][0:2],
                                        lmList[12][0:2],
                                        img=img,
                                        color=(0, 0, 255),
                                        scale=10)
            per_val1=int(np.interp(a1,(75,175),(100,0)))
            per_val2=int(np.interp(a2,(75,175),(100,0)))
            bar_val1=int(np.interp(per_val1,(0,100),(40+350,40)))
            bar_val2=int(np.interp(per_val2,(0,100),(40+350,40)))
            cv2.rectangle(img,(570,bar_val1),(570+35,40+350),color,cv2.FILLED)
            cv2.rectangle(img,(570,40),(570+35,40+350),(),3)
            cv2.rectangle(img,(35,bar_val2),(35+35,40+350),color,cv2.FILLED)
            cv2.rectangle(img,(35,40),(35+35,40+350),(),3)
            if per_val1==100 and per_val2==100:
                 if dir==0:
                      push_ups+=0.5
                      dir=1
                      color=(0,255,0)
            elif per_val1==0 and per_val2==0:
                 if dir==1:
                      push_ups+=0.5
                      dir=0
                      color=(0,255,0)  
            else:
                 color=(0,0,255) 
            cvzone.putTextRect(img,f'push_ups : {int(push_ups)}',(209,35),2,2,colorT=(255,255,255),colorR=(255,0,0),border=3,colorB=())                    
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cvzone.putTextRect(img,f'FPS-{int(fps)}',(270,80),2,2,colorT=(255,255,255),colorR=(255,0,0),border=3,colorB=())

    cv2.imshow("push-ups counter",img)
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == ord('q'):
        break
