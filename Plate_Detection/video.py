import cv2
from ultralytics import YOLO
import pytesseract

# (Sadece Windows'ta gerekliyse aç)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Plaka tespiti için eğitilmiş YOLOv8 modeli
model = YOLO("best.pt")

# Video kaynağı
cap = cv2.VideoCapture("örnekvideo.mp4")  # veya 0 -> webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv8 ile tespit yap
    results = model.predict(frame, conf=0.3, verbose=False)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Koordinatları al
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Plaka bölgesini kırp
            plate_roi = frame[y1:y2, x1:x2]

            # OCR ile metni oku (ön işleme iyileştirme yapılabilir)
            gray = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray, config='--psm 7')  # psm 7: tek satır yazı

            # Etrafına kutu çiz ve OCR sonucu yaz
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, text.strip(), (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 0), 2)

    cv2.imshow("Plaka Tespiti ve OCR", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
