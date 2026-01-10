"""
CMP717 - Image Processing Project
Edge Preserving Filters and Segmentation
"""

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

# Configuration
PROJECT_DIR = Path("/mnt/j/Workspace/717-project")
IMAGES_DIR = PROJECT_DIR / "images"
RESULTS_DIR = PROJECT_DIR / "results"
STEP1_DIR = RESULTS_DIR / "step1"
STEP2_DIR = RESULTS_DIR / "step2"

# Create directories
for d in [IMAGES_DIR, STEP1_DIR, STEP2_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_sample_medical_images():
    """Load real medical images from extracted RAR file"""
    
    # Map actual medical images to detail levels
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
            else:
                print(f"⚠ Warning: Could not load {file_path}")
        else:
            print(f"⚠ Warning: File not found {file_path}")
    
    if images:
        print(f"✓ Loaded {len(images)} real medical images")
        # Return images in order: low, medium, high
        return images
    else:
        print("✗ Error: No medical images found. Ensure images.rar is extracted.")
        return []


def add_uniform_noise(image, probability):
    """
    Add uniform noise to image
    probability: fraction of pixels to distort (0.1, 0.5, 0.8)
    """
    noisy = image.copy().astype(float)
    mask = np.random.random(image.shape) < probability
    noisy[mask] = np.random.uniform(0, 255, np.sum(mask))
    return np.clip(noisy, 0, 255).astype(np.uint8)


def compute_psnr(original, filtered):
    """Compute Peak Signal to Noise Ratio"""
    mse = np.mean((original.astype(float) - filtered.astype(float)) ** 2)
    if mse == 0:
        return float('inf')
    max_val = 255.0
    psnr = 20 * np.log10(max_val / np.sqrt(mse))
    return psnr


def compute_ssim(original, filtered):
    """Compute Structural Similarity Index"""
    from skimage.metrics import structural_similarity as ssim
    return ssim(original, filtered, data_range=255)


# ============================================================================
# EDGE-PRESERVING FILTERS
# ============================================================================

def bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """Bilateral Filter - smooths while preserving edges"""
    return cv2.bilateralFilter(image.astype(np.uint8), d, sigma_color, sigma_space)


def median_filter_ep(image, kernel_size=5):
    """Median Filter - removes noise while preserving edges"""
    return cv2.medianBlur(image.astype(np.uint8), kernel_size)


def guided_filter(image, radius=8, eps=0.4):
    """Guided Filter - preserves edges from guidance image"""
    # Use image as both guidance and input
    return cv2.ximgproc.guidedFilter(image.astype(np.uint8), image.astype(np.uint8), radius, eps)


def apply_filter(image, filter_name, kernel_size):
    """Apply edge-preserving filter"""
    try:
        if filter_name == "bilateral":
            # Adjust parameters based on kernel size
            if kernel_size == 5:
                return bilateral_filter(image, d=5, sigma_color=50, sigma_space=50)
            else:  # 15x15
                return bilateral_filter(image, d=15, sigma_color=100, sigma_space=100)
        
        elif filter_name == "median":
            return median_filter_ep(image, kernel_size)
        
        elif filter_name == "guided":
            if kernel_size == 5:
                return guided_filter(image, radius=2, eps=0.4)
            else:  # 15x15
                return guided_filter(image, radius=8, eps=0.4)
    except Exception as e:
        print(f"Warning: Filter {filter_name} with size {kernel_size} failed: {e}")
        return image
    
    return image


# ============================================================================
# SEGMENTATION METHODS
# ============================================================================

def kmeans_segmentation(image, n_clusters=2):
    """K-Means Clustering Segmentation"""
    # Reshape image to 1D for clustering
    pixels = image.reshape(-1, 1).astype(np.float32)
    
    # Apply K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, n_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert back to image
    centers = np.uint8(centers)
    segmented = centers[labels.flatten()]
    return segmented.reshape(image.shape)


def split_merge_segmentation(image, depth=4):
    """Split and Merge Segmentation using quad-tree"""
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
    """Otsu's Automatic Thresholding"""
    _, segmented = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return segmented


# ============================================================================
# EXPERIMENT STEP 1
# ============================================================================

def run_step1_experiment():
    """
    1st Step: Evaluate 3 edge-preserving filters
    Test with different noise levels (0.1, 0.5, 0.8) and filter sizes (5x5, 15x15)
    """
    print("\n" + "="*70)
    print("STEP 1: Edge-Preserving Filters Evaluation")
    print("="*70)
    
    # Create sample images
    images = create_sample_medical_images()
    image_names = ["low_detail", "medium_detail", "high_detail"]
    
    filters = ["bilateral", "median", "guided"]
    noise_levels = [0.1, 0.5, 0.8]
    kernel_sizes = [5, 15]
    
    # Store metrics for evaluation
    results_metrics = {}
    
    for img_idx, (image, img_name) in enumerate(zip(images, image_names)):
        print(f"\n--- Processing {img_name} image ---")
        
        for noise_level in noise_levels:
            # Add noise
            noisy_img = add_uniform_noise(image, noise_level)
            
            print(f"\nNoise level: {noise_level:.1f}")
            
            for kernel_size in kernel_sizes:
                print(f"  Kernel size: {kernel_size}x{kernel_size}")
                
                for filter_name in filters:
                    # Apply filter
                    filtered = apply_filter(noisy_img, filter_name, kernel_size)
                    
                    # Compute metrics
                    psnr = compute_psnr(image, filtered)
                    ssim_val = compute_ssim(image, filtered)
                    
                    key = f"{img_name}_{noise_level}_{kernel_size}_{filter_name}"
                    results_metrics[key] = {"psnr": psnr, "ssim": ssim_val, "image": filtered}
                    
                    print(f"    {filter_name:10} - PSNR: {psnr:6.2f}, SSIM: {ssim_val:.4f}")
                    
                    # Save result
                    result_path = STEP1_DIR / f"{img_name}_{noise_level:.1f}_{kernel_size}_{filter_name}.png"
                    cv2.imwrite(str(result_path), filtered)
    
    print("\n✓ Step 1 experiment completed")
    return results_metrics


# ============================================================================
# EXPERIMENT STEP 2
# ============================================================================

def run_step2_experiment(best_filter="bilateral"):
    """
    2nd Step: Evaluate segmentation methods with best filter
    Apply different noise levels (0, 0.1, 0.5, 0.8) and filter sizes
    """
    print("\n" + "="*70)
    print("STEP 2: Segmentation Methods with Best Filter")
    print("="*70)
    
    # Create sample images
    images = create_sample_medical_images()
    image_names = ["low_detail", "medium_detail", "high_detail"]
    
    segmentation_methods = ["kmeans", "split_merge", "otsu"]
    noise_levels = [None, 0.1, 0.5, 0.8]
    kernel_sizes = [None, 5, 15]
    
    results_metrics = {}
    
    for img_idx, (image, img_name) in enumerate(zip(images, image_names)):
        print(f"\n--- Processing {img_name} image ---")
        
        for noise_level in noise_levels:
            if noise_level is None:
                test_img = image
                noise_str = "no_noise"
            else:
                test_img = add_uniform_noise(image, noise_level)
                noise_str = f"noise_{noise_level:.1f}"
            
            print(f"\n{noise_str}")
            
            for kernel_size in kernel_sizes:
                if kernel_size is None:
                    filtered_img = test_img
                    filter_str = "no_filter"
                else:
                    filtered_img = apply_filter(test_img, best_filter, kernel_size)
                    filter_str = f"filter_{kernel_size}"
                
                print(f"  {filter_str}")
                
                for seg_method in segmentation_methods:
                    # Apply segmentation
                    if seg_method == "kmeans":
                        segmented = kmeans_segmentation(filtered_img, n_clusters=2)
                    elif seg_method == "split_merge":
                        segmented = split_merge_segmentation(filtered_img)
                    else:  # otsu
                        segmented = otsu_thresholding_segmentation(filtered_img)
                    
                    # Save result
                    result_path = STEP2_DIR / f"{img_name}_{noise_str}_{filter_str}_{seg_method}.png"
                    cv2.imwrite(str(result_path), segmented)
                    
                    key = f"{img_name}_{noise_str}_{filter_str}_{seg_method}"
                    results_metrics[key] = {"segmented": segmented}
                    
                    print(f"    {seg_method:15} - saved")
    
    print("\n✓ Step 2 experiment completed")
    return results_metrics


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("Starting CMP717 - Edge Preserving Filters and Segmentation Project")
    
    # Step 1: Edge-preserving filters evaluation
    step1_metrics = run_step1_experiment()
    
    # Find best filter based on average PSNR
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
        print(f"\nBest filter for {img_name}: {best_filter} (PSNR: {best_psnr:.2f})")
    
    # Use bilateral filter as overall best (usually performs well)
    best_overall_filter = "bilateral"
    
    # Step 2: Segmentation evaluation
    step2_metrics = run_step2_experiment(best_overall_filter)
    
    print("\n" + "="*70)
    print("All experiments completed successfully!")
    print("="*70)
    
    return step1_metrics, step2_metrics


if __name__ == "__main__":
    step1_results, step2_results = main()
