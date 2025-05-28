#%%
import cv2
import pytesseract
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Tesseract yolu
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Plakayı tanıyan modelin eklenmesi
model = YOLO('best.pt')

# Kayıt edilen plakaları tutan set
registered_plates = set()

# TXT'nin içindeki plakaların set'e eklenmesi
if os.path.exists('plates.txt'):
    with open('plates.txt', 'r', encoding='utf-8') as f:
        for line in f:
            registered_plates.add(line.strip())

# Plakaları TXT'ye kaydeden fonksiyon
def save_plate_to_txt(plate):
    with open('plates.txt', 'a', encoding='utf-8') as f:
        f.write(plate + '\n')

# Görüntü işleme ve plakayı çıkarma
def process_image(image_path):
    img = cv2.imread(image_path)
    results = model(img)[0]

    plate_texts = []  # Çoklu plakaları tutan liste

    if not results.boxes:
        return ["! Plaka tespit edilemedi."], img

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        plate_roi = img[y1:y2, x1:x2]

        gray = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contrast = cv2.convertScaleAbs(thresh, alpha=1.5, beta=0)

        config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        text = pytesseract.image_to_string(contrast, config=config)
        plate = ''.join(filter(str.isalnum, text)).strip()

        while plate and plate[0].isalpha():
            plate = plate[1:].strip()

        if plate:
            plate_texts.append(plate)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, plate, (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            plate_texts.append("! Plaka okunamadı")

    return plate_texts, img

# Resim seçme ve işleme
def select_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Görüntü dosyaları", "*.jpg *.png *.jpeg")],
        title="Plakası Okunacak Araç Seçimi")

    if file_path:
        results, processed_img = process_image(file_path)

        found_any = False
        for result in results:
            if result.startswith("!"):
                continue

            found_any = True
            if result in registered_plates:
                messagebox.showinfo("Bilgi", f"{result} plakalı araç zaten kayıtlı!")
            else:
                registered_plates.add(result)
                result_area.insert(tk.END, result + '\n')
                save_plate_to_txt(result)

        result_label.config(text="Okunan Plakalar:\n" + '\n'.join(results) if found_any else results[0])

        processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(processed_img).resize((250, 250))
        img_tk = ImageTk.PhotoImage(img_pil)
        image_label.config(image=img_tk)
        image_label.image = img_tk

# Arayüz
form = tk.Tk()
form.title('Plaka Tanıma Sistemi')
form.geometry('600x650')

tk.Label(form, text="📷 Plaka Okuma Uygulaması", font=("Arial", 16), bg="#032263", fg="#E6EEFE").pack(fill="x")
tk.Button(form, text="Resim Seç", command=select_image, font=("Arial", 12), bg="#E6EEFE", fg="#021132").pack(pady=10)

result_label = tk.Label(form, text="", font=("Arial", 12, "bold"), fg="#021132")
result_label.pack(pady=10)

image_label = tk.Label(form)
image_label.pack(pady=10)

tk.Label(form, text="Kayıtlı Araçlar:", font=("Arial", 12), bg="#032263", fg="#E6EEFE").pack(fill="x")
result_area = tk.Text(form, height=8, width=40, font=("Consolas", 12))
result_area.pack(pady=10)

# Kayıtlı plakaları göstrme
for plate in registered_plates:
    result_area.insert(tk.END, plate + '\n')

form.mainloop()