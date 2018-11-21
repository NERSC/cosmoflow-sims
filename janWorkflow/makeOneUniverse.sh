#!/bin/bash 
 
set -u ;  # exit  if you try to use an uninitialized variable
set -e ;    #  bash exits if any statement returns a non-true return value
set -o errexit ;  # exit if any statement returns a non-true return value

( sleep 40; echo "TTTTTTTTT1";  date; hostname; free -g; top ibn1)&
( sleep 500; echo "TTTTTTTT2";  date; hostname; free -g; top ibn1)&

module unload darshan
module load cray-fftw gsl cray-hdf5


echo 'U: PWD1 '`pwd`
echo 'U: start MUSIC'
./runMusic_2parB.sh

module unload python/3.6-anaconda-4.4
module load python/2.7-anaconda-4.4
source activate cola_jan1
echo 'U: PWD2 '`pwd`
./rdMeta.py

coreStr=`grep coreStr out/cosmoMeta.yaml |  awk  '{printf "%s", $3 }'`
echo U: coreStr=$coreStr

echo U: start PyCola coreStr=$coreStr
#On Haswell:
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/common/software/fftw/3.3.4/hsw/gnu/lib/
#OR on Edison:
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/common/software/fftw/3.3.4/gnu/lib/

time ./pycola-OmSiNs-jan.py  out cosmoMeta.yaml

echo U: start projection and  slicing
time ./projectNBody.py out cosmoMeta.yaml

echo U: optional produce  input for Pk
module unload python/2.7-anaconda-4.4
module load python/3.6-anaconda-4.4
time ./pack_hd5_Pk.py out/$coreStr

srun -n 32 -c 2 --cpu_bind=cores /project/projectdirs/mpccc/balewski/cosmo-gimlet2/apps/matter_pk/matter_pk.ex out/${coreStr}.nyx.hdf5  out/${coreStr}

#gnuplot> set logscale
#gnuplot> plot "ics_2018-12_a12383763_rhom_ps3d.txt" u 3:4 w lines
echo U: plot Pk
gnuplot  <<-EOFMarker
    set title "Pk for ${coreStr}" font ",14" textcolor rgbcolor "royalblue"
    set pointsize 1
    set logscale
    set terminal png   
    set output  "out/${coreStr}_rhom_ps3d.png"    
    plot "out/${coreStr}_rhom_ps3d.txt" u 3:4 w lines
EOFMarker

echo U: done
rm out/wnoise*.bin
ls -lh out/*hdf5
rm out/*hdf5
rm out/winoise*bin


exit

Example how to make 1tferc from one Music (all 64 cubes will ahve the same cosmo-params) - this is bad for convergence
echo U: change env for packing
conda deactivate
module load /global/cscratch1/sd/pjm/modulefiles/cosmoflow-gb-apr10
echo U:pack npy to tfrecords
time ./pack_tfrec.py  -X


