import numpy as np
import cv2
import utils
from Contour import Contour

PIXEL_MIN = 20

class Blob(Contour):
    
    DARK_ON_LIGHT = True
    
    def __init__(self, points, color, centroid_x, centroid_y, area, perimeter):
        Contour.__init__(self, points, color, centroid_x, centroid_y, area, perimeter)
    
    # def __str__(self):
    #     return "%s" % self.contour
    
    # alternative constructor from existing Contour object
    @classmethod
    def from_contour(cls, contour):
        return cls(contour.points, contour.color, contour.centroid_x, 
                    contour.centroid_y, contour.area, contour.perimeter)
    
    @classmethod
    def find_blobs(cls, image):
        blobs = []
        if cls.DARK_ON_LIGHT:
            image = utils.get_invert_image(image)
        contours = Contour.find_contours(image, 150)
        for contour in contours:
            if contour.area >= PIXEL_MIN:
                blobs.append(Blob.from_contour(contour))
        return blobs
        
        