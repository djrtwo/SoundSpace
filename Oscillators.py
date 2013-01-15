import numpy as np
import cv2
import cv
from Gen import Gen

class Osc(Gen):
    
    def __init__(self, name):
        Gen.__init__(self, name)
        self.attrs['freq'] = 220.0
        self.attrs['phase'] = 0.0
        self.attrs['sync'] = 2.0

    def update_attrs(self, updates = {}):
        for attr_type in updates:
            if attr_type in self.attrs:
                self.attrs[attr_type] = updates[attr_type]
    
class Phasor(Osc):
    
    def __init__(self):
        Osc.__init__(self, self.__class__.__name__)
    
class SinOsc(Osc):

    def __init__(self):
        Osc.__init__(self, self.__class__.__name__)

class PulsOsc(Osc):

    def __init__(self):
        Osc.__init__(self, self.__class__.__name__)
        self.attrs['width'] = 0.5

class SqrOsc(Osc):

    def __init__(self):
        Osc.__init__(self, self.__class__.__name__)
        self.attrs['width'] = 0.5

class TriOsc(Osc):

    def __init__(self):
        Osc.__init__(self, self.__class__.__name__)
        self.attrs['width'] = 0.5

class SawOsc(Osc):

    def __init__(self):
        Osc.__init__(self, self.__class__.__name__)
        self.attrs['width'] = 1.0


