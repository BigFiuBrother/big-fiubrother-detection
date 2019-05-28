import sys
import cv2
import os
import time
import importlib
import shutil


def drawBoxes(im, boxes):

    for i in range(boxesAmount(boxes)):
        box = boxes[i]
        x1 = box[0]
        y1 = box[1]
        x2 = box[2]
        y2 = box[3]
        cv2.rectangle(im, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
    return im

def boxesAmount(boxes):
    return len(boxes)

def boxesCSVLines(img_path, boxes):

    lines = img_path + "\n"
    bbAmount = boxesAmount(boxes)
    lines += str(bbAmount) + "\n"

    for i in range(bbAmount):
        box = boxes[i]
        x1 = box[0]
        y1 = box[1]
        x2 = box[2]
        y2 = box[3]
        lines += str(int(x1)) + "," + str(int(y1)) + "," + str(int(x2) - int(x1)) + "," + str(int(y2) - int(y1)) + "\n"
    return lines

if __name__ == "__main__":

    if len(sys.argv) < 3:

        print("--------------------------------")
        print("This script receives a model folder and a list of images and detects faces using mtcnn")
        print("")
        print("Usage: ")
        print("python demo_files.py 'network_folder' 'image_path1' 'image_path2' ... ")
        print("--------------------------------")

    else:

        #minsize = 20
        #threshold = [0.6, 0.7, 0.7]
        #factor = 0.709

        # Init mtcnnMock
        network_folder = sys.argv[1]
        FaceDetector = getattr(importlib.import_module(network_folder + ".FaceDetector"), "FaceDetector")
        model_folder = network_folder + "/model"

        # Get output folder
        if not os.path.exists("output"):
            os.mkdir("output")
        output_folder = "output/" + network_folder
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        # Create Face Detector
        faceDetectorObject = FaceDetector(model_folder)

        # Get Images
        image_paths = sys.argv[2:]
        print("Length: " + str(len(image_paths)))

        start_time = time.time()
        # Detect Bounding Boxes
        total_boxes = []
        for i in range(len(image_paths)):
            if i % 100 == 0:
                print(i)
            # Detect face bounding boxes
            image_path = image_paths[i]
            boundingboxes = faceDetectorObject.detect_face(image_path)
            total_boxes.append(boundingboxes)
        elapsed_time = time.time() - start_time
        print("Total images: " + str(len(image_paths)) + ", Elapsed time: " + str(elapsed_time))

        # Close Face Detector
        faceDetectorObject.close()

        # Save Bounding Boxes to file
        output_csv = open(output_folder + "/bounding_boxes.txt", "w")
        for i in range(len(image_paths)):
            image_path = image_paths[i]
            boundingboxes = total_boxes[i]

            # Show on screen
            #img = cv2.imread(image_path)
            #img = drawBoxes(img, boundingboxes)
            #cv2.imshow('img', img)
            #ch = cv2.waitKey(0) & 0xFF
            #if ch == ord("q"):
            #    break

            # Save bounding boxes to csv file in output folder
            filename = os.path.basename(image_path)
            line = boxesCSVLines(filename, boundingboxes)
            output_csv.write(line)
        output_csv.close()

        # Save cropped faces to folder

        faces_folder = "output/" + network_folder + "/faces"
        if os.path.exists(faces_folder):
            shutil.rmtree(faces_folder)
        os.mkdir(faces_folder)
        for i in range(len(image_paths)):

            image_path = image_paths[i]
            img = cv2.imread(image_path)

            filename = faces_folder + "/" + os.path.basename(image_path)

            boundingboxes = total_boxes[i]
            for i in range(len(boundingboxes)):
                box = boundingboxes[i]
                x1 = int(box[0])
                y1 = int(box[1])
                x2 = int(box[2])
                y2 = int(box[3])

                face = img[y1:y2, x1:x2].copy()
                try:
                    face = cv2.resize(face, (160, 160), interpolation=cv2.INTER_CUBIC)
                    cv2.imwrite(filename, face)
                except:
                    print("Bad box on:", image_path, ", box number:", i, ", box:", box)

