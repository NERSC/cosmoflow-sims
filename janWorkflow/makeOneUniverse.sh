#!/bin/bash 
 
set -u ;  # exit  if you try to use an uninitialized variable
set -e ;    #  bash exits if any statement returns a non-true return value
set -o errexit ;  # exit if any statement returns a non-true return value

( sleep 80; echo "TTTTTTTTT1";  date; hostname; free -g; top ibn1)&
( sleep 600; echo "TTTTTTTT2";  date; hostname; free -g; top ibn1)&

module unload darshan
module load cray-fftw gsl cray-hdf5


echo 'U: PWD1 '`pwd`
echo 'U: start MUSIC'
./prepMusic.sh

module load python/2.7-anaconda-4.4
source activate cola_jan1
echo 'U: PWD2 '`pwd`
./rdMeta.py

echo U: start PyCola
#On Haswell:
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/common/software/fftw/3.3.4/hsw/gnu/lib/
#OR on Edison:
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/common/software/fftw/3.3.4/gnu/lib/

time ./pycola-OmSiNs-jan.py  out cosmoMeta.yaml

echo U: start projection ,aka slicing
time ./projectNBody.py out cosmoMeta.yaml


echo U: done
rm out/wnoise*.bin
ls -l out/*hdf5
rm out/*hdf5


exit

Example how to make 1tferc from one Music (all 64 cubes will ahve the same cosmo-params) - this is bad for convergence
echo U: change env for packing
conda deactivate
module load /global/cscratch1/sd/pjm/modulefiles/cosmoflow-gb-apr10
echo U:pack npy to tfrecords
time ./pack_tfrec.py  -X


