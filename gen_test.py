from Gen import Gen
from Patch import Patch

def main():
    genA = Gen(None, 'genA')
    genB = Gen(None, 'genB')
    genC = Gen(None, 'genC')
    genD = Gen(None, 'genD')
    genE = Gen(None, 'genE')
    genF = Gen(None, 'genF')
    
    genA.add_patch_to(genB)
    genB.add_patch_to(genC)
    genB.add_patch_to(genD)
    genD.add_patch_to(genA)
    genD.add_patch_to(genE)
    
    Patch.dfs_patch_search(genA)
    for patch in Patch.patch_list:
        print patch
    
    genB.add_patch_to(genF)
    Patch.dfs_patch_search(genA)
    for patch in Patch.patch_list:
        print patch

if __name__ == '__main__':
    main()