import cv2
import time
path =  "raw.mp4"
newtime = 0
prevtime =0

cap = cv2.VideoCapture(path)
while True:
    ret, frame =  cap.read()
    if not ret :
        break
    newtime  =  time.time()
    dif_time  =  newtime- prevtime
    fps  =  1/dif_time if dif_time >0 else 0
    prevtime =  newtime
    fps_text =  f"FPS : {int(fps)}"
    cv2.putText(frame, fps_text, (10,40),
                cv2.FONT_HERSHEY_SIMPLEX,1,
                (200,0,0,),2,cv2.LINE_AA)

    cv2.imshow('img',frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("Playback stopped by user.")
        break
cv2.destroyAllWindows()