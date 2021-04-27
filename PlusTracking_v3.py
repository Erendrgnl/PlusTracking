import cv2
import numpy as np
import argparse
import os
from operator import itemgetter
import math


#---------------------------------------------------------------------------
#NOTES   -------------------------------------------------------------------
#---------------------------------------------------------------------------

#self.houghParameters={"minLineLength":1,"maxLineGap":100,"threshold":40,"theta":np.pi/180,"rho":1} #40
#self.cannyParameters={"apertureSize":5,"threshold1":600,"threshold2":700}
#CANNY ve HOUGH transformları parametre değerlerine göre uygulanıyor
#çizgiler yatay veya dikey olarak sınıflandırılıyor
#---------------------------------------------------------------------------
#GLOBAL FUNCTIONS   --------------------------------------------------------
#---------------------------------------------------------------------------

def getFile():
    for filename in os.listdir(args.file):
        path=args.file+"\\"+filename
        print("\n"+path)
        img = cv2.imread(path)
        p.main(img,visualize=False)


def get_parser():
    parser = argparse.ArgumentParser(description="Select image path")
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
        self.houghParameters={"minLineLength":1,"maxLineGap":100,"threshold":40,"theta":np.pi/180,"rho":1} #40
        self.cannyParameters={"apertureSize":5,"threshold1":600,"threshold2":700}
        self.verticalLines=[]
        self.horizontalLines=[]
        self.img=None
        self.out=None
        self.intersectionPoint=[]
        self.centerPoint=[]

    def getHoughLines(self,img):
        self.img=img
        h,w,_=img.shape
        self.out=np.zeros((h,w))
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,self.cannyParameters["threshold1"],self.cannyParameters["threshold2"],apertureSize=self.cannyParameters["apertureSize"])

        lines = cv2.HoughLinesP(edges,
            rho=self.houghParameters["rho"],
            theta=self.houghParameters["theta"],
            threshold =self.houghParameters["threshold"],
            minLineLength=self.houghParameters["minLineLength"],
            maxLineGap=self.houghParameters["maxLineGap"])
        #print(len(lines))
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
                self.horizontalLines.append([x1, x2, y1, y2])
            elif(horizontalDistance<verticalDistance):
                #self.horizontalLines.append([y1, y2])
                self.verticalLines.append([x1, x2, y1, y2])

    def LineToPoint(self,line,point,point_axis='x'):
        m=1
        if(line[1]-line[0]!=0):
            m=(abs(line[2]-line[3]))/(abs(line[1]-line[0]))
        if(point_axis=='x'):
            result_point=line[2]-(m*(point-line[0]))
            result_point=int(result_point)
        if(point_axis=='y'):
            result_point=(abs(point-line[2])/m)+line[0]
            result_point=int(result_point)
        return result_point

    def distance(self,point1,point2):
        d=math.sqrt((abs(point2[0]-point1[0]))**2+(abs(point2[1]-point1[1]))**2)
        return d

    def intersection(self):
        for verticalLine in self.verticalLines:
            for point in range(verticalLine[0],verticalLine[1]):
                for horizontalLine in self.horizontalLines:
                    if (point>=horizontalLine[0] and point<=horizontalLine[1]):
                        V_y=self.LineToPoint(verticalLine,point,point_axis='x')
                        H_y=self.LineToPoint(horizontalLine,point,point_axis='x')
                        d=self.distance((point,V_y),(point,H_y))
                        if(d<=10): #TH1
                            #self.out=image = cv2.circle(self.out, (point,V_y), 1, (255,255,255), thickness=-1)
                            self.intersectionPoint.append((point,V_y))

    def formatList(self):
        self.intersectionPoint = sorted(self.intersectionPoint, key=itemgetter(0))
        holder=self.intersectionPoint
        #print(holder)
        for i,pt in enumerate(holder):
            try:
                for inds in range(i,len(holder)-1):
                    d=self.distance(pt,holder[inds])
                    if(d<=3):
                        holder.remove(holder[inds])
            except:
                pass
            
        #print(holder)
        self.intersectionPoint=holder

    def findCenter(self):
        self.formatList()
        for pt in self.intersectionPoint:
            self.out=image = cv2.circle(self.out, (pt), 1, (255,255,255), thickness=-1)
            self.centerPoint.append(pt)
       
        if(len(self.centerPoint)==2):
            d=self.distance(self.centerPoint[0],self.centerPoint[1])
            V_d=abs(self.centerPoint[0][0]-self.centerPoint[1][0])
            H_d=abs(self.centerPoint[0][1]-self.centerPoint[1][1])
            print("Sapma miktari: {} piksel".format(d))
            print("Yatay kayma: {} piksel".format(V_d))
            print("Dikey kayma: {} piksel".format(H_d))
        elif(len(self.centerPoint)==1):
            print("Sapma yok!")
        elif(len(self.centerPoint)==0):
            print("merkez bulunamadı")
        else:
            print("Birden fazla sapma var")
            for pt in self.centerPoint:
                if(pt==self.centerPoint[0]):
                    continue
                d=self.distance(self.centerPoint[0],pt)
                print("Sapma miktari: {} piksel".format(d))
        

    def clearFrame(self):
        self.verticalLines=[]
        self.horizontalLines=[]
        self.img=None
        self.out=None
        self.intersectionPoint=[]
        self.centerPoint=[]


    def main(self,img,visualize=False):
        lines=self.getHoughLines(img)
        if lines is not None:
            for line in lines:
                self.lineMarker(line,visualize=visualize)
            self.intersection()
            self.formatList()
            self.findCenter()
            
        if(visualize):
            cv2.imshow('out',self.img)
            cv2.imshow('out2',self.out)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        self.clearFrame()


if __name__=='__main__':
    p=PlusTracking()
    args = get_parser().parse_args()
    img = cv2.imread(args.file)
    p.main(img,visualize=True)
