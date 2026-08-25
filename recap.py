from ultralytics import YOLO
import cv2
import numpy as np
Bar = [400,600] #0 , 1
model = YOLO("yolo11n.pt")
source ="source/traf.mp4"
cap =cv2.VideoCapture(source)
W=1020
H=720
which_side = {}
cv2.namedWindow('img')
while(True):
    ret, frame =  cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (W,H))
    result=  model.track(frame, persist=True)
    for i in result[0].boxes:
        seen = set()
        if not i.id[0]:
            continue
        trackid = int(i.id[0])
        x,y,x1,y1 =  map(int, i.xyxy[0])
        centery = int(y1)
        centerx =  int((x+x1)/2)
        # print(trackid, x,y,x1,y1)
        cv2.rectangle(frame, (x,y),(x1,y1),(225,0,0),1,cv2.LINE_8)
        seen.add(trackid)
        if centery >= Bar[1]: #600
            current = "bellow"
        elif centery <= Bar[0]: #400
            current ="above"
        else:
            current = "zone"
        
        previous  =  which_side.get(trackid)
        which_side[trackid] =  current
        

        print(trackid,centery ,which_side[trackid], previous)
        

    cv2.imshow('img',frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

    