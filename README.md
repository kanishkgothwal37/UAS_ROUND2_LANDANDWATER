# UAS-DTU Round 2 Task (SEM 2) — Land/Water Segmentation + Camp Detection

This project performs:
✅ Land vs Water segmentation (overlay visualization)  
✅ Detection of 3 Rescue Camps (Pink, Blue, Grey) using circle detection

The output images are saved into an `output/` folder.

---

## 📌 Features

### 1) Land / Water Segmentation
- Converts image from **BGR → HSV**
- Uses HSV thresholding to create a **water mask**
- Applies morphological operations:
  - **Opening** → removes noise
  - **Closing** → fills small gaps
- Generates overlay:
  - **Water = Blue**
  - **Land = Green**
- Saves output as:  
  `output/seg_<image_name>.png`

### 2) Rescue Camp Detection (3 Camps)
- Converts image to grayscale + median blur
- Uses **Hough Circle Transform** to detect circular pads
- Classifies camp type using BGR pixel value at circle center:
  - **Pink camp**
  - **Blue camp**
  - **Grey camp**
- Draws detected circles + labels and saves:
  `output/camps_<image_name>.png`

---

## 📁 Folder Structure

