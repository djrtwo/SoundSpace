import numpy as np
import cv2
import cv
from Gen import Gen

class Gain(Gen):
    
    def __init__(self):
        Gen.__init__(self, self.__class__.__name__)

class DAC(Gen):
    
    def __init__(self):
        Gen.__init__(self, self.__class__.__name__)
    
    def is_dac(self):
        return True