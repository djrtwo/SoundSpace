import numpy as np
import cv2
import utils
from Contour import Contour
from Blob import Blob

class Region(Contour):
    
    MIN_RATIO = 1/25.0
    MAX_BLOB_RATIO = 0.80
    BLACK_BORDER = True
    next_id = 0
    
    def __init__(self, points, color, centroid_x, centroid_y, area, perimeter):
        Contour.__init__(self, points, color, centroid_x, centroid_y, area, perimeter)
        self.points = utils.approx_contour(points)
        self.id = self.get_next_id()
        self.blobs = []
    
    # alternative constructor from existing Contour object
    @classmethod
    def from_contour(cls, contour):
        return cls(contour.points, contour.color, contour.centroid_x, 
                    contour.centroid_y, contour.area, contour.perimeter)
    
    @classmethod
    def get_next_id(cls):
        next = cls.next_id
        cls.next_id = cls.next_id + 1
        return next
    
    @classmethod
    def find_regions_by_fill_color(cls, image, fill_color=utils.HSV_WHITE):
        # image prep
        # make everything of fill_color (or near fill_color) BGR_WHITE
        #       do this by clever masking.. need to think
        
        return []
        
    @classmethod
    def find_regions_by_border_color(cls, image_BGR, hsv_border_color=utils.HSV_BLACK):
        image_HSV = utils.BGR_to_HSV(image_BGR)
        min_max = utils.HSV_BLACK_RANGE if cls.BLACK_BORDER else utils.get_HSV_range(hsv_border_color)
        thresh = utils.gray_to_BGR(cv2.inRange(image_HSV, min_max['min'], min_max['max']))
        
        # utils.show_image(thresh, 2000, 'debug')
    
        contours = Contour.find_contours(thresh)
        contours = Contour.remove_frame(contours)
        contours = Contour.without_small_contours(contours,         
                                        utils.image_size(image_BGR)*cls.MIN_RATIO)
        regions = []
        for contour in contours:
            regions.append(Region.from_contour(contour))        
        
        return regions
    
    def draw_blobs(self, image, color=None):
        Contour.draw_outlines(self.blobs, image, color)
    
    def find_blobs(self, image):
        blobs = Blob.find_blobs(self.mask_image(image))
        self.blobs = [blob for blob in blobs if blob.area < self.area*self.MAX_BLOB_RATIO]
        return self.blobs
    
    def blob_area(self, image=None):
        if image != None:
            self.find_blobs(image)
        area = 0
        for blob in self.blobs:
            area = area + blob.area
        return area
    
    def blob_to_region_ratio(self, image=None):
        return self.blob_area(image) / self.area
    
    def mask_image(self, image):
        mask = utils.mask_from_contour_points(image, self.points)
        return utils.apply_mask(image, mask)
    
    
