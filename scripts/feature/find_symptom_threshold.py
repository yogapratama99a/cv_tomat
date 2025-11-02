import cv2
import numpy as np
import argparse
import os

def nothing(x):
    # Callback function untuk trackbar
    pass

def create_trackbars(window_name):
    # Membuat trackbar untuk tuning HSV range
    cv2.namedWindow(window_name)
    
    # Trackbar untuk lower bound HSV
    cv2.createTrackbar('H Lower', window_name, 10, 179, nothing)
    cv2.createTrackbar('S Lower', window_name, 60, 255, nothing)
    cv2.createTrackbar('V Lower', window_name, 20, 255, nothing)
    
    # Trackbar untuk upper bound HSV
    cv2.createTrackbar('H Upper', window_name, 20, 179, nothing)
    cv2.createTrackbar('S Upper', window_name, 180, 255, nothing)
    cv2.createTrackbar('V Upper', window_name, 120, 255, nothing)

def get_trackbar_values(window_name):
    # Mendapatkan nilai dari trackbar
    h_low = cv2.getTrackbarPos('H Lower', window_name)
    s_low = cv2.getTrackbarPos('S Lower', window_name)
    v_low = cv2.getTrackbarPos('V Lower', window_name)
    
    h_high = cv2.getTrackbarPos('H Upper', window_name)
    s_high = cv2.getTrackbarPos('S Upper', window_name)
    v_high = cv2.getTrackbarPos('V Upper', window_name)
    
    lower_bound = np.array([h_low, s_low, v_low])
    upper_bound = np.array([h_high, s_high, v_high])
    
    return lower_bound, upper_bound

def apply_morphological_operations(mask):
    # Aplikasikan operasi morfologi untuk membersihkan mask
    # Buat kernel untuk operasi morfologi
    kernel = np.ones((5, 5), np.uint8)
    
    # Closing untuk menghilangkan noise kecil di dalam area
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Opening untuk menghilangkan noise kecil di luar area
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    return mask

def main():
    parser = argparse.ArgumentParser(description='Tuning threshold untuk gejala penyakit tanaman')
    parser.add_argument('--image', type=str, required=True, help='Path ke gambar input')
    parser.add_argument('--output', type=str, default='symptom_config.py', help='Path output untuk konfigurasi')
    args = parser.parse_args()
    
    # Load image
    image = cv2.imread(args.image)
    if image is None:
        print(f"Error: Tidak dapat membuka gambar {args.image}")
        return
    
    # Resize image jika terlalu besar untuk display
    height, width = image.shape[:2]
    if width > 800:
        scale = 800 / width
        new_width = 800
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height))
    
    # Convert ke HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Buat trackbars
    window_name = 'Symptom Threshold Tuning'
    create_trackbars(window_name)
    
    print("=" * 50)
    print("SYMPTOM THRESHOLD TUNING TOOL")
    print("=" * 50)
    print("Penggunaan:")
    print("- Atur trackbar untuk mendapatkan segmentasi optimal")
    print("- Tekan 's' untuk menyimpan nilai threshold")
    print("- Tekan 'c' untuk reset ke nilai default")
    print("- Tekan 'q' untuk keluar")
    print("=" * 50)
    
    while True:
        # Dapatkan nilai trackbar
        lower_bound, upper_bound = get_trackbar_values(window_name)
        
        # Buat mask menggunakan cv2.inRange()
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        
        # Aplikasikan operasi morfologi
        cleaned_mask = apply_morphological_operations(mask)
        
        # Aplikasikan cv2.bitwise_and() untuk mengekstrak region gejala
        result = cv2.bitwise_and(image, image, mask=cleaned_mask)
        
        # Tampilkan informasi nilai threshold
        info_image = image.copy()
        cv2.putText(info_image, f"Lower: [{lower_bound[0]}, {lower_bound[1]}, {lower_bound[2]}]", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(info_image, f"Upper: [{upper_bound[0]}, {upper_bound[1]}, {upper_bound[2]}]", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Tampilkan hasil
        cv2.imshow('Original Image', info_image)
        cv2.imshow('Symptom Mask', cleaned_mask)
        cv2.imshow('Segmented Symptoms', result)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Simpan nilai threshold ke file
            save_config(lower_bound, upper_bound, args.output)
            print(f"\n✅ Nilai threshold disimpan ke: {args.output}")
        elif key == ord('c'):
            # Reset ke nilai default
            cv2.setTrackbarPos('H Lower', window_name, 10)
            cv2.setTrackbarPos('S Lower', window_name, 60)
            cv2.setTrackbarPos('V Lower', window_name, 20)
            cv2.setTrackbarPos('H Upper', window_name, 20)
            cv2.setTrackbarPos('S Upper', window_name, 180)
            cv2.setTrackbarPos('V Upper', window_name, 120)
            print("🔄 Trackbar direset ke nilai default")
    
    cv2.destroyAllWindows()

def save_config(lower_bound, upper_bound, output_path):
    config_content = f'''# Konfigurasi Threshold untuk Gejala Penyakit Tanaman

import numpy as np

# Threshold untuk gejala warna COKLAT (brown spots, necrosis)
BROWN_SYMPTOM = {{
    'lower': [{lower_bound[0]}, {lower_bound[1]}, {lower_bound[2]}],
    'upper': [{upper_bound[0]}, {upper_bound[1]}, {upper_bound[2]}]
}}

# Threshold untuk gejala warna KUNING (yellowing, chlorosis) 
YELLOW_SYMPTOM = {{
    'lower': [20, 80, 80],
    'upper': [35, 255, 255]
}}

# Fungsi utility untuk mendapatkan threshold
def get_brown_threshold():
    # Mengembalikan threshold untuk gejala coklat
    return np.array(BROWN_SYMPTOM['lower']), np.array(BROWN_SYMPTOM['upper'])

def get_yellow_threshold():
    # Mengembalikan threshold untuk gejala kuning
    return np.array(YELLOW_SYMPTOM['lower']), np.array(YELLOW_SYMPTOM['upper'])

if __name__ == "__main__":
    print("Konfigurasi Threshold Gejala:")
    print(f"Brown - Lower: {{BROWN_SYMPTOM['lower']}}, Upper: {{BROWN_SYMPTOM['upper']}}")
    print(f"Yellow - Lower: {{YELLOW_SYMPTOM['lower']}}, Upper: {{YELLOW_SYMPTOM['upper']}}")
'''
    
    with open(output_path, 'w') as f:
        f.write(config_content)

if __name__ == "__main__":
    main()