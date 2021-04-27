import cv2
import numpy as np
import argparse
import os
from matplotlib import pyplot as plt
from math import sqrt

def get_parser():
    parser = argparse.ArgumentParser(description="Select video path")
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="path to image file",
    )
    return parser

def houghLinesOld(edges):
    minLineLength = 1
    maxLineGap = 100
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180,threshold =30,minLineLength=minLineLength,maxLineGap =maxLineGap)
    if lines is not None:
        L=len(lines)
        for line in lines:
            for x1,y1,x2,y2 in line:
                distance=sqrt((x2-x1)**2+(y2-y1)**2)
                if(x2==x1):
                    theta=0
                else:
                    theta=int(abs(y2-y1)/abs(x2-x1))
                print(theta)
                print(distance)
                #if(theta>=0 and theta<5):
                    #print("asd")
                if(distance>0 and distance<450):
                    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)
                else:
                    L-=1
                #cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)
        print(L)
    else:
        print("Not Found!")

def houghLines(edges):
    minLineLength = 1
    maxLineGap = 100
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180,threshold =30,minLineLength=minLineLength,maxLineGap =maxLineGap)
    if lines is not None:
        print(len(lines))
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)
                distance=sqrt((x2-x1)**2+(y2-y1)**2)
                if((x2-x1)==0):
                    theta=-1
                else:
                    theta=int(abs(y2-y1)/abs(x2-x1))
                print("\nDistance: {}     Theta: {}".format(distance,theta))
                print("\nPoints==> X1: {} and X2: {}, Y1: {} and Y2: {}".format(x1,x2,y1,y2))

    else:
        print("Not Found!")


if __name__=='__main__':
    os.chdir("template")
    img=cv2.imread("template5.jpg")
    cv2.imshow('image',img)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,600,700,apertureSize = 5)
    #edges = cv2.GaussianBlur(edges,(3,3),0)

    houghLines(edges)
    
    cv2.imshow('edges',edges)
    cv2.imshow('out',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

