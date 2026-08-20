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
        self.distance = 0
        self.speedkm=0
        self.get_speed={}
        self.alpha = 0.3  #smoothing factor 
# get the center of each 
    def radarr(self,result,frame):
        radar = np.zeros((RADAR_HEIGHT, RADAR_WIDTH, 3)
                         , dtype=np.uint8)        #canvas for dots   
        for i in result[0].boxes:
            if i.id is None:
                continue
            x1,y1,x2,y2  = map(int, i.xyxy[0])
            centerx = int((x1+x2)/2)
            centery =  int(y2) #bottom
            trackid =  int(i.id[0])
            self.previous_pos[trackid]= self.position.get(trackid)#get postion old values
            self.position[trackid]= (centerx, centery)#update

            previous =  self.previous_pos[trackid]
            current = self.position[trackid]
            if previous is not None:    
                distance_px =  np.linalg.norm(np.array(current) - np.array(previous))
                # print(trackid,self.distance)#pixel/frame*0
                meters_per_pixel = 3.5 / 140
                distance_meter =  distance_px*meters_per_pixel
                time  = 1/self.fps #seconds/frame*0
                speedkm =  (distance_meter/time)*3.6 #pixel/sec


                # print(self.get_speed)
                #* exponential moving average (EMA)
                if trackid in self.get_speed:
                    smooth_speed = self.alpha*speedkm+(1-self.alpha)*self.get_speed[trackid]
                else:
                    smooth_speed= speedkm
                self.get_speed[trackid] =  smooth_speed


            
                cv2.putText(frame, f"{smooth_speed:.0f} km/h", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)


            # print( self.speedkm)
            #la regle de 3
            radar_x =  int((centerx*RADAR_WIDTH )/WIDTH) 
            radar_y =  int((centery*RADAR_HEIGHT)/HEIGHT)

            cv2.circle(radar, (radar_x, radar_y),5,(225,0,0),-1 )

        return radar