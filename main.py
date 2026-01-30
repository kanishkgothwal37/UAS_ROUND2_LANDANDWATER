import cv2
import numpy as np
import os

input_folder = "images"
output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(input_folder):

    if file_name.endswith(".png") or file_name.endswith(".jpg") or file_name.endswith(".jpeg"):

        img_path = os.path.join(input_folder, file_name)
        img = cv2.imread(img_path)

        if img is None:
            print("Could not read:", img_path)
            continue

        img = cv2.resize(img, (600, 600))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([140, 255, 255])

        water_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        land_mask = cv2.bitwise_not(water_mask)

        overlay = img.copy()

        overlay[water_mask > 0] = (255, 0, 0)
        overlay[land_mask > 0] = (0, 255, 0)

        final = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)

        out_path = os.path.join(output_folder, "seg_" + file_name)
        cv2.imwrite(out_path, final)

        print("Saved:", out_path)

print(" Check output folder.")