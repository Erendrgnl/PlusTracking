import cv2
import numpy as np
import argparse
import os
# from matplotlib import pyplot as plt
from math import sqrt

#---------------------------------------------------------------------------
#GLOBAL FUNCTIONS   --------------------------------------------------------
#---------------------------------------------------------------------------

def get_parser():
    parser = argparse.ArgumentParser(description="Select video path")
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="path to image file",
    )
    return parser

#---------------------------------------------------------------------------
#CLASS TO IMAGE PROCESS ----------------------------------------------------
#---------------------------------------------------------------------------

class PlusTracking():
    def __init__(self):
        self.houghParameters={"minLineLength":1,"maxLineGap":100,"threshold":30,"theta":np.pi/180,"rho":1}
        self.cannyParameters={"apertureSize":5,"threshold1":600,"threshold2":700}
        self.verticalLines=[]
        self.horizontalLines=[]
        self.img=None

    def getHoughLines(self,img):
        self.img=img
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,self.cannyParameters["threshold1"],self.cannyParameters["threshold2"],apertureSize=self.cannyParameters["apertureSize"])

        lines = cv2.HoughLinesP(edges,
            rho=self.houghParameters["rho"],
            theta=self.houghParameters["theta"],
            threshold =self.houghParameters["threshold"],
            minLineLength=self.houghParameters["minLineLength"],
            maxLineGap=self.houghParameters["maxLineGap"])
        return lines

    def lineMarker(self,line,visualize=False):
        for x1,y1,x2,y2 in line:
            if(visualize):
                cv2.line(self.img,(x1,y1),(x2,y2),(0,0,255),1)
            verticalDistance=abs(x2-x1)
            horizontalDistance=abs(y2-y1)
            #print("\nPoints==> X1: {} and X2: {}, Y1: {} and Y2: {}".format(x1,x2,y1,y2))
            #print("verticalDistance: {}".format(verticalDistance))
            #print("horizontalDistance: {}".format(horizontalDistance))
            if(verticalDistance<horizontalDistance):
                #self.verticalLines.append([x1, x2])
                self.verticalLines.append(min([x1, x2]))
            elif(horizontalDistance<verticalDistance):
                #self.horizontalLines.append([y1, y2])
                self.horizontalLines.append(min([y1, y2]))

    def deviationRate(self):
        HDR=max(self.horizontalLines)-min(self.horizontalLines)
        VDR=max(self.verticalLines)-min(self.verticalLines)
        Rate=sqrt(HDR**2+VDR**2)
        print("Number of deviations in horizontal pixels: {}".format(HDR))
        print("Number of deviations in vertical pixels: {}".format(VDR))
        print("number of deviations in both axis : {}".format(Rate))

    def clearFrame(self):
        self.verticalLines=[]
        self.horizontalLines=[]
        self.img=None


    def main(self,img,visualize=False):
        lines=self.getHoughLines(img)
        if lines is not None:
            for line in lines:
                self.lineMarker(line,visualize=visualize)
            self.deviationRate()
        if(visualize):
            cv2.imshow('out',self.img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        self.clearFrame()


if __name__=='__main__':
    p=PlusTracking()
    args = get_parser().parse_args()
    for filename in os.listdir(args.file):
        path=args.file+"\\"+filename
        print("\n"+path)
        img = cv2.imread(path)
        p.main(img,visualize=True)
