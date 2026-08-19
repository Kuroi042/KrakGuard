import cv2
import numpy as np
from ultralytics import YOLO
RADAR_WIDTH = 300
RADAR_HEIGHT = 300
WIDTH = 1280
HEIGHT = 720
class Radar: 
    def __init__(self): 
        self.position={}
        self.fps= 30
        self.previous_pos={}
# get the center of each 
    def radarr(self,result):
        radar = np.zeros((RADAR_HEIGHT, RADAR_WIDTH, 3)
                         , dtype=np.uint8)        #canvas for dots   
        for i in result[0].boxes:
            x1,y1,x2,y2  = map(int, i.xyxy[0])
            centerx = int((x1+x2)/2)
            centery =  int(y2) #bottom
            trackid =  int(i.id[0])
            self.previous_pos[trackid]= self.position.get(trackid)#get postion old values
            self.position[trackid]= (centerx, centery)#update

            previous =  self.previous_pos[trackid]
            current = self.position[trackid]
            if previous is not None:    
                distance =  np.linalg.norm(np.array(current) - np.array(previous))
                print(trackid,distance)
            # distance = self.current-self.previous
            # print(trackid ,distance)
            # centerx in width 
            # Radar_x in RADAR_WIDTH
            #la regle de 3
            radar_x =  int((centerx*RADAR_WIDTH )/WIDTH) 
            radar_y =  int((centery*RADAR_HEIGHT)/HEIGHT)

            cv2.circle(radar, (radar_x, radar_y),5,(225,0,0),-1 )

        return radar