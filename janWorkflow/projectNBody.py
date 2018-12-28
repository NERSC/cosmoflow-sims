#!/usr/bin/env python
from __future__ import print_function
__author__ = "Jan Balewski"
__email__ = "janstar1122@gmail.com"


from ruamel.yaml import YAML

import numpy as np
import os, shutil
import math

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



import sys
# - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - 

### This code will take the output of one NBody simulation (ie from the pycola code), and split it into ? sub-volumes, and histogram them. 

## ddefining which files to run over. Basically this was added just to allow me to run multiple jobs in parallel. 

######## Loop over the files!
def projectOne(infile,nbins,coreName):
    histFile=coreName+'_dim%d_full'%nbins
    print('input=',infile,' nbins=',nbins)
    ### First, read in the px/py/pz from the pycola output file
    data = np.load(infile)

    px = data['px']
    py = data['py']
    pz = data['pz']

    print ('pxyz: ',px[0][0][0], py[0][0][0], pz[0][0][0])
   

    #### Try using this hp.histogramdd function...
    ### For this I need to turn the particl elists into coord lists, 
    ### so (  (px[i][j][k], py[i][j][k], pz[i][j][k]), ....)
    pxf = np.ndarray.flatten(px)
    pyf = np.ndarray.flatten(py)
    pzf = np.ndarray.flatten(pz)

    print ('pxf.shape', pxf.shape)
    print ('pxf sample', pxf[0], pyf[0], pzf[0])
    ### so the flattening is working. Now make this into a 3d array...
    ps = np.vstack( (pxf, pyf, pzf) ).T
    
    del(pxf); del(pyf); del(pzf)

    print ("one big vector list ", ps.shape, ps[77,:],'\naccumulate 3D histo...')

    
    ## OK! Then this is indeed a big old array. Now I want to histogram it.
    ## this step goes from a set of parcile coordinates to a histogram of particle counts 
    
    H, bins = np.histogramdd(ps, nbins, range=((0,512),(0,512),(0,512)) )
    # the 512-range must match MUSIC input- is hardcoded

    print ("histo dshape!", H.shape,  H[0][0][0])
    #print ('mass sum=%.3g'%np.sum(H))
    np.save(histFile, H)
    return H

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

def  slice_to_sheets( H, newDim, coreName):
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

from pprint import pprint
if __name__ == '__main__':

#ymlF='outMusic/cosmoMeta.yaml'
    ioPath=sys.argv[1]
    ymlF=sys.argv[2]
    print ("read YAML from ",ymlF,' and pprint it:')
    
    blob=read_yaml(ymlF)

    pprint(blob)
    core=blob['coreStr']
    vectFile=ioPath+'/'+core+'.npz'
    nbins = blob['boxlength']
    fnameSeed=vectFile.replace('.npz','')

    bigH=projectOne(vectFile,nbins,fnameSeed)

    slice_to_cubes( bigH, 128, fnameSeed)
    slice_to_sheets( bigH, 8, fnameSeed)
