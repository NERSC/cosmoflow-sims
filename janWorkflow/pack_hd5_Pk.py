#!/usr/bin/env python
import sys
(va,vb,vc,vd,ve)=sys.version_info ; assert(va==3)  # needes Python3

import sys
import h5py
import numpy as np

# - - - - - - - -
def  _QA_dataH3(dataH3):
    print('got H3:',dataH3.shape)
    sum=np.sum(dataH3)
    nx,ny,nz=dataH3.shape
    fac=sum/nx/ny/nz
    print('sum0',sum,'fac=',fac) 
    assert np.abs(fac-1.) <1.e-3
    

# - - - - - - - -
gDeep=0

def _list_all(ds,name):
    global gDeep
    print('list content for %s gDeep=%d'%(name,gDeep))
    gDeep+=1
    print('ds atr:')
    aN=list(ds.attrs.keys())
    aV=list(ds.attrs.values())
    
    print('aN',aN)
    print('aV',aV)

    try:
        for g in ds.keys():
            _list_all(ds[g],g)
    except:
        a=1
    gDeep-=1

# - - - - - - - -
def _copy_all(src,dst):
   # head
    for atr in src.attrs.keys():
        val=src.attrs[atr]
        #print('add attr',atr,val)
        dst.attrs.create(atr,val)
 
    # work with data sets
    try:
      for g in src.keys():
          src[g].copy(src[g],dst,g)
    except Exception as e:
      print ('error in copy:',e)
      pass

# - - - - - - - -
# - - - - - - - -
if __name__=="__main__":

  if (len(sys.argv)) < 2:
     print ('args:  coreName missing')
     exit()
  templHDF5='/global/homes/b/balewski/prj/cosmoflow-sims/janWorkflow/example-z5.hdf5'

  coreName=sys.argv[1]
  inpH3=coreName+'_dim512_full.npy'
  outHDF5=coreName+'.nyx.hdf5'
  print('pack-h5 core:')

  src = h5py.File(templHDF5,'r')
  dst = h5py.File(outHDF5,'w')
  dataH3 = np.load(inpH3)
  
  _QA_dataH3(dataH3)
  #_list_all(src,'main')
  _copy_all(src,dst)
  print ('modifying  cloned dset')
  #dataH3 = np.zeros((512,512,512))
  #dataH3 = np.zeros((12,12,12))

  del dst['native_fields/matter_density']
  dset = dst.create_dataset('native_fields/matter_density', data=dataH3)

  dd=dst['domain']
  newAtr={'shape':[512,512,512], 'size':[ 512., 512., 512.]}

  for atr in dd.attrs.keys():
      val=dd.attrs[atr]
      #print('DD attr',atr,val)
      dd.attrs.create(atr,newAtr[atr])

  # erase cosmo params
  dd=dst['universe']
  for atr in dd.attrs.keys():
      dd.attrs.create(atr,0.5)

  #_list_all(dd,'BBB')
  try:
     src.close()
     dst.close()
  except Exception as e: 
     print ('error in file closing')


