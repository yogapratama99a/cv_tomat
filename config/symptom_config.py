# Konfigurasi Threshold untuk Gejala Penyakit Tanaman

import numpy as np

# Threshold untuk gejala warna COKLAT (brown spots, necrosis)
BROWN_SYMPTOM = {
    'lower': [10, 60, 20],
    'upper': [20, 180, 120]
}

# Threshold untuk gejala warna KUNING (yellowing, chlorosis) 
YELLOW_SYMPTOM = {
    'lower': [20, 80, 80],
    'upper': [35, 255, 255]
}

# Fungsi utility untuk mendapatkan threshold
def get_brown_threshold():
    # Mengembalikan threshold untuk gejala coklat
    return np.array(BROWN_SYMPTOM['lower']), np.array(BROWN_SYMPTOM['upper'])

def get_yellow_threshold():
    # Mengembalikan threshold untuk gejala kuning
    return np.array(YELLOW_SYMPTOM['lower']), np.array(YELLOW_SYMPTOM['upper'])

if __name__ == "__main__":
    print("Konfigurasi Threshold Gejala:")
    print(f"Brown - Lower: {BROWN_SYMPTOM['lower']}, Upper: {BROWN_SYMPTOM['upper']}")
    print(f"Yellow - Lower: {YELLOW_SYMPTOM['lower']}, Upper: {YELLOW_SYMPTOM['upper']}")
