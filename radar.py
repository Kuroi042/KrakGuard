import cv2
import numpy as np
from ultralytics import YOLO
RADAR_WIDTH = 300
RADAR_HEIGHT = 300
WIDTH = 1280
HEIGHT = 720
LIMIT = 30
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
        violators = [] 
        # radar = np.zeros((RADAR_HEIGHT, RADAR_WIDTH, 3)
                        #  , dtype=np.uint8)        #canvas for dots   
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
                speedkm =  (distance_meter/time)*3.6 #km/h 


                # print(self.get_speed)
                #* exponential moving average (EMA)
                if trackid in self.get_speed:
                    smooth_speed = self.alpha*speedkm+(1-self.alpha)*self.get_speed[trackid]
                else:
                    smooth_speed= speedkm
                self.get_speed[trackid] =  smooth_speed
                if self.get_speed[trackid]>30:
                    color =(0,0,255)
                else:
                    color=(0,255,0)
                cv2.putText(frame, f"{smooth_speed:.0f} km/h", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)
                if smooth_speed >LIMIT:
                    violators.append((trackid,int(smooth_speed)))
                    # print(f"id : {violators}")
            self.radar_fix(frame , violators)
  

  
    def radar_fix(self,frame , violators):
        panel_x , panel_y = WIDTH-250,20
        panel_w, line_h =  230,25
        panel_h = 30+line_h*max(len(violators),1)

        overlay = frame.copy()
        cv2.rectangle(overlay, (panel_x, panel_y), (panel_x+panel_w, panel_y+panel_h), (0, 0, 255), -1) 
        cv2.addWeighted(overlay, 0.5, frame, 0.5,0,frame)
        cv2.putText(frame, "SPEEDING !!!",(panel_x+10, panel_y+20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,225),2,cv2.LINE_AA)
        if not violators:
                cv2.putText(frame, "None", (panel_x + 10, panel_y + 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        else:
                for i , (trackid,speed) in enumerate( violators):

                    y = panel_y + 45 + i * line_h
                    text = f"ID {trackid} | speed: {speed}"
                    cv2.putText(frame, text,(panel_x+10,y),cv2.FONT_HERSHEY_SIMPLEX,0.5
                                ,(225,0,0),1,cv2.LINE_AA,)

 
