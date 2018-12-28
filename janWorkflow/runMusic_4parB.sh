#!/bin/bash

set -u ;  # exit  if you try to use an uninitialized variable
set -e ;    #  bash exits if any statement returns a non-true return value
set -o errexit ;  # exit if any statement returns a non-true return value

# this function returns 3 type of values derived from the same 3-byte random int
myRandomF () {
    rndI=`od -A n -t d -N 3 /dev/random | tr -d ' '`
    # This is 3-byte truly random generator, max value: 256^3=16777216-1
    rndF=` echo $rndI | awk  '{printf "%.7f", $1/ 16777216 *2 -1. }'`
    #rnd1eps=` echo $rndF | awk  '{printf "%.7f", $1 * 0.1 }'`
    #echo rndI=$rndI rndF=$rndF rnd1eps=$rnd1eps
}


outPath=${1-out}

#OUTPUTS:

# STEP 1 - - - -   generate unique seed for MUSIC
myRandomF 
seed9=$rndI
core=ics_2018-12_b$rndI
musicTempl=ics_template.conf
musicConf=${core}.conf
musicHDF5=${core}.hdf5
# yaml w/ metaData
ymlF=${outPath}/'cosmoMeta.yaml'

# unit-params
myRandomF
uOmega_m=$rndF
myRandomF
uSigma_8=$rndF
myRandomF
uN_spec=$rndF
myRandomF
uH_0=$rndF

#echo $uOmega_m $uSigma_8 $uN_spec $uH_0

#phys-params
Omega_m=` echo $uOmega_m | awk '{printf "%f", (1.+$1*0.30)* 0.5 }'` 
sigma_8=` echo $uSigma_8 | awk '{printf "%f", (1.+$1*0.30)* 0.75 }'` 
N_spec=`  echo $uN_spec  | awk '{printf "%f", (1.+$1*0.30)* 1.0 }'` 
H_0=`     echo $uH_0     | awk '{printf "%f", (1.+$1*0.30)* 70.0  }'` 

#echo $Omega_m $sigma_8 $N_spec $H0
boxlength=512

# - - - - - -  create meta-data
echo "date: "`date` > $ymlF
echo 'namePar: ' >> $ymlF
echo '- Omega_m ' >> $ymlF
echo '- sigma_8 ' >> $ymlF
echo '- N_spec ' >> $ymlF
echo '- H_0 ' >> $ymlF

echo 'unitPar:' >> $ymlF
echo "- $uOmega_m" >> $ymlF
echo "- $uSigma_8" >> $ymlF
echo "- $uN_spec" >> $ymlF
echo "- $uH_0" >> $ymlF

echo 'physPar:' >> $ymlF
echo "- $Omega_m" >> $ymlF
echo "- $sigma_8" >> $ymlF
echo "- $N_spec" >> $ymlF
echo "- $H_0" >> $ymlF

echo "coreStr : $core" >> $ymlF
echo "boxlength : $boxlength" >> $ymlF
echo "seed9 : $seed9" >> $ymlF
echo "physOmega_m:  $Omega_m" >> $ymlF

# - - - - - -prepare SED edits
SEDINP=${outPath}/tmp.fix_${core}
echo "s/<boxlength>/$boxlength/g" >$SEDINP
echo "s/<seed9>/$seed9/g" >>$SEDINP
echo "s/<Omega_m>/$Omega_m/g" >>$SEDINP
echo "s/<sigma_8>/$sigma_8/g" >>$SEDINP
echo "s/<N_spec>/$N_spec/g" >>$SEDINP
echo "s/<H_0>/$H_0/g" >>$SEDINP
echo "s|<musicHDF5>|$musicHDF5|g" >>$SEDINP

echo make new config with $musicTempl
cat $SEDINP
[ ! -f $musicTempl ] && { echo "$musicTempl file not found, abort"; exit 98; }
cat  $musicTempl  |sed -f $SEDINP > ${outPath}/$musicConf

pwd
cd ${outPath}
pwd
MusicExe=/global/homes/b/balewski/prj/cosmoflow-sims/MUSIC/MUSIC
echo 'start MUSIC $musicConf '`date`
time $MusicExe $musicConf

echo 'done Music '`date`

