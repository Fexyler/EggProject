from __future__ import division
import cv2
import numpy as np
import imutils
from datetime import datetime

def banner():
    print("""


 _______  _______  _______  _______  _______           _       _________ _______  _______ 
(  ____ \(  ____ \(  ____ \(  ____ \(  ___  )|\     /|( (    /|\__   __/(  ____ \(  ____ )
| (    \/| (    \/| (    \/| (    \/| (   ) || )   ( ||  \  ( |   ) (   | (    \/| (    )|
| (__    | |      | |      | |      | |   | || |   | ||   \ | |   | |   | (__    | (____)|
|  __)   | | ____ | | ____ | |      | |   | || |   | || (\ \) |   | |   |  __)   |     __)
| (      | | \_  )| | \_  )| |      | |   | || |   | || | \   |   | |   | (      | (\ (   
| (____/\| (___) || (___) || (____/\| (___) || (___) || )  \  |   | |   | (____/\| ) \ \__
(_______/(_______)(_______)(_______/(_______)(_______)|/    )_)   )_(   (_______/|/   \__/


Coder : Batuhan \"Fexyler\" Isildak
Email : batuhanisildak@sabanciuniv.edu

This program counts eggs and writes the counter value in a xml file.

For questions, send an e-mail to me.
    """)

def capturer(param):
    cap      = cv2.VideoCapture(param)
    return cap

def lookat(cap, xwidth, xheight):
    _, frame = cap.read()
    frame    = imutils.resize(frame, width = xwidth, height = xheight)
    #framex = frame[160:xwidth, xwidth/2:xwidth/2+100]

    return frame
def getframe(resized):
    hsv       = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    v_channel = hsv[:, :, 2]
    v_channel = cv2.GaussianBlur(v_channel, (11, 11), 0)

    return v_channel, resized

def thresholder(frame, minval):
    bw, th = cv2.threshold(frame, minval, 255, cv2.THRESH_BINARY)

    return th
def morph(value, frame):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (value, value))
    morph  = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

    return morph
def distmaker(frame):
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    #morph = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
    dist = cv2.distanceTransform(frame, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)

    return dist
def templatemaker(bordersize, gap):
    #distborder = cv2.copyMakeBorder(dist, bordersize, bordersize, bordersize, bordersize,cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, 0)

    kernelx  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * (bordersize - gap) + 1, 3 * (bordersize - gap) + 3))

    kernel2  = cv2.copyMakeBorder(kernelx, gap, gap, gap, gap, cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, 2)

    template = cv2.distanceTransform(kernel2, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)

    return template
def templatematcher(distborder, template, scd_thresh):
    #matching = "cv2." + matching
    match        = cv2.matchTemplate(distborder, template, cv2.TM_CCORR_NORMED) # (cv2.TM_CCORR_NORMED) # cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, (cv2.TM_CCORR), cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED
    mn, mx, _, _ = cv2.minMaxLoc(match)
    b            = scd_thresh / 100
    yh, peaks    = cv2.threshold(match, mx *b , 255, cv2.THRESH_BINARY)
    morphedpeaks = morph(5, peaks)


    return morphedpeaks
def scaleconverter(peaks):
    peaksxu = cv2.convertScaleAbs(peaks)

    return peaksxu
def contourfinder(imaj):
    contours = cv2.findContours(imaj, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[1]


    return contours



def CheckEntranceLineCrossing(dist, y, CoorYEntranceLine, CoorYExitLine):
    AbsDistance = abs(y - CoorYEntranceLine)

    if ((AbsDistance <= dist) and (y < CoorYExitLine)):
        return 1
    else:
        return 0

def get_frame(normalframe):
    ret, jpeg             = cv2.imencode('.jpg', normalframe)
    return jpeg.tobytes()
def main(cap, fst_thresh, morph_value, scd_thresh, gap, bordersize, distx, display): #fst_thresh, morph_value, scd_thresh, matching, gap, bordersize,  distx):
    banner()
    now                   = datetime.now()
    year, month, day, hour, minute, second = now.year, now.month, now.day, now.hour, now.minute, now.second
    list                  = [year, month, day, hour, minute, second]
    #start = timeit.timeit()
    cap                   = capturer(cap)
    fps                   = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    EntranceCounter       = 0
    ExitCounter           = 0
    x                     = 0
    OffsetRefLines        = 100
    while True:
        _, frame          = cap.read()
        height            = np.size(frame, 0)
        width             = np.size(frame, 1)
        frame             = cv2.transpose(frame, -1)

        v_cha, normalframe= getframe(frame)


        th                = thresholder(v_cha, fst_thresh)
        morphed           = morph(morph_value, th)

        dist              = distmaker(morphed)

        distborder        = cv2.copyMakeBorder(dist, bordersize, bordersize, bordersize, bordersize,cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, 0)

        template          = templatemaker(bordersize, gap)

        morphedpeaks      = templatematcher(distborder, template, scd_thresh)

        peaksxu           = scaleconverter(morphedpeaks)
        CoorYEntranceLine = int((height / 2) + 200)
        CoorYExitLine     = int((height / 2) + 300)
        cv2.line(frame, (0, CoorYEntranceLine), (width, CoorYEntranceLine), (255, 0, 0), 2)

        contours = contourfinder(peaksxu)
        for i in range(len(contours)):
            x, y, w, h      = cv2.boundingRect(contours[i])
            _, mx, _, mxloc = cv2.minMaxLoc(dist[y:y + h, x:x + w], peaksxu[y:y + h, x:x + w])
            cv2.circle(frame, (int(mxloc[0] + x), int(mxloc[1] + y)), int(mx), (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.drawContours(frame, contours, i, (0, 0, 255), 2)
            CoordXCentroid = (x + x + w) / 2
            CoordYCentroid = (y + y + h) / 2
            ObjectCentroid = (CoordXCentroid, CoordYCentroid)
            if (CheckEntranceLineCrossing(distx, CoordYCentroid, CoorYEntranceLine, CoorYExitLine)):
                EntranceCounter += 1

            #if (CheckExitLineCrossing(CoordYCentroid, CoorYEntranceLine, CoorYExitLine)):
                #ExitCounter += 1

        cv2.putText(normalframe, "Entrances: {}".format(str(EntranceCounter)), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 1), 2)
        cv2.putText(normalframe, "Exits: {}".format(str(ExitCounter)), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if display:
            cv2.imshow("Display", normalframe)
        #cv2.imshow("threshed", morphedpeaks)

        if cv2.waitKey(5) == ord("q"):
            break



    cap.release()
    cv2.destroyAllWindows()
    now2 = datetime.now()
    year2, month2, day2, hour2, minute2, second2 = now2.year, now2.month, now2.day, now2.hour, now2.minute, now2.second
    list2 = [year2, month2, day2, hour2, minute2, second2]
    end = timeit.timeit()
    return EntranceCounter, ExitCounter, list, list2
