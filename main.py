import cv2
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage import median_filter, gaussian_filter
from sklearn.cluster import KMeans
from skimage import filters, segmentation
import warnings
warnings.filterwarnings('ignore')

PROJECT_DIR = Path(__file__).parent.resolve()
IMAGES_DIR = PROJECT_DIR / "images"
RESULTS_DIR = PROJECT_DIR / "results"
STEP1_DIR = RESULTS_DIR / "step1"
STEP2_DIR = RESULTS_DIR / "step2"

for d in [IMAGES_DIR, STEP1_DIR, STEP2_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def create_sample_medical_images():
    
    image_files = {
        "low": IMAGES_DIR / "m_low.jpg",
        "mid": IMAGES_DIR / "m_mid.jpg",
        "high": IMAGES_DIR / "m_high.jpg"
    }
    
    images = []
    image_names = []
    
    for detail_level, file_path in [("low_detail", image_files["low"]), 
                                     ("medium_detail", image_files["mid"]),
                                     ("high_detail", image_files["high"])]:
        if file_path.exists():
            img = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
                image_names.append(detail_level)
    
    if images:
        return images
    else:
        return []


def add_uniform_noise(image, probability):
    noisy = image.copy().astype(float)
    mask = np.random.random(image.shape) < probability
    noisy[mask] = np.random.uniform(0, 255, np.sum(mask))
    return np.clip(noisy, 0, 255).astype(np.uint8)


def compute_psnr(original, filtered):
    mse = np.mean((original.astype(float) - filtered.astype(float)) ** 2)
    if mse == 0:
        return float('inf')
    max_val = 255.0
    psnr = 20 * np.log10(max_val / np.sqrt(mse))
    return psnr


def compute_ssim(original, filtered):
    from skimage.metrics import structural_similarity as ssim
    return ssim(original, filtered, data_range=255)

def bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    return cv2.bilateralFilter(image.astype(np.uint8), d, sigma_color, sigma_space)


def median_filter_ep(image, kernel_size=5):
    return cv2.medianBlur(image.astype(np.uint8), kernel_size)


def guided_filter(image, radius=8, eps=0.4):
    return cv2.ximgproc.guidedFilter(image.astype(np.uint8), image.astype(np.uint8), radius, eps)


def apply_filter(image, filter_name, kernel_size):
    try:
        if filter_name == "bilateral":
            if kernel_size == 5:
                return bilateral_filter(image, d=5, sigma_color=50, sigma_space=50)
            else:
                return bilateral_filter(image, d=15, sigma_color=100, sigma_space=100)
        
        elif filter_name == "median":
            return median_filter_ep(image, kernel_size)
        
        elif filter_name == "guided":
            if kernel_size == 5:
                return guided_filter(image, radius=2, eps=0.4)
            else:
                return guided_filter(image, radius=8, eps=0.4)
    except Exception as e:
        return image
    
    return image

def kmeans_segmentation(image, n_clusters=2):
    pixels = image.reshape(-1, 1).astype(np.float32)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, n_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)
    segmented = centers[labels.flatten()]
    return segmented.reshape(image.shape)


def split_merge_segmentation(image, depth=4):
    def is_uniform(region, threshold=10):
        return region.std() < threshold
    
    def split_merge_recursive(img, min_size=4):
        if is_uniform(img) or img.shape[0] <= min_size:
            return np.ones_like(img, dtype=np.uint8) * int(img.mean())
        
        h, w = img.shape
        h2, w2 = h // 2, w // 2
        
        tl = split_merge_recursive(img[:h2, :w2], min_size)
        tr = split_merge_recursive(img[:h2, w2:], min_size)
        bl = split_merge_recursive(img[h2:, :w2], min_size)
        br = split_merge_recursive(img[h2:, w2:], min_size)
        
        result = np.zeros_like(img, dtype=np.uint8)
        result[:h2, :w2] = tl
        result[:h2, w2:] = tr
        result[h2:, :w2] = bl
        result[h2:, w2:] = br
        
        return result
    
    return split_merge_recursive(image)


def otsu_thresholding_segmentation(image):
    _, segmented = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return segmented

def run_step1_experiment():
    
    images = create_sample_medical_images()
    image_names = ["low_detail", "medium_detail", "high_detail"]
    
    filters = ["bilateral", "median", "guided"]
    noise_levels = [0.1, 0.5, 0.8]
    kernel_sizes = [5, 15]
    
    results_metrics = {}
    
    for img_idx, (image, img_name) in enumerate(zip(images, image_names)):
        
        for noise_level in noise_levels:
            noisy_img = add_uniform_noise(image, noise_level)
            
            for kernel_size in kernel_sizes:
                
                for filter_name in filters:
                    filtered = apply_filter(noisy_img, filter_name, kernel_size)
                    
                    psnr = compute_psnr(image, filtered)
                    ssim_val = compute_ssim(image, filtered)
                    
                    key = f"{img_name}_{noise_level}_{kernel_size}_{filter_name}"
                    results_metrics[key] = {"psnr": psnr, "ssim": ssim_val, "image": filtered}
                    
                    result_path = STEP1_DIR / f"{img_name}_{noise_level:.1f}_{kernel_size}_{filter_name}.png"
                    cv2.imwrite(str(result_path), filtered)
    
    return results_metrics

def run_step2_experiment(best_filter="bilateral"):
    
    images = create_sample_medical_images()
    image_names = ["low_detail", "medium_detail", "high_detail"]
    
    segmentation_methods = ["kmeans", "split_merge", "otsu"]
    noise_levels = [None, 0.1, 0.5, 0.8]
    kernel_sizes = [None, 5, 15]
    
    results_metrics = {}
    
    for img_idx, (image, img_name) in enumerate(zip(images, image_names)):
        
        for noise_level in noise_levels:
            if noise_level is None:
                test_img = image
                noise_str = "no_noise"
            else:
                test_img = add_uniform_noise(image, noise_level)
                noise_str = f"noise_{noise_level:.1f}"
            
            for kernel_size in kernel_sizes:
                if kernel_size is None:
                    filtered_img = test_img
                    filter_str = "no_filter"
                else:
                    filtered_img = apply_filter(test_img, best_filter, kernel_size)
                    filter_str = f"filter_{kernel_size}"
                
                for seg_method in segmentation_methods:
                    if seg_method == "kmeans":
                        segmented = kmeans_segmentation(filtered_img, n_clusters=2)
                    elif seg_method == "split_merge":
                        segmented = split_merge_segmentation(filtered_img)
                    else:
                        segmented = otsu_thresholding_segmentation(filtered_img)
                    
                    result_path = STEP2_DIR / f"{img_name}_{noise_str}_{filter_str}_{seg_method}.png"
                    cv2.imwrite(str(result_path), segmented)
                    
                    key = f"{img_name}_{noise_str}_{filter_str}_{seg_method}"
                    results_metrics[key] = {"segmented": segmented}
    
    return results_metrics

def main():
    
    step1_metrics = run_step1_experiment()
    
    best_filters = {}
    for img_name in ["low_detail", "medium_detail", "high_detail"]:
        best_psnr = -float('inf')
        best_filter = None
        for key, metrics in step1_metrics.items():
            if img_name in key:
                if metrics["psnr"] > best_psnr:
                    best_psnr = metrics["psnr"]
                    best_filter = key.split("_")[-1]
        best_filters[img_name] = best_filter
    
    best_overall_filter = "bilateral"
    
    step2_metrics = run_step2_experiment(best_overall_filter)
    
    return step1_metrics, step2_metrics


if __name__ == "__main__":
    step1_results, step2_results = main()
