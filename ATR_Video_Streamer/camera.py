import cv2

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        self.video.set(cv.CAP_PROP_FRAME_WIDTH,256);
        self.video.set(cv.CAP_PROP_FRAME_HEIGHT,144);
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
	image = cv2.circle(image, (320,240), 20, (0,0,255), -1)
	#font = cv2.FONT_HERSHEY_SIMPLEX
	#image = cv2.putText(image,'Kent State University', (10,40),font, 1, (255,255,255), 2, cv2.LINE_AA)
	#image = cv2.putText(image,'Software Development for Robotics', (10,100),font, 1, (255,255,255), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', image)
	#jpeg = cv2.line(jpeg, (100,0), 63, (0,0,255), -1)
        return jpeg.tobytes()
