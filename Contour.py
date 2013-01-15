import numpy as np
import cv2
import utils

class Contour(object):
    
    THRESHOLD = 200
    
    def __init__(self, points, color, centroid_x, centroid_y, area, perimeter):
        self.points = points
        self.color = color
        self.centroid_x = centroid_x
        self.centroid_y = centroid_y
        self.area = area
        self.perimeter = perimeter

    def __str__(self):
        return """
color: %s
centroid: (%s, %s)
area: %s
perimeter: %s
""" % (self.color, self.centroid_x, self.centroid_y, self.area, self.perimeter)

    @classmethod
    def find_contours(cls, image, threshold=THRESHOLD):
        image_gray = utils.BGR_to_gray(image)
        ret, thresh = cv2.threshold(image_gray, threshold, 255, 0)
        base_contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_SIMPLE)
        
        # base_contours = [utils.approx_contour(cnt) for cnt in base_contours]
        
        contours = []
        for contour in base_contours:
            area = cv2.contourArea(contour)
            
            mask = utils.mask_from_contour_points(image, contour)
            color = cv2.mean(image, mask=mask)
            
            perimeter = cv2.arcLength(contour, True)

            M = cv2.moments(contour)
            try:
                centroid_x = int(M['m10']/M['m00'])
                centroid_y = int(M['m01']/M['m00'])
            
                contours.append(Contour(contour, color, centroid_x, centroid_y, area, perimeter))
            except ZeroDivisionError:
                pass
        
        return contours
       
    @classmethod
    def draw_outlines(cls, contours, image, color=None, thickness=3):
        for contour in contours:
            contour.draw_outline(image, color, thickness)
            
    @classmethod
    def draw_fills(cls, contours, image, color=None):
        for contour in contours:
            contour.draw_fill(image, color)
    
    @classmethod
    def remove_frame(cls, contours):
        max_contour = contours[0]
        for contour in contours:
            max_contour = contour if contour.area > max_contour.area else max_contour
        return [c for c in contours if c != max_contour]
     
    @classmethod
    def without_small_contours(cls, contours, min_size):
        return [c for c in contours if c.area > min_size ]
    
    def draw_outline(self, image, color=None, thickness=3):
        color = color if color else self.color
        cv2.drawContours(image, [self.points], 0, color, thickness)
        return image
        
    def draw_fill(self, image, color=None):
        return self.draw_outline(image, color, -1)
    
    
    