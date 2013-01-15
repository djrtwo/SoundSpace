import numpy as np
import cv2
import cv
from osc_utils import *
from Blob import Blob
from Region import Region
from Patch import Patch
import utils
import threading
import time
from Gen import *
from Oscillators import *
from MiscGens import *
from GenMap import GenMap

class TextOutput(object):
    
    def __init__(self, text, loc, scale=1.0, 
                    font=cv2.FONT_HERSHEY_TRIPLEX, color=(0,0,0)):
        self.text = text
        self.loc = loc
        self.scale = scale
        self.font = font
        self.color = color

class CameraOutThread(threading.Thread):
    
    def __init__(self, cam, scale=1.0, font=cv2.FONT_HERSHEY_TRIPLEX, color=(0,0,0)):
        threading.Thread.__init__(self)
        self.cam = cam
        self.text_outputs = []
        self.gen_maps = {}
        self.font = font
        self.color = color
        self.scale = scale
    
    def run(self):
        num_round = 0
        while(1):
            _,f = self.cam.read()
            if self.gen_maps:
                for gm_id in self.gen_maps:
                    self.gen_maps[gm_id].update_attrs(utils.copy_image(f))
                Patch.osc_update_all_attrs()
            
            for output in self.text_outputs:
                cv2.putText(f, output.text, output.loc, 
                            output.font, output.scale, output.color)
            
            if num_round % 30 == 0:
                for gm_id in self.gen_maps:
                    gm = self.gen_maps[gm_id]
                    cv2.putText(f, '%s-%s' % (gm.region.id, gm.gen.gen_type),
                                    (gm.region.centroid_x, gm.region.centroid_y),
                                    self.font, self.scale, self.color)
                    gm.region.draw_outline(f, utils.BGR_RED)
                    gm.region.draw_blobs(f, utils.BGR_GREEN)
            
            cv2.imshow('e2',f)
            if cv2.waitKey(10)==27:
                break
        cv2.destroyAllWindows()
    
    def add_text(self, text_output):
        self.text_outputs.append(text_output)

def start():
    # init camera
    cam = cv2.VideoCapture(1)
    
    # init osc communication with chuck
    initOSCClient()

    cam_thread = CameraOutThread(cam)
    cam_thread.start()
    
    time.sleep(0.5)
    raw_input("Press Enter when camera is positioned")
    
    # display numbers on regions
    image = cam.read()
    regions = Region.find_regions_by_border_color(image[1])
    for region in regions:
        cam_thread.add_text(TextOutput(str(region.id), (region.centroid_x, region.centroid_y)))
    
    # ask for Gen type for each region
    dac = DAC()
    gen_maps = {}
    for i, region in enumerate(regions):
        while (True):
            try:
                gen_type = raw_input("Please enter UGen type for region %s: " % region.id)
                gen = eval(gen_type)()
                attr_range = [0.0, 1.0]
                if isinstance(gen, Osc):
                    attr_range[0] = float(raw_input("    What is the low frequency on this oscillator? "))
                    attr_range[1] = float(raw_input("    What is the high frequency on this oscillator? "))
                    
                gen_maps[region.id] = GenMap(gen, region, attr_range=attr_range)
                break
            except:
                print 'Invalid UGen, try again.'

    # ask for gen links 
    # dac special to_where
    while (raw_input("Add a patch? (y/n): ") == 'y'):
        from_where = None
        while (True):
            try:
                # NOTE: no range checking
                from_where = int(raw_input('from Region #: '))
                from_where = gen_maps[from_where]
                break
            except ValueError:
                print 'Please enter an integer.'
                
        to_where = None
        while (True):
            try:
                to_where = raw_input('to Region #: ')
                if to_where == 'dac':
                    to_where = dac
                    break
                to_where = int(to_where)
                to_where = gen_maps[to_where]
                break
            except ValueError:
                print 'Please enter an integer.'
        
        # will handle dac later
        # for now, all patch paths assumed end in dac
        if not isinstance(to_where, DAC):
            (from_where.gen).add_patch_to(to_where.gen)
    
    Patch.find_patches([gen_maps[gm_id].gen for gm_id in gen_maps])
    Patch.osc_send_all_patches()
    
    cam_thread.text_outputs = []
    cam_thread.gen_maps = gen_maps
            
    # start system updating the blob in the regions
    # sending attr data to chuck

if __name__ == "__main__":
    start()