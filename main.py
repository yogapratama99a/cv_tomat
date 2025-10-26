import cv2
import time

# URL dari Arduino IDE
# IP harus sesuai dengan Serial Monitor Arduino IDE
URL_STREAM = "http://192.168.1.10/stream" 

# --- (Opsional) Import skrip anggota lain (masih kosong/skeleton) ---
# import scripts.preprocess as pp
# import scripts.segmentation as seg
# import scripts.find_objects as det
# import scripts.extract_features as feat


print(f"Mencoba menyambung ke stream: {URL_STREAM}...")
cap = cv2.VideoCapture(URL_STREAM)

# Cek apakah koneksi berhasil
if not cap.isOpened():
    print("==============================================")
    print("Error: Tidak bisa membuka stream.")
    print(f"Pastikan URL ({URL_STREAM}) sudah benar dan ESP32-CAM terhubung ke WiFi.")
    print("==============================================")
    exit()

print("Berhasil terhubung ke stream ESP32-CAM.")
print("Tekan 'q' pada jendela video untuk keluar.")

# Ini adalah 'main loop' aplikasi Anda
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Gagal mengambil frame. Mencoba menyambung kembali...")
        cap.release()
        cap = cv2.VideoCapture(URL_STREAM)
        time.sleep(1)
        continue

    
    # 1. Panggil Anggota 2 (Preprocessing)
    #    hsv_image = pp.clean_image(frame)
    
    # 2. Panggil Anggota 3 (Segmentasi)
    #    mask = seg.create_mask(hsv_image)
    
    # 3. Panggil Anggota 4 (Deteksi Objek)
    #    coordinates = det.find_all_tomatoes(mask)
    
    # 4. Panggil Anggota 5 (Ekstraksi Fitur)
    #    features = feat.get_features(hsv_image, coordinates)
    
    # 5. Visualisasikan (Tugas Anda nanti)
    #    annotated_frame = draw_results(frame, coordinates, features)
    
    # --- Output W1-P2 ---
    # Untuk minggu ini, kita hanya tampilkan frame aslinya
    cv2.imshow("Live Feed ESP32-CAM (Tugas Anggota 6)", frame)

    # Cek jika tombol 'q' ditekan untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Menutup stream...")
cap.release()
cv2.destroyAllWindows()