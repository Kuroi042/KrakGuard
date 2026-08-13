import cv2
import time
from ultralytics import YOLO
path =  "/home/kenshin/Desktop/DataProject/dvr/vid.mp4"
model  =  YOLO("yolo11n.pt")
class_name = model.names #* return a dictionary of yolo class index 
#* boxes.xyxy → WHERE
#* boxes.conf → HOW CONFIDENT
#* boxes.cls  → WHAT CLASS



newtime = 0
prevtime =0
path =  "vid.mp4"

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
while True:
    ret, frame =  cap.read()
    if not ret :
        break

    fps_text =  f"FPS : {int(fps)}"
    cv2.putText(frame, fps_text, (10,40),
                cv2.FONT_HERSHEY_SIMPLEX,1,
                 (200,0,0,),2,cv2.LINE_AA)

    result =  model.track(frame,persist=True) #*on the current frame
    for c  in result[0].boxes:
        index = int(c)
        classid =  

    new_frame =  result[0].plot()

    cv2.imshow('recording ... ',new_frame)
    out.write(new_frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("Playback stopped by user.")
        break
cv2.destroyAllWindows()