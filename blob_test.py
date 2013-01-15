#
# http://opencvpython.blogspot.com/2012/06/hi-this-article-is-tutorial-which-try.html
# article discusses how to use thresholding to find objects (contours)
# then discusses iterating through contours while using masks to get the average
# color of each object.  SUPER USEFUL
# 
import numpy as np
import cv2
import cv
from Blob import Blob

import argparse

def main():
    parser = argparse.ArgumentParser(description='Test blob functionality')
    parser.add_argument('--file', '-f', dest='file', default='test_images/balls.png', help='file to test', type=str)
    args = parser.parse_args()
    
    image = cv2.imread(args.file)
    blobs = Blob.find_blobs(image)
    for blob in blobs:
        blob.draw_outline(image, color=(0, 255, 0))
        blob.draw_fill(image, color=(255,0,0))
        print blob

    cv.NamedWindow('a_window', cv.CV_WINDOW_AUTOSIZE)
    cv2.imshow('a_window', image)
    cv.WaitKey(10000)

if __name__ == '__main__':
    main()


# # ALSO START TO ORGANIZE INTO A BLOB OBJECT
# # AND REGION OBJECTS 
#     
