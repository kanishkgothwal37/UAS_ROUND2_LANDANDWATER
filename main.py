import cv2 
import numpy as np
import os

input_folder = "images"
output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def classify_camp_from_bgr(bgr):
    b, g, r = int(bgr[0]), int(bgr[1]), int(bgr[2])

    if abs(r - g) < 30 and abs(g - b) < 30 and r > 160:
        return "grey"

    if b > 150 and g > 100 and r < 150:
        return "blue"

    if r > 150 and b > 120 and g < 170:
        return "pink"

    return "unknown"

for file_name in os.listdir(input_folder):

    if file_name.endswith((".png", ".jpg", ".jpeg")):

        img_path = os.path.join(input_folder, file_name)
        img = cv2.imread(img_path)

        if img is None:
            print("Could not read:", img_path)
            continue

        img = cv2.resize(img, (600, 600))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_water = np.array([90, 20, 20])
        upper_water = np.array([140, 255, 160])

        water_mask = cv2.inRange(hsv, lower_water, upper_water)

        kernel = np.ones((5, 5), np.uint8)
        water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_OPEN, kernel)
        water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_CLOSE, kernel)

        land_mask = cv2.bitwise_not(water_mask)

        overlay = img.copy()
        overlay[water_mask > 0] = (255, 0, 0)   
        overlay[land_mask > 0] = (0, 255, 0)    

        final_seg = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)

        seg_path = os.path.join(output_folder, "seg_" + file_name)
        cv2.imwrite(seg_path, final_seg)
        print("✅ Saved segmentation:", seg_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)

        circles = cv2.HoughCircles(
            blur,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=120,
            param1=80,
            param2=30,
            minRadius=15,
            maxRadius=60
        )

        camps = {} 

        if circles is not None:
            circles = np.uint16(np.around(circles[0]))

            for (x, y, r) in circles:
                camp_type = classify_camp_from_bgr(img[y, x])

                if camp_type != "unknown" and camp_type not in camps:
                    camps[camp_type] = (x, y)

                    cv2.circle(img, (x, y), r, (0, 0, 255), 2)
                    cv2.circle(img, (x, y), 2, (255, 255, 255), 3)
                    cv2.putText(img, camp_type, (x - 30, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        print("✅ Camps detected in", file_name, "=>", camps)

        camp_out_path = os.path.join(output_folder, "camps_" + file_name)
        cv2.imwrite(camp_out_path, img)
        print("✅ Saved camps image:", camp_out_path)

print("\n✅ Done! Check output folder.")
