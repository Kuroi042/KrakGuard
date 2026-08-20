import cv2
import numpy as np
from ultralytics import YOLO
import json
RADAR_WIDTH = 300
RADAR_HEIGHT = 300
WIDTH = 1280
HEIGHT = 720
LIMIT = 30
VIOLATION_TTL = 10 #how many frames violatator stay on screen 
class Radar:
    def __init__(self, fps=30, detect_every=1):
        self.position = {}
        self.fps = fps
        self.previous_pos = {}
        self.detect_every = detect_every
        self.get_speed = {}
        self.alpha = 0.3
        self.violators = {}        # active on-screen panel, entries expire via TTL
        self.violation_history = {}  # permanent log, never deleted

    def radarr(self, result, frame):
        for i in result[0].boxes:
            if i.id is None:
                continue
            x1, y1, x2, y2 = map(int, i.xyxy[0])
            centerx = int((x1 + x2) / 2)
            centery = int(y2)
            trackid = int(i.id[0])

            previous = self.position.get(trackid)
            self.position[trackid] = (centerx, centery)
            current = self.position[trackid]

            if previous is None:
                continue

            distance_px = np.linalg.norm(np.array(current) - np.array(previous))#px
            meters_per_pixel = 3.5 / 140 #ratio 3.5=140px
            distance_meter = distance_px * meters_per_pixel#how many m per one pixel
            time = self.detect_every / self.fps#how much time passed between two position
            speedkm = (distance_meter / time) * 3.6 #*km/h

            if trackid in self.get_speed:
                #*Exponential moving average
                smooth_speed = self.alpha * speedkm + (1 - self.alpha) * self.get_speed[trackid]
            else:
                smooth_speed = speedkm
            self.get_speed[trackid] = smooth_speed

            if smooth_speed > LIMIT:
                if trackid in self.violators:
                    old_max = self.violators[trackid][0] 
                else: 
                    old_max=0# default
                # self.violators[trackid][0]==>max() | self.violators[trackid][1] ==> TLL
                self.violators[trackid] = [max(smooth_speed, old_max), VIOLATION_TTL]

                # keep the highest speed ever recorded for this id
                prev_history_max = self.violation_history.get(trackid, 0)
                self.violation_history[trackid] = max(smooth_speed, prev_history_max)

            color = (0, 0, 255) if trackid in self.violators else (0, 255, 0)
            cv2.putText(frame, f"{smooth_speed:.0f} km/h", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

        for trackid in list(self.violators.keys()):
            self.violators[trackid][1] -= 1
            if self.violators[trackid][1] <= 0:
                del self.violators[trackid]

        self.radar_fix(frame)

    def radar_fix(self, frame):
        panel_x, panel_y = WIDTH - 250, 20
        panel_w, line_h = 230, 25
        panel_h = 30 + line_h * max(len(self.violators), 1)

        overlay = frame.copy()
        cv2.rectangle(overlay, (panel_x, panel_y), (panel_x + panel_w, panel_y + panel_h), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        cv2.putText(frame, "SPEEDING !!!", (panel_x + 10, panel_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 225), 2, cv2.LINE_AA)

        for i, (trackid, (speed, ttl)) in enumerate(self.violators.items(), start=1):
            text = f"ID {trackid} | speed: {speed:.0f} km/h"
            cv2.putText(frame, text, (panel_x + 10, panel_y + 25 + i * line_h),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 0, 0), 1, cv2.LINE_AA)

        if self.violation_history:
            with open("data.json", "w") as f:
                json.dump(self.violation_history, f, indent=4)
