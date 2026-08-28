from ultralytics import YOLO
import cv2
from counting import Counter
from radar import Radar
import time
import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.withdraw()

# Show alert popup


WIDTH = 1280
HEIGHT = 720

mouse_pos = (0, 0)

drawing = False
ix, iy = -1, -1
draw = 0
region_mode = False
regions = []

def draw_regions(frame):

    for x1, y1, x2, y2, color_id in regions:

        if color_id == 0:
            color = (0, 0, 225)
        else:
            color = (225, 0, 0)

        cv2.rectangle(frame,(x1, y1),(x2, y2),color,2)

def select_region(event, x, y, flags, param):

    global mouse_pos
    global drawing, ix, iy
    global draw, region_mode, regions
    radar = param["radar"]
    counter = param["counter"]
    frame = param["frame"]
    img =  frame.copy()
    shapes_history = []
    trigger_alert = True
    if frame is None:
        return
    mouse_pos = (x, y)

    if event == cv2.EVENT_MOUSEMOVE:

        if drawing:
            param["current_x"] = x
            param["current_y"] = y
        return
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if 5 < x < 100 and 120 < y < 155:
            if frame is not None:
                capture = frame.copy()
                cv2.putText(capture,"Capture_Saved!!",(640, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 0),1,cv2.LINE_AA)
                cv2.imwrite("Capture_saved.png",capture)
            return
        elif 5 < x < 100 and 165 < y < 200:         #*radar btn
            radar.btn = not radar.btn
            return
        elif 5 < x < 100 and 210 < y < 245:         #*counter btn
            messagebox.showwarning("Alert", "ALERT: Action Detected!")
            root.destroy()
        #rectangle coordinate
        elif 5 < x < 100 and 255 < y < 290:          #*region_btn
            region_mode = not region_mode
            print("Region mode:", region_mode)
            return
        if region_mode:
            drawing = True
            ix = x
            iy = y
            param["current_x"] = x
            param["current_y"] = y

    elif event == cv2.EVENT_LBUTTONUP:

        if drawing:
            fx = x
            fy = y

            regions.append(
                (ix,  iy,fx,fy,draw))

            print(
                f"Region: {(ix, iy)} -> {(fx, fy)}")
            draw = 1 - draw
            drawing = False
            trigger_alert = False


def draw_current_region(frame, param): #while the scroolwheel event

    if not param["drawing"]:
        return

    x1 = param["ix"]#first_click
    y1 = param["iy"]

    x2 = param["current_x"]#movewheel
    y2 = param["current_y"]

    if param["draw"] == 0:
        color = (0, 0, 225)
    else:
        color = (225, 0, 0)
    cv2.rectangle(frame,(x1, y1),(x2, y2),color,2)


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

    cap = cv2.VideoCapture(
        "source/traf.mp4"
    )

    if not cap.isOpened():
        raise IOError("Could not open video")
    counter = Counter()
    radar = Radar()
    mouse_data = {"radar": radar, #extra info for select_region
                  "counter": counter,
                  "frame": None,
                  "drawing": False,"ix": -1,
                  "iy": -1,
                  "current_x": -1,
                  "current_y": -1,
                  "draw": 0}

    cv2.namedWindow("img")

    cv2.setMouseCallback("img",select_region,mouse_data)# additive data to the main function wile calling back 
    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(
            frame,
            (WIDTH, HEIGHT)
        )

        mouse_data["frame"] = frame.copy()

        result = model.track(
            frame,persist=True,tracker="bytetrack.yaml", classes=[2, 3, 7, 5],conf=0.25,imgsz=640)

        counter.count(result,frame)

        radar.radarr(result,frame)

        draw_regions(frame)
        draw_current_region(frame,mouse_data)

        Button(frame,"Capture",5,120,100,155,mouse_pos)
        Button(frame,"Radar",5,165,100,200,mouse_pos)
        Button(frame,"Counting",5,210,100,245,mouse_pos)
        Button(frame,"SetRegion\nCount",5,255,100,290,mouse_pos)
        Button(frame,"UndoSetRegion",1,300,130,335,mouse_pos)
        
        current_time = time.localtime()
        formatted_time = time.strftime("%H:%M:%S",current_time)

        cv2.putText(frame,formatted_time,(WIDTH - 200, 30),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 0),1,cv2.LINE_AA)
        cv2.circle(frame,mouse_pos,4,(0, 0, 255),-1)
        cv2.imshow("img",frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()