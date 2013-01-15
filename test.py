import cv
import cv2
import numpy as np
import utils

def main():
    image = cv2.imread('test_images/simple_grid.png')
    image_HSV = utils.BGR_to_HSV(image)
    
    # NOTE HSV IN PYTHON
    # range from [0, 0, 0] to [180, 255, 255]
    # MIN = np.array([0, 0, 200], np.uint8)
    # MAX = np.array([10, 10, 255], np.uint8)
    
    min_max = utils.get_HSV_range(utils.HSV_BLACK)
    print "max : %s" % min_max['max']
    print "min : %s" % min_max['min']
    # MIN = np.array([0, 0, 0], np.uint8)
    # MAX = np.array([10, 10, 10], np.uint8)
    
    # below = utils.get_colored_image(image_HSV.shape, utils.HSV_BLACK)
    #     above = utils.get_colored_image(image_HSV.shape, utils.HSV_BLACK)
    
    # below = utils.get_colored_image(image_HSV.shape, (0, 0, 90))
    # above = utils.get_colored_image(image_HSV.shape, (10, 10, 100))
    
    thresh = cv2.inRange(image_HSV, min_max['min'], min_max['max'])
    cv.NamedWindow('a_window', cv.CV_WINDOW_AUTOSIZE)
    cv2.imshow('a_window', thresh)
    cv.WaitKey(1000)

if __name__ == "__main__":
    main()