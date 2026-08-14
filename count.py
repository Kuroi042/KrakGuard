from ultralytics import YOLO
import cv2
import numpy as np
model  =  YOLO("yolo11s.pt")
cap =  cv2.VideoCapture('traf.mp4')
fps  =  cap.get(cv2.CAP_PROP_FPS)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
trajectorie = {}
previous_side = {}
inn, out = 0,0
cv2.namedWindow('img')
while(True):
    print(width, height)
# 22 in | out 23-24
    ret, frame = cap.read() 
    fps_text =  f"FPS: {int(fps)}"
    # cv2.putText(`frame, fps_text,(10,40), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
    result =  model.track(source=frame, persist=True,conf=0.1)
    line_y = 280
    line_top = 260
    line_bottom = 280
    # cv2.line(frame, (0,line_y),(int(width),line_y), (255, 0, 0),2,2)
    cv2.rectangle(frame, (0,260),(int(width),300),(225,225,0),2,cv2.LINE_AA)
    for i in (result[0].boxes):
        x1,y1,x2,y2 =  np.array(i.xyxy[0])
        centerx =  int((x1+x2)/2)
        centery =  int((y1+y2)/2)

        point_x = int((x1 + x2) / 2)
        point_y = int(y2)

        track_id =  int(i.id[0])
        if i.id is not None:
            track_id = int(i.id[0])
        else:
            track_id = None
        if track_id not in trajectorie:
            trajectorie[track_id]=[]
        trajectorie[track_id].append((centerx,centery))
        for id , point in trajectorie.items():
            #* point = [(centerx, centery)]
            for j in range(1, len(point)):

                cv2.line(frame, (point[j-1]), (point[j]) ,(0,225,0),1,cv2.LINE_AA)

        # current_side = "above" if centery < line_top else "below" #*centry >liney
        if point_y < line_top:
            current_side = "above"
        elif point_y >line_bottom:
            current_side = "below"
        else:
            current_side = "zone"
        
        if track_id in previous_side:

            old_side = previous_side[track_id]

            # ABOVE → ZONE → BELOW
            if old_side == "zone" and current_side == "below":
                if previous_side.get(f"{track_id}_start") == "above":
                    out += 1
                    print(f"ID {track_id} → OUT")

            # BELOW → ZONE → ABOVE
            elif old_side == "zone" and current_side == "above":
                if previous_side.get(f"{track_id}_start") == "below":
                    inn += 1
                    print(f"ID {track_id} → IN")

            # Remember where the object entered the zone
            if old_side != "zone" and current_side == "zone":
                previous_side[f"{track_id}_start"] = old_side

        previous_side[track_id] = current_side
        
        text = f"Out:{out}--------------in{inn}"
        cv2.putText(frame,text, (50,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)


    vid  =  result[0].plot()
    cv2.imshow('img',vid)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()