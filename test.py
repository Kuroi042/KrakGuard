import cv2
import time
import numpy as np
from ultralytics import YOLO
path =  "source/vid.mp4"
model  =  YOLO("yolo11n.pt")
class_name = model.names #* return a dictionary of yolo class index 
#* boxes.xyxy → WHERE
#* boxes.conf → HOW CONFIDENT
#* boxes.cls  → WHAT CLASS



newtime = 0
prevtime =0
path =  "source/traf.mp4"

cap = cv2.VideoCapture(path)
fps = cap.get(cv2.CAP_PROP_FPS)
width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fourcc =  cv2.VideoWriter_fourcc(*'mp4v')
current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
out = cv2.VideoWriter('out.mp4',
                fourcc,
                fps,(width,height) )

traject = {}
while True:
    ret, frame =  cap.read()
    if not ret :
        break
    fps_text =  f"FPS : {int(fps)}"
    cv2.putText(frame, fps_text, (10,40),
                cv2.FONT_HERSHEY_SIMPLEX,1,
                 (200,0,0,),2,cv2.LINE_AA)
    results =  model.track(frame,persist=True, ) #*on the current frame
    for i in (results[0].boxes):
        conf =  float(i.conf[0])
        cord =  np.array(i.xyxy[0])
        x1,y1,x2,y2 =  cord
        CenterX =  int((x1+x2)/2) 
        CenterY = int((y1+y2)/2)  

        track_id =  int(i.id[0])
        if track_id not in traject:
            traject[track_id]=[]
        traject[track_id].append((CenterX,CenterY))
        cv2.circle(frame,(CenterX, CenterY),10,(0, 0, 225),-1)

        for track_id , points in traject.items():
            for j in range(1,len(points)):
                cv2.line(
                frame,
                points[j - 1],
                points[j],
                (0, 255, 0),
                2
            )
    new_frame =  results[0].plot()
   

    cv2.imshow('recording ... ',new_frame)
    out.write(new_frame)
    # frame_id+=1
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("Playback stopped by user.")
        break
cv2.destroyAllWindows()