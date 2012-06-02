# AP Physics Final Project 2012
# Author: Fouad Matin
# 
# Copyright (c) 2011 Fouad Matin
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import sys
import cv
import time

filename = '/Users/fouad/dropbox/code/py/physics-final2012/close.mov'

def find_ball(image):

  size = cv.GetSize(image)

  #prepare memory
  ball = cv.CreateImage(size, 8, 1)
  hsv = cv.CreateImage(size, 8, 3)
  sat = cv.CreateImage(size, 8, 1)
  yellow = cv.CreateImage(size, 8, 1)

  #split image into hsv, grab the sat
  cv.CvtColor(image, hsv, cv.CV_BGR2HSV)
  cv.Split(hsv, None, sat, None, None)

  #split image into rgb
  cv.Split(image, None, None, yellow, None)
  #find the ball by looking for yellow, with high saturation
  cv.Threshold(yellow, yellow, 128, 255, cv.CV_THRESH_BINARY)
  cv.Threshold(sat, sat, 128, 255, cv.CV_THRESH_BINARY)
  #AND the two thresholds, finding the ball
  cv.Mul(yellow, sat, ball)

  #remove noise, highlighting the ball
  cv.Erode(ball, ball, iterations=5)
  cv.Dilate(ball, ball, iterations=5)

  storage = cv.CreateMemStorage(0)
  obj = cv.FindContours(ball, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
  cv.ShowImage('A', ball)
  if not obj:
    return(0, 0, 0, 0)
  else:
    return cv.BoundingRect(obj)

points = []
capture = cv.CaptureFromFile( filename )
if not capture:
  print "Error opening video file"
  sys.exit(1)

cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

lastpoint = (0,0)
while True:
  original = cv.QueryFrame(capture)
  obj_rect = find_ball(original)
  print obj_rect
  if obj_rect != (0,0,0,0):
    middle = (obj_rect[0] + (obj_rect[2] / 2), obj_rect[1] + (obj_rect[3]/2))
    if points == []:
      points.append(middle)       
    else:
      if abs(points[-1][0] - middle[0]) > 5 and abs(points[-1][1] - middle[1]) > 10:
        points.append(middle)

  cv.Rectangle(original,  (obj_rect[0], obj_rect[1]),  (obj_rect[0] + obj_rect[2], obj_rect[1] + obj_rect[3]),  (255, 0, 0),  1,  8,  0)
  for point, previous in zip(points, points[1::]):
    if lastpoint != (0,0) and point != (0,0):
      cv.Line(original, point, previous, (0, 0, 255), 2)
    cv.Circle(original, point,  1,  (0, 255, 255),  -1,  100,  0)
    lastpoint = point

  cv.ShowImage('Analyzed', original)
  k = cv.WaitKey(50)
  if k == 0x1b:
    print "Saving and closing."
    name = filename.split('/')[-1]
    imgname = 'Processed-'+name+'.JPG'
    print imgname
    cv.SaveImage(imgname, original)
    time.sleep(2)
    sys.exit(1)
  
  if cv.WaitKey(10) >=0:
     sys.exit(1)
    