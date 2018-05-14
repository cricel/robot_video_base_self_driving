import video
import sys
import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError

MIN_MATCH_COUNT=10



detector=cv2.xfeatures2d.SIFT_create()

FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

trainImg_stop=cv2.imread("train_image/stop_sign_template_small_01.png",0)
trainKP_stop,trainDesc_stop=detector.detectAndCompute(trainImg_stop,None)

trainImg_limit5=cv2.imread("train_image/sign_speed-5.jpg",0)
trainKP_limit5,trainDesc_limit5=detector.detectAndCompute(trainImg_limit5,None)

trainImg_limit50=cv2.imread("train_image/sign_speed-50.jpg",0)
trainKP_limit50,trainDesc_limit50=detector.detectAndCompute(trainImg_limit50,None)

start = time.time()
cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,256);
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,144);

def findline(img, linenum):
    temp = img[linenum]
    #print(len(temp))
    i = 0
    j = 0
    isObejct = 0
    #count = 0
    for pixle in temp:
        if pixle == 255:
            break
        else:
            i += 1

    for pixle in reversed(temp):
        if pixle == 255:
            break
        else:
            j += 1

    #print("i: {}, j: {}".format(i, j))
    if ((i + j) > 140 and (i + j) < 256):
        isObejct = 0
        return i , j , isObejct
    else:
        isObejct = 1
        return i , j, isObejct

while True:
    shapes = 0
    red = 0
    ret, QueryImgBGR=cam.read()
    QueryImg=cv2.cvtColor(QueryImgBGR,cv2.COLOR_BGR2GRAY)

    queryKP,queryDesc=detector.detectAndCompute(QueryImg,None)

    matches_stop=flann.knnMatch(queryDesc,trainDesc_stop,k=2)

    matches_limit5=flann.knnMatch(queryDesc,trainDesc_limit5,k=2)

    matches_limit50=flann.knnMatch(queryDesc,trainDesc_limit50,k=2)

    end = time.time()
    sub = end - start

    if ( sub > 3 and sub < 5):
        pass
    else:
        goodMatch_stop=[]
        for m,n in matches_stop:
            if(m.distance<0.55*n.distance):
                goodMatch_stop.append(m)
        if(len(goodMatch_stop)>MIN_MATCH_COUNT):
            #client_socket.send("found a stop sign")
            print ("find a stop sign")
            start = time.time()
            for i in range(0, 3):
                print("we wait for: {} seconds".format(i))
                time.sleep(1)
            stopsign_go = 1
            #print ("start: {}".format(start))
            continue

    goodMatch_limit5=[]
    for m,n in matches_limit5:
        if(m.distance<0.45*n.distance):
            goodMatch_limit5.append(m)
    if(len(goodMatch_limit5)>MIN_MATCH_COUNT):
        print ("found a 5 speed limit")

    goodMatch_limit50=[]
    for m,n in matches_limit50:
        if(m.distance<0.45*n.distance):
            goodMatch_limit50.append(m)
    if(len(goodMatch_limit50)>MIN_MATCH_COUNT):
        print ("found a 55 speed limit")

    gray = cv2.medianBlur(QueryImg, 5)
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8, param1=100, param2=30, minRadius=1, maxRadius=30)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            shapes = shapes + 1

    color = cv2.cvtColor(QueryImgBGR, cv2.COLOR_BGR2HSV)
    lower_range = np.array([169, 100, 100], dtype=np.uint8)
    upper_range = np.array([189, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(color, lower_range, upper_range)
    if (mask.any()):
        red = 1

    if (shapes == 3 and red == 1):
        print("red traffic sign: stop!!")
        continue

    edge = cv2.Canny(QueryImg, 1500, 1500, apertureSize=5)

    vis = QueryImgBGR.copy()
    vis = np.uint8(vis/2.)
    vis[edge != 0] = (0, 255, 0)

    line1_i, line1_j, line1_obj = findline(edge, 40)
    line2_i, line2_j, line2_obj = findline(edge, 100)

    if (line1_obj == 0 and line2_obj == 0):
        if (int(line2_i) - int(line1_i) <10 and  int(line2_i) - int(line1_i) > 0):
            print ("go forward")
        elif (int(line1_i) - int(line2_i) <10 and  int(line1_i) - int(line2_i) > 0):
            print ("go forward")
        elif line1_i > line2_i:
            print ("turn right")
        elif line2_i > line1_i:    
            print ("turn left")
    if (line1_obj == 1 or line2_obj == 1):
        if(line1_i > line1_j or line2_i > line2_j):
            if (int(line2_i) - int(line1_i) <10 and  int(line2_i) - int(line1_i) > 0):
                print ("go forward")
            elif (int(line1_i) - int(line2_i) <10 and  int(line1_i) - int(line2_i) > 0):
                print ("go forward")
            elif line1_i > line2_i:
                print ("turn right")
            elif line2_i > line1_i:    
                print ("turn left")
        if(line1_i < line1_j or line2_i < line2_j):
            if (int(line2_j) - int(line1_j) <10 and  int(line2_j) - int(line1_j) > 0):
                print ("go forward")
            elif (int(line1_j) - int(line2_j) <10 and  int(line1_j) - int(line2_j) > 0):
                print ("go forward")
            elif line1_j < line2_j:
                print ("turn right")
            elif line2_j < line1_j:    
                print ("turn left")

    cv2.imshow('cam',QueryImgBGR)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

#def detectorsss():
