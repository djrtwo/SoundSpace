import numpy as np
import cv2
import cv
from Gen import Gen
from MiscGens import DAC
from osc_utils import *
from copy import copy
import time

class Patch(object):
    
    next_id = 0
    patch_list = []
    dac_list = []
    
    def __init__(self, root_gen=None):
        self.patch_chain = [root_gen] if root_gen else []
        self.id = None
        self.patch_sent = False
    
    def __eq__(self, other):
        if len(self.patch_chain) != len(other.patch_chain):
            return False
        for i, gen in enumerate(self.patch_chain):
            if gen != other.patch_chain[i]:
                return False
        return True
    
    def __copy__(self):
        result = Patch()
        for gen in self.patch_chain:
            result.add(gen)
        return result
    
    def __str__(self):
        result = '%s: ' % self.id
        for i, gen in enumerate(self.patch_chain):
            result = result +' => ' + str(gen) if i!=0 else result + str(gen)
        return result
    
    @classmethod
    def get_next_id(cls):
        next = cls.next_id
        cls.next_id = cls.next_id + 1
        return next
    
    def add(self, gen):
        self.patch_chain.append(gen)
    
    def osc_send_patch(self):
        if (self.patch_sent):
            pass
        else:
            sendOSCMsg("/new_patch", [self.id, len(self.patch_chain)])
            self.patch_sent = True
            time.sleep(0.01)
            self.osc_update_gens()
            self.osc_update_attrs()
            
    def osc_update_gens(self):
        for i, gen in enumerate(self.patch_chain):
            sendOSCMsg("/set_ugen/"+str(self.id), [i, gen.gen_type])
    
    def osc_update_attrs(self):
        for i, gen in enumerate(self.patch_chain):
            # print 'update %s' % self 
            for attr in gen.attrs:
                # print "%s : %s" % (attr, gen.attrs[attr])
                sendOSCMsg("/set_attr/"+str(self.id), [i, attr, gen.attrs[attr]])
    
    @classmethod
    def osc_send_all_patches(cls):
        for patch in cls.patch_list:
            patch.osc_send_patch()
    
    @classmethod
    def osc_update_all_gens(cls):
        for patch in cls.patch_list:
            patch.osc_update_gens()
        
    @classmethod
    def osc_update_all_attrs(cls):
        for patch in cls.patch_list:
            patch.osc_update_attrs()
    
    @classmethod
    def find_patches(cls, gens):
        for gen in gens:
            if gen.is_root:
                cls.dfs_patch_search(gen)
    
    @classmethod
    def dfs_patch_search(cls, gen):
        cls.dfs_patch_recur(Patch(gen))
        # for p in cls.patch_list:
        #     if isinstance(p.patch_chain[-1], DAC):
        #         cls.dac_list.append(p)
    
    @classmethod
    def dfs_patch_recur(cls, patch):
        last_gen = patch.patch_chain[-1]    
        if not last_gen.out_patches:
            if patch not in cls.patch_list:
                patch.id = cls.get_next_id()
                cls.patch_list.append(patch)
        for i, gen in enumerate(last_gen.out_patches):
            if gen in patch.patch_chain:
                # DECIDE HOW TO HANDLE PATCH LOOPS
                print 'patch loop'
                continue
            send_patch = copy(patch)
            send_patch.add(gen)
            cls.dfs_patch_recur(send_patch)
    
    
    
