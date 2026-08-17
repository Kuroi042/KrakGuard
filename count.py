from ultralytics import YOLO
import cv2
import numpy as np
model  =YOLO("yolo11n.pt")
cap = cv2.VideoCapture("source/traf.mp4")
WIDTH =  1280
HEIGHT =720   
GRACE_FRAMES=10      #above
bar=[500,600]       #----- 500
                    #----- 600
                    #below
side_of_line={} #id+side
is_in={}
entered_from={}
crossed = {}
last_seen = {} #keep track of ID 
inn = 0
out = 0
previous = None
col=[(0,225,0),(0,0,255)]
while True:
    ret, frame =  cap.read()
    if  not ret:
        break
    frame = cv2.resize(frame, (WIDTH,HEIGHT))
    result = model.track(frame, persist=True,classes=[2, 3, 7, 5], conf=0.25,imgsz=640)
    cv2.rectangle(frame, (0,bar[0]),(WIDTH,bar[1]),(225,0,0),1,cv2.LINE_4)
    seen_now =  set()

    for box in result[0].boxes:

        if box.id is None:
            continue
        x1,y1,x2,y2 = map(int,box.xyxy[0])
        centerx = int((x1+x2)/2)
        centery =  int(y2)
        trackid =  int(box.id[0])

        seen_now.add(trackid)
        cv2.rectangle(frame, (x1,y1),(x2,y2),(0,0,225),1, cv2.LDR_SIZE)
        if centery < bar[0]:
            current ="above"
        elif centery > bar[1]:
            current ="below"
        else:
            current = "zone"
        previous =  side_of_line.get(trackid) #get the value for specific trackid
 
        side_of_line[trackid]=current #this one first then previous
        if previous=="above" and current =="zone":
             entered_from[trackid]="above"

        elif previous=="below" and current == "zone":
             entered_from[trackid]="below"

        if previous == "zone" and current =="below" and entered_from.get(trackid)=="above":
            if not crossed.get(trackid, False):
                out+=1
                crossed[trackid]="out"
        if previous ==  "zone" and current =="above" and entered_from.get(trackid)=="below":
            if not crossed.get(trackid, False):
                inn+=1
                crossed[trackid]="in"
        if crossed.get(trackid)=="in":
            color = col[0]        
        elif crossed.get(trackid)=="out":
            color = col[1]
        else:
            color = (225,225,225)
        cv2.circle(frame, (centerx, centery), 10, color, -1)

        text_out = f"in: {inn}----out: {out}"
       
        cv2.putText(frame, text_out, (50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(225,0,0),1,cv2.LINE_AA)
        last_seen[trackid]=[centerx, centery,0] #zero for zero frame been missing 
    for trackid in list(last_seen.keys()):
        if trackid not in seen_now:
            last_seen[trackid][2] += 1

            if last_seen[trackid][2]>GRACE_FRAMES:
                del last_seen[trackid]
    cv2.imshow("img", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()