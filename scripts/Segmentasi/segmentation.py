import cv2
import numpy as np

def create_leaf_mask(hsv_image):
    """
    Membuat mask daun berdasarkan rentang HSV (threshold W1).
    Parameter:
        hsv_image: citra dalam ruang warna HSV
    Return:
        mask daun (binary image)
    """

    # Threshold hasil tuning W1 (contoh hasil dari find_threshold.py)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])

    # Buat mask daun
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Opsional: bersihkan noise dengan morfologi
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask


# Contoh penggunaan mandiri (uji fungsi)
if __name__ == "__main__":
    # Baca gambar daun tomat
    img = cv2.imread('scripts\Segmentasi\daun_tomat.jpg')
    if img is None:
        raise ValueError

    # Konversi ke HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Buat mask daun
    leaf_mask = create_leaf_mask(hsv)

    # Terapkan mask pada gambar asli
    result = cv2.bitwise_and(img, img, mask=leaf_mask)

    # Tampilkan hasil
    cv2.imshow('Original', img)
    cv2.imshow('Leaf Mask (W1)', leaf_mask)
    cv2.imshow('Segmented Leaf', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
