import numpy as np
import cv2


# Capturing video through webcam
webcam = cv2.VideoCapture(0)

# Start a while loop
while(1):
	
	# Reading the video from the
	# webcam in image frames
	_, imageFrame = webcam.read()

	# Convert the imageFrame in
	# BGR(RGB color space) to
	# HSV(hue-saturation-value)
	# color space
	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

	# Set range for red color and
	# define mask
	red_lower = np.array([136, 87, 111], np.uint8)
	red_upper = np.array([180, 255, 255], np.uint8)
	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

	# Set range for blue color and
	# define mask
	blue_lower = np.array([54, 80, 2], np.uint8)
	blue_upper = np.array([120, 255, 255], np.uint8)
	blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

	# Set range for black color and
	# define mask
	black_lower = np.array([0, 0, 0], np.uint8)
	black_upper = np.array([90, 90, 90], np.uint8)
	black_mask = cv2.inRange(hsvFrame, black_lower, black_upper)
	
	# Morphological Transform, Dilation
	# for each color and bitwise_and operator
	# between imageFrame and mask determines
	# to detect only that particular color
	kernel = np.ones((5, 5), "uint8")
	
	# For red color
	red_mask = cv2.dilate(red_mask, kernel)
	res_red = cv2.bitwise_and(imageFrame, imageFrame,
							mask = red_mask)

	# For blue color
	blue_mask = cv2.dilate(blue_mask, kernel)
	res_blue = cv2.bitwise_and(imageFrame, imageFrame,
							mask = blue_mask)
	# For black color
	black_mask = cv2.dilate(black_mask, kernel)
	res_black = cv2.bitwise_and(imageFrame, imageFrame,
							mask = black_mask)

	# Creating contour to track red color
	contours, hierarchy = cv2.findContours(red_mask,
									        cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(219, 0, 219), 2)
			
			cv2.putText(imageFrame, "Pink Color", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 1.0,
						(219, 0, 219))	

	# Creating contour to track blue color
	contours, hierarchy = cv2.findContours(blue_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(255, 0, 0), 2)
			
			cv2.putText(imageFrame, "Blue Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX,
						1.0, (255, 0, 0))
	# Creating contour to track black color
	contours, hierarchy = cv2.findContours(black_mask,
									        cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(0, 0, 0), 2)
			
			cv2.putText(imageFrame, "Black Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 1.0,
						(0, 0, 0))	

			
	# Program Termination
	cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyAllWindows()
		break
