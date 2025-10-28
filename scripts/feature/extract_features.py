import cv2
import numpy as np
import json
import os

# ==== Fungsi klasifikasi kondisi daun berdasarkan nilai HSV ====
def classify_leaf_condition(hue, saturation, value):
    if 35 <= hue <= 85 and saturation > 100 and value > 70:
        return "Segar"
    elif 25 <= hue < 35 and 40 <= saturation <= 100 and 40 <= value <= 80:
        return "Layu"
    elif hue < 25 or hue > 90 or saturation < 50 or value < 60:
        return "Busuk"
    else:
        return "Tidak Diketahui"

# ==== Ekstraksi fitur warna ====
def extract_color_features(image, contours):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_features = []

    for contour in contours:
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, -1)

        mean_hsv = cv2.mean(hsv_image, mask=mask)
        mean_bgr = cv2.mean(image, mask=mask)

        condition = classify_leaf_condition(mean_hsv[0], mean_hsv[1], mean_hsv[2])

        color_features.append({
            'mean_hue': float(mean_hsv[0]),
            'mean_saturation': float(mean_hsv[1]),
            'mean_value': float(mean_hsv[2]),
            'mean_blue': float(mean_bgr[0]),
            'mean_green': float(mean_bgr[1]),
            'mean_red': float(mean_bgr[2]),
            'condition': condition
        })

    return color_features

# ==== Visualisasi hasil pada gambar ====
def visualize_leaf_conditions(image, contours, features):
    result_image = image.copy()
    for i, (contour, feature) in enumerate(zip(contours, features)):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.drawContours(result_image, [contour], -1, (0, 255, 0), 2)
        text = f"{feature['condition']}"
        cv2.putText(result_image, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return result_image

# ==== Main program ====
if __name__ == "__main__":
    base_dir = r"C:\tomato_project\cv_tomat"
    image_path = os.path.join(base_dir, "test_images", "tomato_leaf_test01.jpg")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Gambar tidak bisa diload dari {image_path}")
        exit()

    # Segmentasi warna daun
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([25, 30, 30])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Ditemukan {len(contours)} kontur daun")

    # Ekstraksi warna dan klasifikasi
    color_features = extract_color_features(image, contours)

    print("\n=== HASIL DETEKSI KONDISI DAUN ===")
    for i, feature in enumerate(color_features):
        print(f"Daun {i}: Hue={feature['mean_hue']:.1f}, S={feature['mean_saturation']:.1f}, V={feature['mean_value']:.1f}")
        print(f"→ Kondisi: {feature['condition']}\n")

    # Simpan hasil visualisasi dan data
    result_img = visualize_leaf_conditions(image, contours, color_features)
    image_output_path = os.path.join(output_dir, "hasil_deteksi_kondisi_daun.jpg")
    json_output_path = os.path.join(output_dir, "daun_kondisi.json")

    cv2.imwrite(image_output_path, result_img)
    with open(json_output_path, "w") as f:
        json.dump(color_features, f, indent=4)

    print(f"Gambar hasil disimpan di: {image_output_path}")
    print(f"Data fitur disimpan di: {json_output_path}")

    cv2.imshow("Hasil Deteksi Kondisi Daun", result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()