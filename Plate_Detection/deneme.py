from ultralytics import YOLO
import cv2 as cv
class_name={
    0:"plaka"
}
path="images/örnek3.png"
image=cv.imread(path)

model=YOLO("best.pt")
results=model(image)[0]
for result in results.boxes.data.tolist():
    x1 , y1 , x2 , y2 , score,ID=result
    x1 , y1 , x2 , y2=map(int,[x1,y1,x2,y2])

    if score >= 0.1:
        color=(0,255,0)
        thickness=2
        cv.rectangle(image,(x1,y1),(x2,y2),color,thickness)
        if ID in class_name:
            cv.putText(image,class_name[ID],(x1,y1+25),cv.FONT_HERSHEY_COMPLEX,1,(0,255,255))

cv.imshow("Görüntü",image)
cv.waitKey(0)
cv.destroyAllWindows()