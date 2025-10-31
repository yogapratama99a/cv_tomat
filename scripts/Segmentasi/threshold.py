import cv2
import numpy as np

def nothing(x):
    pass

# Baca gambar (pastikan path benar)
img = cv2.imread(r'scripts\Segmentasi\daun_tomat.jpg')
if img is None:
    raise ValueError

# Konversi ke HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Buat jendela untuk trackbar
cv2.namedWindow('Tuning HSV')

# Trackbar untuk nilai minimum dan maksimum HSV
cv2.createTrackbar('H Min', 'Tuning HSV', 35, 179, nothing)
cv2.createTrackbar('S Min', 'Tuning HSV', 40, 255, nothing)
cv2.createTrackbar('V Min', 'Tuning HSV', 40, 255, nothing)
cv2.createTrackbar('H Max', 'Tuning HSV', 85, 179, nothing)
cv2.createTrackbar('S Max', 'Tuning HSV', 255, 255, nothing)
cv2.createTrackbar('V Max', 'Tuning HSV', 255, 255, nothing)

while True:
    # Ambil posisi trackbar
    h_min = cv2.getTrackbarPos('H Min', 'Tuning HSV')
    s_min = cv2.getTrackbarPos('S Min', 'Tuning HSV')
    v_min = cv2.getTrackbarPos('V Min', 'Tuning HSV')
    h_max = cv2.getTrackbarPos('H Max', 'Tuning HSV')
    s_max = cv2.getTrackbarPos('S Max', 'Tuning HSV')
    v_max = cv2.getTrackbarPos('V Max', 'Tuning HSV')

    # Buat mask
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower, upper)

    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"H_min={h_min}, S_min={s_min}, V_min={v_min}")
        print(f"H_max={h_max}, S_max={s_max}, V_max={v_max}")
        break

cv2.destroyAllWindows()
