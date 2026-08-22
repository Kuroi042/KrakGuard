from ultralytics import YOLO
import cv2

from counting import Counter
from radar import Radar

WIDTH = 1280
HEIGHT = 720
x1, y1, x2, y2 = 5, 120, 100, 155
mouse_pos = (0, 0)

def MouseControl(event, x, y, flags, param):
    global mouse_pos
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_pos = (x, y)

def Button(frame, text, x1, y1, x2, y2, mouse_pos):
    hover = (x1 <= mouse_pos[0] <= x2 and y1 <= mouse_pos[1] <= y2)

    if hover:
        bg_color = (0, 180, 255)
    else:
        bg_color = (0, 0, 225)

    overlay = frame.copy()

    cv2.rectangle(overlay,(x1, y1),(x2, y2),bg_color,-1)
    cv2.addWeighted(overlay,0.75,frame,0.25,0,frame)
    cv2.rectangle(frame,(x1, y1),(x2, y2),(255, 255, 255),1,cv2.LINE_AA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.45
    thickness = 1

    text_size = cv2.getTextSize(text,font,font_scale,thickness)[0]
    text_x = x1 + ((x2 - x1) - text_size[0]) // 2
    text_y = y1 + ((y2 - y1) + text_size[1]) // 2

    cv2.putText(frame,text,(text_x, text_y),font,font_scale,(255, 255, 255),thickness,cv2.LINE_AA)


def main():

    model = YOLO("yolo11n.pt")
    cap = cv2.VideoCapture("source/traf.mp4")
    if not cap.isOpened():
        raise IOError("Could not open video")
    counter = Counter()
    radar = Radar()
    cv2.namedWindow("img")
    cv2.setMouseCallback("img", MouseControl)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame,(WIDTH, HEIGHT))
        result = model.track(frame,persist=True,tracker="bytetrack.yaml",classes=[2, 3, 7, 5],conf=0.25,imgsz=640)
        Button(frame,"Capture",5, 120,100, 155,mouse_pos)
        Button(frame,"Radar",5, 165,100, 200,mouse_pos)
        Button(frame,"Counting",5, 210,100, 245,mouse_pos)
        Button(frame,"OCR",5, 255,100, 290,mouse_pos)
        frame = counter.count(result,frame)
        radar_img = radar.radarr(result,frame)
        cv2.circle(frame,mouse_pos,4,(0, 0, 255),-1)


        cv2.imshow("img",frame)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()