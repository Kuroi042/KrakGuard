from ultralytics import YOLO
import numpy as np
import cv2
import os

model_path='yolo11s.pt'

class Detector:
    def __init__(self, model):
        self.model = YOLO(model_path)
    def detect(self,frame):
        return self.model(frame)
class Tracker:
    def __init__(self,model):
        self.model =model
    def track(self, frame):
        return self.model.track(
            frame, persist=True,
            conf = 0.25
        )
    