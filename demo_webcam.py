import sys
import cv2
import os
import time
import importlib
from FaceDetectorThread import FaceDetectorThread

def drawBoxes(im, boxes, color):
    x1 = [i[0] for i in boxes]
    y1 = [i[1] for i in boxes]
    x2 = [i[2] for i in boxes]
    y2 = [i[3] for i in boxes]
    for i in range(len(boxes)):
        cv2.rectangle(im, (int(x1[i]), int(y1[i])), (int(x2[i]), int(y2[i])), color, 1)
    return im


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("This script receives a model folder and a list of images and detects faces using mtcnn")
        print("")
        print("Usage: ")
        print("python demo_webcam.py 'network_folder'")
        print("--------------------------------")

    else:

        # Init mtcnnMock
        network_folder = sys.argv[1]
        FaceDetector = getattr(importlib.import_module(network_folder + ".FaceDetector"), "FaceDetector")
        model_folder = network_folder + "/model"

        # Create Face Detector
        faceDetectorObject = FaceDetector(model_folder)
        faceDetectorThread = FaceDetectorThread(faceDetectorObject)
        faceDetectorThread.start()

        # Start webcam
        camera = cv2.VideoCapture(0)
        ret, image = camera.read()
        cv2.imshow('img', image)

        # init FPS calc
        start_time = time.time()
        processed_frames = 0

        while True:

            # Read frame from Webcam
            ret, image = camera.read()

            # Detect faces
            faceDetectorThread.set_image(image)

            if faceDetectorThread.rects_ready():

                # Get bounding boxes
                rects = faceDetectorThread.get_rects()

                # Draw bounding boxes
                drawBoxes(image, rects, (0, 0, 255))

                # FPS calc
                processed_frames += 1

            # Show image on screen
            cv2.imshow('img', image)

            # Check for exit button 'q'
            ch = cv2.waitKey(1) & 0xFF
            if ch == ord("q"):
                break

        faceDetectorThread.stop()
        faceDetectorThread.join()

        # FPS calc
        total_time = time.time() - start_time
        print("FPS: " + str(processed_frames / total_time))
