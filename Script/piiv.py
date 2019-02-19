from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import screeninfo

width = 800
height = 600

def streamDistortion():
	camera = PiCamera()
	camera.resolution = (width, height)
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(width, height))

	screen = screeninfo.get_monitors()[0]

	distCoeff = np.zeros((4,1), np.float64)

	# TODO: add your coefficients here!
	k1 = -1.0e-5; # negative to remove barrel distortion
	k2 = 0.0;
	p1 = 0.0;
	p2 = 0.0;

	distCoeff[0,0] = k1;
	distCoeff[1,0] = k2;
	distCoeff[2,0] = p1;
	distCoeff[3,0] = p2;

	# assume unit matrix for camera
	cam = np.eye(3, dtype = np.float32)

	cam[0,2] = width / 4.0  # define center x
	cam[1,2] = height / 2.0 # define center y
	cam[0,0] = 10.0        # define focal length x
	cam[1,1] = 10.0        # define focal length y

	window_title = "frame"
	cv2.namedWindow(window_title, cv2.WND_PROP_FULLSCREEN)
	cv2.moveWindow(window_title, screen.x - 1, screen.y - 1)
	cv2.setWindowProperty(window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

	time.sleep(0.1)

	for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
		image = frame.array
		
		result = cv2.resize(image, (0, 0), None, 0.5, 1.0)

		dst = cv2.undistort(result, cam, distCoeff)
		result = dst
		horizontal_stack = np.hstack((result, result))

		cv2.imshow(window_title, horizontal_stack)
		key = cv2.waitKey(1) & 0xff

		rawCapture.truncate(0)

		if key == ord("q"):
			break
	cv2.destroyAllWindows()

streamDistortion()