# Plaka Tanıma Sistemi

Bu proje, araç plakalarını otomatik olarak algılayıp tanımayı amaçlayan bir plaka tanıma sistemidir. Sistem, nesne algılama için **YOLOv8**, optik karakter tanıma (OCR) için ise **Tesseract OCR** teknolojilerini bir araya getirerek geliştirilmiştir.

## Proje Süreci ve Görev Dağılımı

| Ekip Üyesi | Görevi |
|------------|--------|
| **Tunahan** | Modelin eğitimi ve doğruluk analizlerinin gerçekleştirilmesi |
| **Oğuz** | Kullanıcı arayüzü tasarımı ve entegrasyonu |
| **Veysel** | Eğitilen modelin gerçek zamanlı plaka tespiti ve **Tesseract** ile okuma işlemlerinin yapılması |

## Kullanılan Teknolojiler

- **YOLOv8**: Nesne tespiti için kullanıldı (plaka bölgesini algılamak amacıyla).
- **Tesseract OCR**: Algılanan plaka bölgesinden metin okunması için kullanıldı.
- **Python** ve ilgili kütüphaneler (OpenCV, Ultralytics YOLO, pytesseract)
- **PyQt / Tkinter (veya ilgili arayüz kütüphanesi)**: Arayüz tasarımı için

## Model Eğitimi ve Doğruluk

Aşağıdaki grafik, YOLOv8 modeliyle eğittiğimiz plaka tespit modelinin eğitim sürecindeki doğruluk, kayıp ve başarı metriklerini göstermektedir:

![Eğitim Doğruluk Grafiği](./50292f99-38f6-43e9-80a2-9135251fa527.png)

### Açıklama:

- **Loss değerleri (train/val)** eğitim süreci boyunca istikrarlı bir şekilde azalmış, bu da modelin başarılı bir şekilde öğrenme gerçekleştirdiğini göstermektedir.
- **mAP50 ve mAP50-95** gibi doğruluk metrikleri zamanla artmış ve yüksek değerlere ulaşmıştır (>%90).
- **Precision (kesinlik)** ve **Recall (duyarlılık)** değerleri de neredeyse 1’e ulaşmıştır, bu da plaka tespitinde yüksek doğruluk sağlandığını gösterir.

## Sistem Akışı

1. **Giriş**: Kullanıcıdan gelen görüntü alınır.
2. **Tespit**: YOLOv8 modeli ile görüntüdeki plaka bölgesi tespit edilir.
3. **OCR**: Algılanan plaka bölgesi Tesseract ile işlenerek karakterler okunur.
4. **Çıktı**: Arayüzde plakadaki metin kullanıcıya gösterilir.
