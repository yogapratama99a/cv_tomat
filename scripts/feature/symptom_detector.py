import cv2
import numpy as np

def get_symptom_mask(hsv_image):
    """
    Mendeteksi gejala penyakit tanaman dari gambar HSV dan menghasilkan mask yang sudah dibersihkan.
    
    Args:
        hsv_image (numpy.ndarray): Gambar input dalam format HSV
        
    Returns:
        numpy.ndarray: Mask biner (0-255) yang menunjukkan area gejala penyakit
    """
    # Define HSV ranges for different symptom colors
    # Brown symptoms (necrosis, brown spots)
    brown_lower = np.array([0, 50, 30])
    brown_upper = np.array([20, 200, 150])
    
    # Yellow symptoms (chlorosis, yellowing)
    yellow_lower = np.array([20, 80, 80])
    yellow_upper = np.array([35, 255, 200])
    
    # Create masks for each symptom type
    brown_mask = cv2.inRange(hsv_image, brown_lower, brown_upper)
    yellow_mask = cv2.inRange(hsv_image, yellow_lower, yellow_upper)
    
    # Combine all symptom masks
    combined_mask = cv2.bitwise_or(brown_mask, yellow_mask)
    
    # Apply morphological operations to clean the mask
    cleaned_mask = apply_morphological_operations(combined_mask)
    
    return cleaned_mask

def apply_morphological_operations(mask):
    """
    Membersihkan mask menggunakan operasi morfologi OPEN dan CLOSE.
    
    Args:
        mask (numpy.ndarray): Mask biner input
        
    Returns:
        numpy.ndarray: Mask yang sudah dibersihkan dari noise
    """
    # Create kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)
    
    # Step 1: OPENING (erosion followed by dilation)
    # Menghilangkan noise kecil dan objek kecil di luar area utama
    cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Step 2: CLOSING (dilation followed by erosion)  
    # Menutup lubang kecil dan menyatukan area yang terputus
    cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, kernel)
    
    return cleaned_mask

def calculate_symptom_percentage(mask):
    """
    Menghitung persentase area gejala terhadap total area gambar.
    
    Args:
        mask (numpy.ndarray): Mask gejala
        
    Returns:
        float: Persentase area gejala (0-100)
    """
    total_pixels = mask.shape[0] * mask.shape[1]
    symptom_pixels = np.sum(mask > 0)
    percentage = (symptom_pixels / total_pixels) * 100
    return percentage

def visualize_detection(original_image, symptom_mask, percentage=None):
    """
    Memvisualisasikan hasil deteksi gejala pada gambar asli.
    
    Args:
        original_image (numpy.ndarray): Gambar asli (BGR)
        symptom_mask (numpy.ndarray): Mask gejala
        percentage (float, optional): Persentase gejala
        
    Returns:
        numpy.ndarray: Gambar dengan visualisasi hasil deteksi
    """
    # Create a copy of the original image
    result_image = original_image.copy()
    
    # Create colored overlay for symptoms (red color)
    overlay = result_image.copy()
    overlay[symptom_mask > 0] = [0, 0, 255]  # Red color for symptoms
    
    # Blend overlay with original image
    alpha = 0.3  # Transparency
    cv2.addWeighted(overlay, alpha, result_image, 1 - alpha, 0, result_image)
    
    # Add contour of symptoms
    contours, _ = cv2.findContours(symptom_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(result_image, contours, -1, (0, 0, 255), 2)
    
    # Add information text
    if percentage is not None:
        text = f"Symptom Area: {percentage:.2f}%"
        cv2.putText(result_image, text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Add status based on percentage
    if percentage is not None:
        if percentage > 10:
            status = "SEVERE"
            color = (0, 0, 255)  # Red
        elif percentage > 5:
            status = "MODERATE" 
            color = (0, 165, 255)  # Orange
        elif percentage > 1:
            status = "MILD"
            color = (0, 255, 255)  # Yellow
        else:
            status = "HEALTHY"
            color = (0, 255, 0)  # Green
            
        cv2.putText(result_image, f"Status: {status}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    return result_image

def detect_symptom_type(hsv_image, symptom_mask):
    """
    Mendeteksi jenis gejala berdasarkan warna dominan.
    
    Args:
        hsv_image (numpy.ndarray): Gambar HSV asli
        symptom_mask (numpy.ndarray): Mask gejala
        
    Returns:
        dict: Informasi tentang jenis dan persentase setiap gejala
    """
    # Define HSV ranges
    brown_lower = np.array([0, 50, 30])
    brown_upper = np.array([20, 200, 150])
    yellow_lower = np.array([20, 80, 80])
    yellow_upper = np.array([35, 255, 200])
    
    # Create individual masks
    brown_mask = cv2.inRange(hsv_image, brown_lower, brown_upper)
    yellow_mask = cv2.inRange(hsv_image, yellow_lower, yellow_upper)
    
    # Clean individual masks
    brown_mask = apply_morphological_operations(brown_mask)
    yellow_mask = apply_morphological_operations(yellow_mask)
    
    # Calculate percentages
    total_pixels = symptom_mask.shape[0] * symptom_mask.shape[1]
    brown_pixels = np.sum(brown_mask > 0)
    yellow_pixels = np.sum(yellow_mask > 0)
    
    brown_percentage = (brown_pixels / total_pixels) * 100
    yellow_percentage = (yellow_pixels / total_pixels) * 100
    
    # Determine dominant symptom
    if brown_percentage > yellow_percentage:
        dominant = "BROWN"
    elif yellow_percentage > brown_percentage:
        dominant = "YELLOW"
    else:
        dominant = "MIXED"
    
    return {
        'brown_percentage': brown_percentage,
        'yellow_percentage': yellow_percentage,
        'dominant_symptom': dominant,
        'brown_mask': brown_mask,
        'yellow_mask': yellow_mask
    }

# Example usage and testing
if __name__ == "__main__":
    # Load sample image
    image_path = "tomato_leaf.jpg"  # Ganti dengan path gambar Anda
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Cannot load image. Please check the file path.")
        exit()
    
    # Convert to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Get symptom mask using the main function
    symptom_mask = get_symptom_mask(hsv_image)
    
    # Calculate symptom percentage
    percentage = calculate_symptom_percentage(symptom_mask)
    
    # Detect symptom types
    symptom_info = detect_symptom_type(hsv_image, symptom_mask)
    
    # Create visualization
    result_visualization = visualize_detection(image, symptom_mask, percentage)
    
    # Display results
    print("=" * 50)
    print("SYMPTOM DETECTION RESULTS")
    print("=" * 50)
    print(f"Total Symptom Area: {percentage:.2f}%")
    print(f"Brown Symptoms: {symptom_info['brown_percentage']:.2f}%")
    print(f"Yellow Symptoms: {symptom_info['yellow_percentage']:.2f}%")
    print(f"Dominant Symptom: {symptom_info['dominant_symptom']}")
    print("=" * 50)
    
    # Show images
    cv2.imshow("Original Image", image)
    cv2.imshow("Symptom Mask", symptom_mask)
    cv2.imshow("Detection Result", result_visualization)
    
    # Show individual symptom masks if available
    if symptom_info['brown_mask'] is not None:
        cv2.imshow("Brown Symptoms", symptom_info['brown_mask'])
    if symptom_info['yellow_mask'] is not None:
        cv2.imshow("Yellow Symptoms", symptom_info['yellow_mask'])
    
    print("Press any key to close windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save results if needed
    save_results = input("Save results? (y/n): ").lower()
    if save_results == 'y':
        cv2.imwrite("symptom_mask.jpg", symptom_mask)
        cv2.imwrite("detection_result.jpg", result_visualization)
        print("Results saved as 'symptom_mask.jpg' and 'detection_result.jpg'")