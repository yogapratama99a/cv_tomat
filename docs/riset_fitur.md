# 🧩 Riset Fitur Extraction - cv2.mean() dan Mask Creation

## 1. 📘 Fungsi `cv2.mean(image, mask)`

### Deskripsi
`cv2.mean()` digunakan untuk menghitung nilai rata-rata dari setiap channel warna pada area yang ditentukan oleh *mask*.

### Sintaks
```python
mean_values = cv2.mean(image, mask=None)
````

### Parameter

| Parameter | Deskripsi                                                                     |
| --------- | ----------------------------------------------------------------------------- |
| **image** | Gambar input (BGR, HSV, atau grayscale)                                       |
| **mask**  | Area yang ingin dihitung rata-ratanya (nilai 255 = area aktif, 0 = diabaikan) |

### Nilai Kembalian

* Jika gambar berwarna (BGR): `(mean_B, mean_G, mean_R, alpha)`
* Jika gambar grayscale: `(mean_gray, 0, 0, 0)`

### Contoh Penggunaan

```python
import cv2
import numpy as np

image = cv2.imread('tomat.jpg')
mask = np.zeros(image.shape[:2], np.uint8)
mask[100:200, 100:200] = 255  # area persegi untuk analisis

mean_val = cv2.mean(image, mask=mask)
print("Mean BGR:", mean_val)
```

---

## 2. 🎭 Pembuatan Mask

*Mask* digunakan untuk menandai area spesifik yang akan dianalisis dari gambar.

### Contoh

```python
mask = np.zeros(image.shape[:2], np.uint8)
cv2.rectangle(mask, (50, 50), (150, 150), 255, -1)
```

Mask berisi nilai **255 (putih)** di area yang akan dihitung dan **0 (hitam)** di area yang diabaikan.

---

## 3. 🧮 Implementasi Fungsi `get_mean_hue()`

```python
import cv2
import numpy as np

def get_mean_hue(image, contours):
    
    # Menghitung mean hue untuk setiap kontur menggunakan cv2.mean() dan mask
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mean_hues = []

    for contour in contours:
        mask = np.zeros(image.shape[:2], np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, -1)

        mean_val = cv2.mean(hsv_image, mask=mask)
        mean_hues.append(mean_val[0])  # ambil nilai hue

    return mean_hues
```

---

## 4. 🌿 Studi Kasus: Deteksi Kondisi Daun Tomat Berdasarkan Warna

### 🎯 Tujuan

Menerapkan konsep `cv2.mean()` dan *mask creation* untuk mendeteksi **kondisi fisiologis daun tomat** (Segar, Layu, atau Busuk) menggunakan analisis warna pada ruang warna **HSV**.

---

### 🧠 Langkah-Langkah Utama

#### 1. Konversi Warna

Gambar daun dikonversi dari BGR → HSV agar mudah menganalisis **Hue (warna dominan)**, **Saturation (kejenuhan)**, dan **Value (kecerahan)**.

```python
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
```

---

#### 2. Segmentasi Warna Daun

Gunakan rentang warna hijau untuk mengekstraksi area daun.

```python
lower_green = np.array([25, 30, 30])
upper_green = np.array([90, 255, 255])
mask = cv2.inRange(hsv_image, lower_green, upper_green)
```

---

#### 3. Deteksi Kontur dan Mask Individual

Temukan kontur daun lalu buat *mask* untuk setiap kontur yang ditemukan.

```python
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    mask = np.zeros(image.shape[:2], np.uint8)
    cv2.drawContours(mask, [contour], -1, 255, -1)
```

---

#### 4. Ekstraksi Fitur Warna

Hitung nilai rata-rata **Hue, Saturation, Value** pada setiap kontur menggunakan `cv2.mean()`.

```python
mean_hsv = cv2.mean(hsv_image, mask=mask)
```

Contoh hasil:

| Kontur | Mean Hue | Mean Saturation | Mean Value |
| ------ | -------- | --------------- | ---------- |
| 0      | 64.2     | 148.5           | 102.3      |
| 1      | 28.4     | 85.7            | 65.4       |

---

#### 5. Klasifikasi Kondisi Daun

Daun dikategorikan berdasar nilai HSV:

| Kondisi   | Hue          | Saturation | Value |
| --------- | ------------ | ---------- | ----- |
| **Segar** | 35–85        | >100       | >70   |
| **Layu**  | 25–35        | 40–100     | 40–80 |
| **Busuk** | <25 atau >90 | <50        | <60   |

```python
def classify_leaf_condition(hue, saturation, value):
    if 35 <= hue <= 85 and saturation > 100 and value > 70:
        return "Segar"
    elif 25 <= hue < 35 and 40 <= saturation <= 100 and 40 <= value <= 80:
        return "Layu"
    elif hue < 25 or hue > 90 or saturation < 50 or value < 60:
        return "Busuk"
    else:
        return "Tidak Diketahui"
```

---

#### 6. Visualisasi dan Output JSON

Berikan label kondisi daun dan simpan hasilnya.

```python
cv2.putText(result_image, condition, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
cv2.imwrite('hasil_deteksi_kondisi_daun.jpg', result_image)
```

Contoh output JSON:

```json
[
    {
        "mean_hue": 64.2,
        "mean_saturation": 148.5,
        "mean_value": 102.3,
        "condition": "Segar"
    },
    {
        "mean_hue": 28.4,
        "mean_saturation": 85.7,
        "mean_value": 65.4,
        "condition": "Layu"
    }
]
```

---

### ✅ Kesimpulan

Metode ini memperluas konsep dasar `cv2.mean()` dan *mask creation* menjadi penerapan nyata di bidang **visi komputer pertanian (Agricultural Computer Vision)**.
Dengan teknik ini, sistem dapat:

* Mengekstraksi area daun secara akurat,
* Menghitung intensitas warna,
* Mengidentifikasi kondisi fisiologis daun tomat berdasarkan warna.