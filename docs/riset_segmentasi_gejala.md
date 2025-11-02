# Riset Segmentasi Warna Gejala (Coklat & Kuning)

## Range HSV untuk Warna Coklat
- **Lower Bound**: [10, 60, 20]
- **Upper Bound**: [20, 180, 120]
- **Karakteristik**: Hue rendah, Saturation medium, Value medium

## Range HSV untuk Warna Kuning
- **Lower Bound**: [20, 80, 80]
- **Upper Bound**: [35, 255, 255]
- **Karakteristik**: Hue medium, Saturation tinggi, Value tinggi

## Catatan:
- Warna coklat pada HSV memiliki hue yang mirip dengan orange/merah tapi dengan value yang lebih rendah
- Lighting condition sangat mempengaruhi hasil segmentasi
- Disarankan untuk tuning menggunakan find_threshold.py

# Menjalankan tuning tool
python find_symptom_threshold.py --image path/to/leaf_image.jpg

# Contoh penggunaan dalam code
from symptom_config import get_brown_threshold, get_yellow_threshold

# Untuk segmentasi gejala coklat
lower_brown, upper_brown = get_brown_threshold()
mask_brown = cv2.inRange(hsv_image, lower_brown, upper_brown)

# Untuk segmentasi gejala kuning  
lower_yellow, upper_yellow = get_yellow_threshold()
mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

# Untuk Run Code gunakan Tamplate ini
python find_symptom_threshold.py --image "Path Image" --output "Path Output"