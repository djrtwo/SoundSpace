from Gen import Gen
from MiscGens import *
from Oscillators import *
from Region import Region

ACCUM = 10
WEIGHT_FACTOR = 0.5

class GenMap(object):
    
    def __init__(self, gen, region, attr_range=[0.0, 1.0]):
        self.gen = gen
        self.region = region
        self.attr_range = attr_range
        self.last_ratio = []   
    
    def weighted_average(self):
        divisor = 0
        numerator = 0
        weight = 1.0
        for attr in self.last_ratio:
            numerator = numerator + attr * weight
            divisor = divisor + weight
            weight = weight * WEIGHT_FACTOR
        
        return numerator / divisor
    
    def update_attrs(self, image):
        ratio = self.region.blob_to_region_ratio(image)
        if len(self.last_ratio) < ACCUM:
            self.last_ratio.append(ratio)
        else:
            self.last_ratio = self.last_ratio[1:] + [ratio]
            
        avg_ratio = self.weighted_average()
        
        if isinstance(self.gen, Gain):
            self.gen.attrs['gain'] = avg_ratio*(4.0/3.0) if avg_ratio*(4.0/3.0) < 1.0 else 1.0
        elif isinstance(self.gen, Osc):
            freq = avg_ratio*(self.attr_range[1]-self.attr_range[0]) + self.attr_range[0]
            self.gen.attrs['freq'] = freq
            