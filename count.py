from ultralytics import YOLO
import cv2
import numpy as np
model  =  YOLO("yolo11s.pt")
cap =  cv2.VideoCapture('source/traffic.mp4')
fps  =  cap.get(cv2.CAP_PROP_FPS)
TARGET_WIDTH = 1280
TARGET_HEIGHT = 720
trajectorie = {}
previous_side = {}
inn, out = 0,0
line_y = 280
line_top = 600
line_bottom = 640
flag = False
while(True):
    ret, frame = cap.read() 
    frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))

    fps_text =  f"FPS: {int(fps)}"

    result =  model.track(source=frame,persist=True,conf=0.25)

    cv2.rectangle(frame, (0,line_top),(int(TARGET_WIDTH),line_bottom),(225,225,0),-1,cv2.LINE_AA)
    boxes =  result[0].boxes
    if boxes is not None and len(boxes)>0:
        for i in boxes:
            x1,y1,x2,y2 =  np.array(i.xyxy[0])#bbox
            centerx =  int((x1+x2)/2)
            centery =  int((y1+y2)/2)

            point_x = int((x1 + x2)/2)  
            point_y = int(y2) 

            if i.id is not None:
                track_id = int(i.id[0]) 
            else:
                continue

            if track_id not in trajectorie:
                trajectorie[track_id]=[] #create an empty list for id
            trajectorie[track_id].append((centerx,centery))#fill the list
            point = trajectorie[track_id]
            for j in range(1, len(point)):
                    cv2.line(frame, (point[j-1]), (point[j]) ,(0,225,0),1,cv2.LINE_AA)

            if point_y < line_top: #
                current_side = "above"
            elif point_y >line_bottom:
                current_side = "below"
            else:
                current_side = "zone"
            
            if track_id in previous_side:
                old_side = previous_side[track_id]
            
                # ABOVE → ZONE → BELOW
                if old_side == "zone" and current_side == "below":
                    if previous_side.get(f"{track_id}_start") == "above":#history checl
                        flag = False
                        out += 1
                        print(f"ID {track_id} → OUT")

                # BELOW → ZONE → ABOVE
                elif old_side == "zone" and current_side == "above":
                    if previous_side.get(f"{track_id}_start") == "below":
                        flag = True 
                        inn += 1
                        print(f"ID {track_id} → IN")
            
                # Remember where the object entered the zone
                if old_side != "zone" and current_side == "zone":
                    flag  =True
                    previous_side[f"{track_id}_start"] = old_side
            ##add circle 
                green,red = [(0,0,255),(0,255,0)]
                for id in previous_side:
                    if previous_side[id] == "below":
                        color = red
                        cv2.circle(frame, (centerx,centery),10,color,-1, cv2.LINE_AA)

                    elif previous_side[id]=="above":
                        color=green
                        cv2.circle(frame, (centerx,centery),10,color,-1, cv2.LINE_AA)

                    else:
                        color = green
                        # color =red if flag==False else green
                        cv2.circle(frame, (centerx,centery),10,color,-1, cv2.LINE_AA)
            previous_side[track_id] = current_side

        text = f"Out:{out}----in{inn}"
        cv2.putText(frame,text, (50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)


    # cv2.imshow("Vehicle Counter 
    # vid  =  result[0].plot()

    cv2.imshow('img',frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()