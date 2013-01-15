from Oscillators import *
from Patch import Patch
from osc_utils import *
from random import random
import time

def main():
    initOSCClient()
    
    gens = [SinOsc(None), SawOsc(None)]
    # sinA = SinOsc(None)
    # sawA = SawOsc(None)
    
    for gen in gens:
        if gen.is_root:
            Patch.dfs_patch_search(gen)
    Patch.osc_send_all_patches()
    
    while (True):
        for gen in gens:
            gen.attrs['gain'] = random()
        Patch.osc_update_all_attrs()
        time.sleep(0.5)
    

if __name__ == "__main__":
    main()