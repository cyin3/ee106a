import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import re
import json
from scipy import ndimage
import itertools

filename = "/home/girish/Documents/data/ee106a/red_folder_debug.txt"
textfile = open(filename, 'r')
filetext = textfile.read()
textfile.close()

print("Length of file: ")
print(len(filetext))

matches = re.findall("data\: \[[^\]]+\]", filetext)


str_arrays = [i[6:] for i in matches]

print("Number of frames: ")
print(len(str_arrays))

int_arrays = [np.array(json.loads(i)) for i in str_arrays]

def conv_img(img):
    return img[:,:,[2,1,0]]

def find_target_center(image_data):
    img_cv = np.uint8(image_data.reshape((480,640,3)))
    og_img_cv = img_cv.copy()
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)


    # first mask
    lower_red_0 = np.array([0,128,0])
    upper_red_0 = np.array([10,255,255])
    mask_0 = cv2.inRange(hsv, lower_red_0, upper_red_0)

    # second mask
    lower_red_1 = np.array([160,128,0])
    upper_red_1 = np.array([180,255,255])
    mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)

    mask = cv2.bitwise_or(mask_0, mask_1)

    res = cv2.bitwise_or(img_cv,img_cv, mask= mask)
    blurred = cv2.GaussianBlur(mask, (11, 11), 0)
    thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]
    #plt.imshow(thresh, cmap="gray")

    # find contours in the thresholded image
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contours = (np.array([cv2.contourArea(cnt) for cnt in contours]))
    max_cnt_idx = np.argmax(max_contours)
    max_cnt = contours[max_cnt_idx]
    # max_cnt_cvHull = cv2.convexHull(max_cnt)

    #img_cv_copy = og_img_cv.copy()
    peri = cv2.arcLength(max_cnt, True)

    if cv2.contourArea(max_cnt) < 10000:
        plt.imshow(conv_img(og_img_cv))
        plt.show()
        return "NaN"

    eps = .08
    approx = cv2.approxPolyDP(max_cnt, eps * peri, True)


    # setting the approx length to 4
    delta = 10
    for _ in range(500):
        if len(approx) == 4:
            break
        elif len(approx) > 4:
            eps *= delta
            approx = cv2.approxPolyDP(max_cnt, eps * peri, True)
            delta /= 1.1
        elif len(approx) < 4:
            eps /= delta
            approx = cv2.approxPolyDP(max_cnt, eps * peri, True)
            delta /= 1.1

    x,y = np.int_(np.mean(approx, axis = 0))[0]

    #print("AAJHH")
    #x,y = find_target_center(image_data)
    #plt.imshow(conv_img(og_img_cv))
    #plt.scatter([x],[y])
    #plt.show()

    #return str(x) + " " + str(y)
    return (x,y)

for i in int_arrays:
    image_data = i
    img_cv = np.uint8(image_data.reshape((480,640,3)))
    plt.imshow(conv_img(img_cv))
    x, y = (find_target_center(image_data))
    plt.scatter([x],[y])
    print((x,y))
    plt.pause(.05)
