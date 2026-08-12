import cv2
import time
from ultralytics import YOLO
path =  "/home/kenshin/Desktop/DataProject/dvr/vid.mp4"
model  =  YOLO("yolo11n.pt")




newtime = 0
prevtime =0
path =  "vid.mp4"

cap = cv2.VideoCapture(path)
fps = cap.get(cv2.CAP_PROP_FPS)
width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fourcc =  cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter('out.mp4',
                fourcc,
                fps,(width,height) )

while True:
    ret, frame =  cap.read()
    if not ret :
        break

    newtime  =  time.time()
    dif_time  =  newtime- prevtime
    fps  =  1/dif_time if dif_time >0 else 0
    prevtime =  newtime
    fps_text =  f"FPS : {int(fps)}"
    cv2.putText(frame, fps_text, (10,40),
                cv2.FONT_HERSHEY_SIMPLEX,1,
                 (200,0,0,),2,cv2.LINE_AA)
    print(f"fps:{fps}| width:{width}| Height:{height}| frame_count:{frame_count}")
    result =  model(frame, classes=0)
    new_frame =  result[0].plot()

    cv2.imshow('recording ... ',new_frame)
    out.write(new_frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("Playback stopped by user.")
        break
cv2.destroyAllWindows()