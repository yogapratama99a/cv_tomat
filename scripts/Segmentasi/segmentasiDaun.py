import cv2
import numpy as np

# Baca gambar
img = cv2.imread('scripts\Segmentasi\daun_tomat.jpg')
if img is None:
    raise ValueError

# Ubah ke ruang warna HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Estimasi rentang warna hijau (bisa disesuaikan hasil risetmu)
lower_green = np.array([35, 40, 40])
upper_green = np.array([85, 255, 255])

# Segmentasi warna hijau
mask = cv2.inRange(hsv, lower_green, upper_green)

# Temukan kontur area hijau (daun)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Gambar kontur di atas gambar asli
result = img.copy()
cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

# Tampilkan hasil
cv2.imshow('Asli', img)
cv2.imshow('Mask Hijau', mask)
cv2.imshow('Hasil Segmentasi Daun', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
