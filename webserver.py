import cv2
import eggcounterv1

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        normalframe, ntranceCounter, ExitCounter, hour, minute, second, hour2, minute2, second2 = eggcounterv1.main('myvideo.mp4')
        #self.video = cv2.VideoCapture(normalframe)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def get_frame(self):
        normalframe, ntranceCounter, ExitCounter, hour, minute, second, hour2, minute2, second2 = eggcounterv1.main(0)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', normalframe)
        return jpeg.tobytes()