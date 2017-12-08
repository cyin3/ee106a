#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from matplotlib import pyplot as plt
from geometry_msgs.msg import Twist

pub = None
vel_pub = None
x_c = 'nan'
y_c = 'nan'
last_cmd_time = 'nan'
last_depth = float('nan')
depth_mat = None
def camera_data_parsing(message):
	global pub, x, y
	#print(message)
	cv_image = bridge.imgmsg_to_cv2(message, "rgb8")
	#print(cv_image) 
	#print(np.array(message.data, dtype=np.uint8))
	center = find_target_center(np.array(cv_image))
	#print(center)
	#pub.publish(center)
	#print(message)

def camera_depth_parsing(message):
	global x_c, y_c, depth_mat
	cv_image = bridge.imgmsg_to_cv2(message, "32FC1")
	depth_matrix = np.array(cv_image)
	depth_mat = depth_matrix
	# to access point in depth_matrix, depth_matrix[y_c][x_c]
	# print('Center_x : %d, Center_y : %d, Center_z: %f', x_c, y_c, depth_matrix[y_c][x_c])
	#if x_c == 'nan' or y_c == 'nan':
	#	pub.publish("nan nan nan")
	#else:
	#	pub.publish(str(x_c)+" "+str(y_c)+" "+str(depth_matrix[y_c][x_c]))
		#publish_speed(x_c, depth_matrix[y_c][x_c])

def publish_speed(message):
	x_pos, y_pos, depth_pos = message.data.split()
        depth_pos = float(depth_pos)
        x_pos = float(x_pos)
        y_pos = float(y_pos)
        global vel_pub, last_cmd_time, last_depth, angErrorPrev
        max_z = 3
        min_z = 0.1
        desired_z = 0.75
        pGain = 1
        tol_z = 0.03125
        blinder = 0.5
        maxSpeed = 0.4
        tol_ang = 0.05
        pGainRot = 1.0
        speed = Twist()
        angError = "nan"
        angErrorDerivative = "nan"
        Kd = 0
        h = 1/6.7

        if (np.isnan(last_depth)):
                last_depth = depth_pos
        diff_from_last_depth = last_depth - depth_pos
        if (diff_from_last_depth > 0.5):
                depth_pos = 0
        else:
                last_depth = depth_pos
        if (np.isnan(depth_pos) or np.isnan(x_pos) or depth_pos < min_z or depth_pos  > max_z):
                speed.linear.x = 0
                speed.linear.y = 0
                speed.angular.z = 0
        else:
                zError = depth_pos - desired_z
                speed_x = zError * pGain
                if (np.absolute(zError) < tol_z):
                        speed.linear.x = 0
                else:
                        speed.linear.x = speed_x
                if (np.absolute(speed.linear.x) > maxSpeed):
                        speed.linear.x = maxSpeed*np.sign(speed.linear.x)

                angError = (320 - x_pos)/640.0
                #angError = -np.arctan2(x_pos, y_pos)
                if (np.absolute(angError) < tol_ang):
                        speed.angular.z = 0
                else:
                        #curr_time = rospy.get_time()
                        #if (curr_time - last_cmd_time > 0):
                        speed.angular.z = angError*pGainRot
                                #last_cmd_time = curr_time
                        #else:
                                #speed.angular.z = 0
                #print("xError: %f angError: %f speed: %f rot: %f", zError, angError, speed.linear.x, speed.angular$
                if (x_pos < 350 and x_pos > 290):
                        #speed.angular.z = 0
                        pass
                elif(x_pos > 320):
                        pass
                        #speed.angular.z = -0.3
                else:
                        pass
                        #speed.angular.z = 0.3
        #print("x_pos: "+str(x_pos)+", z_pos: "+str(depth_pos))
        #print("ang_error", angError)

        curr_time = rospy.get_time()
        time_diff = curr_time - last_cmd_time
        #if time_diff > .6 and time_diff < 1.2:
                #speed.angular.z = 0 
        #else:
        print("x_pos: "+str(x_pos)+" angSpeed:"+str(speed.angular.z)+"depth: "+str(depth_pos)+" linear_speed: "+str(speed.linear.x))
        #speed.linear.x = 0
        #speed.angular.z = 0

        last_cmd_time = rospy.get_time()
        vel_pub.publish(speed)

def listener():
	rospy.init_node('get_target_center', anonymous=True)
	global pub, vel_pub, last_cmd_time
	last_cmd_time = 0
	pub = rospy.Publisher('target_midpoint', String, queue_size=10)
	vel_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
	rospy.Subscriber('/camera/rgb/image_color', Image, camera_data_parsing )
	rospy.Subscriber('/camera/depth_registered/image', Image, camera_depth_parsing)
	rospy.Subscriber('/target_midpoint', String, publish_speed)
	rospy.spin()

# convert from np image to img cv and back
def conv_img(img):
	return img[:,:,[2,1,0]]

def find_target_center(image_data):
    global x_c, y_c, face_cascade, depth_mat
    if depth_mat is None:
        pub.publish("nan nan nan")
        return "nan" 
    depth_local = depth_mat.copy()
    img_cv = conv_img(np.uint8(image_data))
    frame = img_cv
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
       gray,
       scaleFactor=1.1,
       minNeighbors=5,
       minSize=(30, 30),
       flags = cv2.CASCADE_SCALE_IMAGE #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    if len(faces) == 0:
        x_c = "nan"
        y_c = "nan"
        pub.publish("nan nan nan")
        return "nan nan"
    print("Num faces found: ", len(faces))

    max_face_area = -1
    max_face_centroid = None
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        #print("W H", w * h)
        #print((x + w/2.0, y + h/2.0))
        if w * h > max_face_area:
            max_face_area = w * h
            max_face_centroid = (x + w/2.0, y + h/2.0)
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #plt.imshow(conv_img(frame))
    #plt.show()
    x_c = max_face_centroid[0]
    y_c = max_face_centroid[1]
    if x_c == 'nan' or y_c == 'nan':
        pub.publish("nan nan nan")
    else:
        pub.publish(str(x_c)+" "+str(y_c)+" "+str(depth_local[y_c][x_c]))
    return_val = str(max_face_centroid[0]) + " " + str(max_face_centroid[1])
    """
    #og_img_cv = img_cv.copy()
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
    #plt.imshow(thresh,cmap="gray")

    # find contours in the thresholded image
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contours = (np.array([cv2.contourArea(cnt) for cnt in contours]))
    max_cnt_idx = np.argmax(max_contours)
    max_cnt = contours[max_cnt_idx]
    # max_cnt_cvHull = cv2.convexHull(max_cnt)

    #img_cv_copy = og_img_cv.copy()
    if cv2.contourArea(max_cnt) < 5000:
        x_c = "nan"
        return "nan"

    peri = cv2.arcLength(max_cnt, True)
    
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
            delta -= 1
            delta /= 1.02
            delta += 1
        elif len(approx) < 4:
            eps /= delta
            approx = cv2.approxPolyDP(max_cnt, eps * peri, True)
            delta -= 1
            delta /= 1.02
            delta += 1
    #if len(approx) != 4:
    #    x_c = "nan"
    #    y_c = "nan"
	#print("len  approx != 4")
       # return "nan"
    center = np.int_(np.mean(approx, axis = 0))[0]
    x = center[0]
    y = center[1]
    x_c = x
    y_c = y
    #print("center", center)

	# plot the image and centroid
    #plt.imshow(conv_img(og_img_cv))
    #plt.scatter([x],[y])
    #plt.pause(.00000000000005)
    #plt.show()
    #plt.pause(.000000002)

    return_val = str(x) + " " + str(y)
    """
    return return_val

global bridge


if __name__ == '__main__':
	bridge = CvBridge()
	face_cascade = cv2.CascadeClassifier('/home/turtlebot/project_follower/haarcascade_frontalface_default.xml')
	try:
		listener()
	except rospy.ROSInterruptException: pass
	#plt.show()