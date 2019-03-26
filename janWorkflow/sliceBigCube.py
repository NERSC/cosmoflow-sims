#!/usr/bin/env python

__author__ = "Jan Balewski"
__email__ = "janstar1122@gmail.com"

from ruamel.yaml import YAML

import numpy as np
import os, shutil
import math, sys

def read_yaml(yaml_fn,verb=1):
        data={}

        if verb:  print('  read  yaml:',yaml_fn)
        with open(yaml_fn) as yamlfile:
            for key, val in YAML().load(yamlfile).items():
                print('hpar:',key, val)
                data[key]=val
        assert len(data['namePar']) == len(data['unitPar'])
        assert len(data['physPar']) == len(data['unitPar'])

        return data


# - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - 

def  slice_to_cubes( H, newDim,coreName):
 
    ### now I have my histogram of particle density, I split it up into 8 subvolumes and write it out
    ### note that the file structure here is required from the legacy CosmoFlow code. One dir is created for each NBody output file, then the 8 sub-volumes are named [0-7].npy inside that dir. 
    print('slice_to_cubes dim=',newDim)
    bigDim=H.shape[0]
    assert bigDim%newDim==0
    count = -1
    for i in range(0,bigDim, newDim ):
        for j in range(0, bigDim, newDim):
            for k in range(0, bigDim, newDim):
                count+=1
                d = H[i:(i+newDim),j:(j+newDim),k:(k+newDim)]
                histFile=coreName+'_dim%d_cube%d'%(d.shape[0],count)
                print (count,'mass sum=%.3g'%np.sum(d))
                np.save(histFile, d)
                
    print ("got cube count :", count)

    print ("**************************")

# - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - 

def  slice_to_fullSheets( H, newDim, coreName):
    print('slice_to_shits shortDim=',newDim)
    bigDim=H.shape[0]
    assert bigDim%newDim==0
 
    count = -1
    step=newDim
    for i in range(0, bigDim, step):
                count+=1
                d = H[:,:,i:(i+step)] # the last dim is shorter
                histFile=coreName+'_dim%d_sheet%d'%(bigDim,count)
                print (count,'mass sum=%.3g'%np.sum(d))
                np.save(histFile, d)
                
    print ("got sheet count :", count)

    print ("**************************")



# - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - 


def  slice_to_subSheets( H, stepXY,stepZ, coreName):
    print('slice_to_sheets stepXY=%d stepZ=%d'%(stepXY,stepZ))
    bigDim=H.shape[0]
    assert bigDim%stepZ==0
    assert bigDim%stepXY==0
 
    count = -1
    for iz in range(0, bigDim, stepZ):
        for ix in range(0, bigDim, stepXY): 
            for iy in range(0, bigDim, stepXY):
                count+=1
                d = H[ix:(ix+stepXY),iy:(iy+stepXY),iz:(iz+stepZ)] # the last dim is shorter
                histFile=coreName+'_xy%d_z%d_slice%d'%(stepXY,stepZ,count)
                if count%23==0:
                        print (count,'mass sum=%.3g'%np.sum(d), d.shape,ix,iy,iz)
                np.save(histFile, d)
                
    print ("got sheet count :", count)

    print ("**************************")

# - - - - - - - - - - - - - - - - - - - - - - 
# - -  M A I N E 
# - - - - - - - - - - - - - - - - - - - - - - 

from pprint import pprint
if __name__ == '__main__':

    inPath=sys.argv[1]+'/'
    ymlF=sys.argv[2]
    print ("read YAML from ",ymlF,' and pprint it:')
    
    blob=read_yaml(ymlF)
    outPath=inPath
    pprint(blob)

    core=blob['coreStr']
    #ics_2018-11_d14600087_dim512_full.npy
    bigFileN=inPath+core+'_dim512_full.npy'
    nbins = blob['boxlength']

    bigH=np.load(bigFileN)
    print('shape1:',bigH.shape)
    fnameSeed=outPath+core

    slice_to_cubes( bigH, 128, fnameSeed)
    #slice_to_cubes( bigH, 256, fnameSeed)
    slice_to_fullSheets( bigH, 1, fnameSeed)
    #slice_to_subSheets( bigH, 256,4, fnameSeed)
