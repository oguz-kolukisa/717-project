CMP717 - Image Processing Project
================================

Simple demo evaluating edge-preserving filters and segmentation on medical images.

Files
- `main.py`: experiment entrypoint (runs step 1 and step 2).
- `images/`: sample input images (m_low.jpg, m_mid.jpg, m_high.jpg).
- `results/`: output images saved by experiments.

Quick start

Install dependencies and run:

```bash
python -m pip install -r requirements.txt
python main.py
```

Notes
- The code may require `opencv-contrib-python` for `cv2.ximgproc.guidedFilter`.
