from ultralytics import YOLO
import cv2 as cv

clas_name={
    0:"plaka"
}
model= YOLO("best.pt")
video_path="örnekvideo.mp4"
cap=cv.VideoCapture(video_path)

screen_width= 448
screen_height=800
while cap.isOpened():
    ret,frame = cap.read()
    if not ret:
        break
    frame=cv.resize(frame,(screen_width,screen_height))
    results=model(frame)[0]
    for result in results.boxes.data.tolist():
     x1  , y1 , x2 ,y2 ,score , ID=results
     x1 , y1 , x2 ,y2=map(int,[x1,y1,x2,y2])
    
     if score>=0.1:
        color=(0,255,0)
        thickness=2
        cv.rectangle(frame,(x1,y1),(x2,y2),color,thickness)
        if ID in clas_name:
            cv.putText(frame,clas_name[ID],(x1,y1+50),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255))

    cv.imshow("Video",frame)

cap.release()
cv.destroyAllWindows()        
