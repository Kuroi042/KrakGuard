import cv2
import numpy as np
from ultralytics import YOLO
RADAR_WIDTH = 300
RADAR_HEIGHT = 300
WIDTH = 1280
HEIGHT = 720
class Radar: 
    def __init__(self): 
        self.fps = 30   
        self.positions={}
        self.prevPosition={}
        self.distance=None
        self.meters_per_pixel = 0.05
        self.time = float(1/self.fps)
    def radarr(self,result):
        radar = np.zeros((RADAR_HEIGHT, RADAR_WIDTH, 3)
                         , dtype=np.uint8)             

        for box in result[0].boxes:
            if box.id is None:
                continue
            x1,y1,x2,y2 =  map(int,box.xyxy[0])
            centerx=int((x1+x2)/2) 
            centery = int(y2)  
            trackid =  int(box.id[0])
            radar_x =  int(centerx *RADAR_WIDTH / WIDTH) #get the middle
            radar_y = int(centery * RADAR_HEIGHT / HEIGHT )#get the middle
            cv2.circle(radar,(radar_x, radar_y),5,(0,0,225),-1)
            previous = self.prevPosition[trackid]=self.positions.get(trackid)
            current  = self.positions[trackid] = (centerx, centery) 
            if previous is not None:

                self.distance = np.linalg.norm(
                    np.array(current) - np.array(previous)
                )

                meters_per_second = (
                    self.distance
                    * self.fps
                    * self.meters_per_pixel
                )

                speed_kmh = meters_per_second * 3.6

                self.speed_limit = 50

                if speed_kmh > self.speed_limit:
                    print(f"ID {trackid} -> SPEEDING: {speed_kmh:.1f} km/h")
            # print(trackid, self.distance)

        return radar