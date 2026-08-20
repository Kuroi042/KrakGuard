from ultralytics import YOLO
import cv2

from counting import Counter
from radar import Radar

WIDTH = 1280
HEIGHT = 720

def main():
    model = YOLO("yolo11n.pt")
    cap = cv2.VideoCapture("source/traffic.mp4")
    counter = Counter()
    radar =  Radar()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        result = model.track(frame,persist=True,classes=[2, 3, 7, 5]
                             ,conf=0.25,
                             imgsz=640)
        frame = counter.count(result, frame)
        radar_img =  radar.radarr(result,frame)
        cv2.imshow("img", frame)
        # cv2.imshow("radar", radar_img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()