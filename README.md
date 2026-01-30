# UAS-DTU Round 2 Task (SEM 2)

## ✅ Part Completed: Land vs Water Segmentation
This project detects and separates **Land** and **Water** regions from input images using basic OpenCV.

### Approach (Beginner Friendly)
1. Read the image using OpenCV
2. Convert BGR to HSV
3. Detect water using blue HSV range (mask)
4. Land mask = inverse of water mask
5. Overlay colors and save output image

### Output Colors
- **Land = Green**
- **Water = Blue**

