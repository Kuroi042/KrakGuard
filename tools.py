import cv2
import numpy as np
#  and justice for all
drawing = False
ix, iy, = -1, -1 
fx, fy= -1, -1 
backup_img = img.copy()
draw = 0

def select_region(event, x, y, flags, param):
  global ix, iy, fx, fy, drawing, img, backup_img, draw
  if event == cv2.EVENT_LBUTTONDOWN and draw == 0: #red == 0
    drawing = True
    ix, iy = x, y
  if event == cv2.EVENT_LBUTTONDOWN and draw == 1: #blue = -1
    draw = 1
    drawing = True
    ix, iy = x, y
  elif event == cv2.EVENT_MOUSEMOVE:
    if drawing:
      img = backup_img.copy() #reset the image avoid multi drawinf
      if draw == 0:
        cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 225), 2)
      elif draw == 1:
        cv2.rectangle(img, (ix, iy), (x, y), (225, 0, 0), 2)

  elif event == cv2.EVENT_LBUTTONUP and draw == 0:#red 0
      drawing = False
      fx, fy = x, y
      cv2.rectangle(backup_img, (ix, iy), (fx, fy), ( 0, 0, 225), 2)
      img = backup_img.copy()
      draw= 1

  elif event == cv2.EVENT_LBUTTONUP and draw == 1:#blue 1
      jx, jy = x, y
      drawing = False
      cv2.rectangle(backup_img, (ix, iy), (jx, jy ), ( 225, 0, 0), 2)
      img = backup_img.copy()
      draw=0
mouse_data={
       "frame":None
    }
# cv2.setMouseCallback("Image Window", select_region, mouse_data)

while True:
  cv2.imshow("Image Window", img)
  if cv2.waitKey(1) & 0xFF == ord('q') : # Press 'ESC' to exit
    break
cv2.destroyAllWindows()
