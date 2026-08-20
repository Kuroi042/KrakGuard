import cv2
import numpy as np
from ultralytics import YOLO
from radar import Radar 
WIDTH = 1280
HEIGHT = 720

BAR = [500, 600]
GRACE_FRAMES = 10

CLASS_NAMES = {
    2: "car",
    3: "Motorcycle",
    7: "Truck",
    5: "bus"
}

GREEN = (0, 225, 0)
RED = (0, 0, 255)

radar =  Radar()
class Counter:

    def __init__(self):
        self.side_of_line = {}
        self.entered_from = {}
        self.crossed = {}
        self.last_seen = {}

        self.inn = 0
        self.out = 0

    def count(self, result, frame):

        cv2.rectangle(frame,(0, BAR[0]),(WIDTH, BAR[1]),(225, 0, 0),5)
        seen_now = set()
        for box in result[0].boxes:
            if box.id is None:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            centerx = int((x1 + x2) / 2)
            centery = int(y2)

            trackid = int(box.id[0])
            class_id = int(box.cls[0])

            seen_now.add(trackid)
            text = f"obj: {trackid}, {CLASS_NAMES[class_id]}"
            cv2.putText(frame,text,(centerx, centery),cv2.FONT_HERSHEY_SIMPLEX,0.5,GREEN,1,cv2.LINE_AA)
            cv2.rectangle(frame,(x1, y1),(x2, y2),(0, 225, 0),2,cv2.LINE_AA)
            if centery < BAR[0]:
                current = "above"

            elif centery > BAR[1]:
                current = "below"

            else:
                current = "zone"

            previous = self.side_of_line.get(trackid)

            self.side_of_line[trackid] = current

            if previous == "above" and current == "zone":
                self.entered_from[trackid] = "above"

            elif previous == "below" and current == "zone":
                self.entered_from[trackid] = "below"


            if (previous == "zone"and current == "below"and self.entered_from.get(trackid) == "above"):
                if not self.crossed.get(trackid, False):
                    self.out += 1
                    self.crossed[trackid] = "out"
            if (previous == "zone"and current == "above"and self.entered_from.get(trackid) == "below"):
                if not self.crossed.get(trackid, False):
                    self.inn += 1
                    self.crossed[trackid] = "in"
            if self.crossed.get(trackid) == "in":
                color = GREEN

            elif self.crossed.get(trackid) == "out":
                color = RED

            else:
                color = (225, 225, 225)
            cv2.circle(frame,(centerx, centery),10,color,-1)
            self.last_seen[trackid] = [centerx,centery,0]
        for trackid in list(self.last_seen.keys()):
            if trackid not in seen_now:
                self.last_seen[trackid][2] += 1

                if self.last_seen[trackid][2] > GRACE_FRAMES:
                    del self.last_seen[trackid]

        text_out = f"IN: {self.inn}   OUT: {self.out}"

        cv2.putText(
            frame,
            text_out,
            (50, 50),
            cv2.FONT_HERSHEY_COMPLEX_SMALL,
            1,
            (225, 0, 0),
            1,
            cv2.LINE_AA
        )

        return frame