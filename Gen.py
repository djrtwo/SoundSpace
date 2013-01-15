import numpy as np
import cv2
import cv
from Blob import Blob
from Region import Region

class Gen(object):
    
    def __init__(self, gen_type):
        self.gen_type = gen_type
        self.out_patches = []
        self.in_patches = []
        self.attrs = {}
        self.attrs['gain'] = 1.0
        
    def __str__(self):
        return self.gen_type
        
    @property
    def is_root(self):
        return not self.in_patches
    
    def add_patch_to(self, gen):
        self.out_patches.append(gen)
        gen.in_patches.append(self)
    
    def remove_patch_to(self, gen):
        try:
            self.out_patches.remove(gen)
        except ValueError:
            pass
        try:
            gen.in_patches.remove(self)
        except ValueError:
            pass

    def is_dac(self):
        return False
        