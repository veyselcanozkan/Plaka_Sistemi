import cv2
from ultralytics import YOLO
import pytesseract

# Modeli yükle (kendi eğittiğin plaka modeli)
model = YOLO("best.pt")  # veya kendi path'in

# Video kaynağı
video_path = "örnekvideo.mp4"
cap = cv2.VideoCapture(video_path)

# (Opsiyonel) video çıktısını kaydetmek istersen:

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv8 ile plaka tespiti
    results = model(frame)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            # Plaka alanını kırp
            plate_crop = frame[y1:y2, x1:x2]

            # OCR ile plaka okuma
            text = pytesseract.image_to_string(plate_crop, config='--psm 7')
            text = text.strip()

            # Görüntü üzerine çizim
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 255), 2)

      # videoya yaz
    cv2.imshow("Plaka Tespiti", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Temizlik
cap.release()

cv2.destroyAllWindows()