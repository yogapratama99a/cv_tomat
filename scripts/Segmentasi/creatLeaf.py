import cv2
import numpy as np

def create_leaf_mask(hsv_image):
    """
    Membuat mask daun berdasarkan rentang HSV (threshold W1),
    serta membersihkan noise menggunakan operasi morfologi OPEN dan CLOSE.
    Parameter:
        hsv_image: citra dalam ruang warna HSV
    Return:
        mask daun (binary image yang bersih)
    """

    # Threshold hasil tuning W1 (daun hijau)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])

    # Buat mask daun dari rentang HSV
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # --- Bersihkan noise ---
    kernel = np.ones((5, 5), np.uint8)

    # 1️⃣ OPEN: menghapus noise kecil (bintik putih di area gelap)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 2️⃣ CLOSE: menutup lubang kecil di dalam area daun
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask


# --- Contoh Penggunaan ---
if __name__ == "__main__":
    img = cv2.imread('scripts\Segmentasi\daun_tomat.jpg')
    if img is None:
        raise ValueError

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Panggil fungsi mask daun
    leaf_mask = create_leaf_mask(hsv)

    # Terapkan mask pada gambar asli
    result = cv2.bitwise_and(img, img, mask=leaf_mask)

    # Tampilkan hasil
    cv2.imshow('Asli', img)
    cv2.imshow('Mask Daun (Bersih)', leaf_mask)
    cv2.imshow('Segmentasi Daun', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
