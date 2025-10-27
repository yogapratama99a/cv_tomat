import cv2
import numpy as np
import datetime
import os

# --- 1. FUNGSI KOSONG ---
def empty(a):
    pass

# --- 2. SETUP JENDELA dan GAMBAR ---
# GANTI NAMA FILE INI dengan salah satu gambar tomat Anda
path = 'Tomat Hijau.jpg' 
img = cv2.imread(path)
if img is None:
    print(f"Error: Tidak dapat memuat gambar dari path: {path}")
    exit()

# Ubah ukuran gambar agar lebih kecil dan muat di layar
scale_percent = 50 # Ubah menjadi 50% ukuran asli
width = int(img.shape[1] * scale_percent / 120)
height = int(img.shape[0] * scale_percent / 120)
dim = (width, height)
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
window_name = 'HSV RISet - Atur Ukuran Jendela Ini'
cv2.namedWindow(window_name)

# --- 3. SETUP TRACKBAR (Nilai Awal disetel untuk Hijau) ---
cv2.createTrackbar("H_Min", window_name, 40, 179, empty)
cv2.createTrackbar("S_Min", window_name, 40, 255, empty)
cv2.createTrackbar("V_Min", window_name, 40, 255, empty)
cv2.createTrackbar("H_Max", window_name, 80, 179, empty)
cv2.createTrackbar("S_Max", window_name, 255, 255, empty)
cv2.createTrackbar("V_Max", window_name, 255, 255, empty)

# --- 4. LOOP UTAMA ---
while True:
    # Ambil nilai dari trackbar
    h_min = cv2.getTrackbarPos("H_Min", window_name)
    s_min = cv2.getTrackbarPos("S_Min", window_name)
    v_min = cv2.getTrackbarPos("V_Min", window_name)
    h_max = cv2.getTrackbarPos("H_Max", window_name)
    s_max = cv2.getTrackbarPos("S_Max", window_name)
    v_max = cv2.getTrackbarPos("V_Max", window_name)

    # Definisikan batas
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Terapkan segmentasi
    mask = cv2.inRange(imgHSV, lower, upper)
    
    # Gabungkan semua untuk tampilan ringkas
    h_stack = np.hstack([img, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
    
    # Tampilkan hasilnya
    cv2.imshow(window_name, h_stack)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    
    # Tombol 's' untuk menyimpan hasil segmentasi dan mencatat nilai
    if key == ord('s'):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Simpan screenshot gabungan (sebagai bukti visual)
        cv2.imwrite(f'BUKTI_HSV_Riset_{timestamp}.png', h_stack)
        
        # 2. Catat nilai ke file teks (sebagai bukti data)
        file_name = 'CATATAN_HSV_Riset.txt'
        mode = 'a' if os.path.exists(file_name) else 'w'
        with open(file_name, mode) as f:
            f.write(f"\n--- DATA RISet ({timestamp}) ---\n")
            f.write(f"Gambar Uji: {path}\n")
            f.write(f"Lower Bound (Batas Bawah): ({h_min}, {s_min}, {v_min})\n")
            f.write(f"Upper Bound (Batas Atas): ({h_max}, {s_max}, {v_max})\n")
            f.write("-------------------------------------\n")
        
        print(f"Data dan Screenshot disimpan dengan timestamp: {timestamp}")

cv2.destroyAllWindows()