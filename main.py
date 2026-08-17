from ultralytics import YOLO
import cv2
import numpy as np
from counting import count
model  =YOLO("yolo11n.pt")
WIDTH =  1280
HEIGHT =720 
inn = 0
out = 0
def main():

    model = YOLO("yolo11n.pt")
    cap = cv2.VideoCapture("source/traffic.mp4")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (WIDTH, HEIGHT))

        result = model.track(
            frame,
            persist=True,
            classes=[2, 3, 7, 5],
            conf=0.25,
            imgsz=640
        )
        frame, inn, out = count(result, frame, 0, 0)  
        cv2.imshow("img", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
if __name__ =="__main__":
    main()