from ultralytics import YOLO
import cv2
import numpy as np
model  =  YOLO("yolo11n.pt")
cap =  cv2.VideoCapture('traffic.mp4')
fps  =  cap.get(cv2.CAP_PROP_FPS)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
trajectorie = {}
previous_side = {}
inn, out = 0,0
while(True):
    print(width, height)

    ret, frame = cap.read() 
    fps_text =  f"FPS: {int(fps)}"
    # cv2.putText(`frame, fps_text,(10,40), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
    result =  model.track(source=frame, persist=True,conf=0.4)
    for i in (result[0].boxes):
        x1,y1,x2,y2 =  np.array(i.xyxy[0])
        centerx =  int((x1+x2)/2)
        centery =  int((y1+y2)/2)
        track_id =  int(i.id[0])
        line_y = 280
        cv2.line(frame, (0,line_y),(int(width),line_y), (255, 0, 0),2,2)
        if track_id not in trajectorie:
            trajectorie[track_id]=[]
        trajectorie[track_id].append((centerx,centery))
        for id , point in trajectorie.items():
            #* point = [(centerx, centery)]
            for j in range(1, len(point)):

                cv2.line(frame, (point[j-1]), (point[j]) ,(0,225,0),1,cv2.LINE_AA)

        current_side = "above" if centery < line_y else "below" #*centry >liney
        if track_id in previous_side:
            old_side = previous_side[track_id]

            if old_side != current_side:

                if current_side == 'above' and old_side=="below":
                    out+=1
                    print(f"ID {track_id} → OUT")
                elif current_side == 'below' and old_side=="above":
                    inn+=1
                    print(f"ID {track_id} → IN")
        previous_side[track_id] = current_side
        
        text = f"In:{inn}--------------Out{out}"
        cv2.putText(frame,text, (50,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)


    vid  =  result[0].plot()
    cv2.imshow('img',vid)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()