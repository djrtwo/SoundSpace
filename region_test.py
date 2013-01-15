import numpy as np
import cv2
import cv
from Blob import Blob
from Region import Region
import utils

import argparse

def test_blob(image):
    regions = Region.find_regions_by_border_color(image)
    for i, region in enumerate(regions):
        region_mask = region.mask_image(image)
        blobs = region.find_blobs(image)
        Blob.draw_outlines(blobs, region_mask, (234, 34, 102))         
        utils.show_image(region_mask, time=1000)
    
def test_region(image):
    regions = Region.find_regions_by_border_color(image)
    Region.draw_fills(regions, image, (20, 144, 15))
    Region.draw_outlines(regions, image, (144, 144, 255))
    print "number of regions = %s" % len(regions)
    # convert image between color spaces
    
    # #cvCvtColor(source, destination, conversion_code);
    # 
    cv.NamedWindow('a_window', cv.CV_WINDOW_AUTOSIZE)
    cv2.imshow('a_window', image)
    cv.WaitKey(3000)

def main():
    parser = argparse.ArgumentParser(description='Test region functionality')
    parser.add_argument('--file', '-f', dest='file', default='test_images/simple_grid.png', help='file to test', type=str)
    args = parser.parse_args()
    
    image = cv2.imread(args.file)
    
    # test_region(image)
    test_blob(image)

if __name__ == '__main__':
    main()
