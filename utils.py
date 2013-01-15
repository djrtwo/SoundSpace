import numpy as np
import cv2
import cv

# CONFIG PROPERTIES
THRESHOLD = 100
CHUCK_PORT = 9000

# CONSTANTS
HSV_RANGE = np.array([10, 50, 50], np.uint8)
BGR_WHITE = (255, 255, 255)
BGR_BLACK = (0, 0, 0)
BGR_RED   = (0, 0, 255)
BGR_GREEN = (0, 255, 0)
BGR_BLUE  = (255, 0, 0)
HSV_WHITE = np.array([0,0,255], np.uint8)
HSV_BLACK = np.array([0,0,0], np.uint8)
HSV_BLACK_RANGE = {
                    'min':np.array([0,0,0], np.uint8),
                    'max':np.array([180, 255, 0.3*255], np.uint8)
                  }

def show_image(image, time=3000, title='show_window'):
    cv2.imshow(title, image)
    cv2.waitKey(time)

def image_size(image):
    return image.shape[0] * image.shape[1]

def copy_image(image):
    return np.copy(image)

def get_invert_image(image):
    invert = np.zeros(image.shape, np.uint8)
    invert.fill(255)
    return invert-image

def apply_mask(image, mask):
    return cv2.bitwise_and(image, image, mask = mask)

def find_contours(image, threshold=THRESHOLD):
    image_gray = BGR_to_gray(image)
    ret, thresh = cv2.threshold(image_gray, threshold, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE)
    return contours

def approx_contour(contour, arc_ratio = 0.05):
    return cv2.approxPolyDP(contour, arc_ratio*cv2.arcLength(contour,True), True)

# image is needed to know the mask size
def mask_from_contour_points(image, contour):
    image_gray = BGR_to_gray(image)
    mask = np.zeros(image_gray.shape, np.uint8)
    cv2.drawContours(mask, [contour], 0, 255, -1)
    return mask
    
def BGR_to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
def BGR_to_HSV(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def gray_to_BGR(image):
    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

def get_HSV_range(color, span=HSV_RANGE):
    HSV_range  = {}
    HSV_range['max'] = cv2.add(color, span/2)
    HSV_range['min'] = cv2.subtract(color, span/2)
    return HSV_range

#
# Find extreme points
#
def leftmost_contour_pt(contour):
    return tuple(contour[contour[:,:,0].argmin()][0])

def rightmost_contour_pt(contour):
    return tuple(contour[contour[:,:,0].argmax()][0])

def topmost_contour_pt(contour):
    return tuple(contour[contour[:,:,1].argmin()][0])
    
def bottommost_contour_pt(contour):
    return tuple(contour[contour[:,:,1].argmax()][0])
    
#
# Drawing
#
def get_colored_image(shape, color=None):
    image = np.zeros(shape, np.uint8)
    if color is not None:
        cv2.rectangle(image, (0,0), (shape[0], shape[1]), color, cv.CV_FILLED)
    return image
    
#
# OSC utils
#
# def osc_