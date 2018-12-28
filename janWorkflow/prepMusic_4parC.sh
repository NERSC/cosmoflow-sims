#!/bin/bash

set -u ;  # exit  if you try to use an uninitialized variable
set -e ;    #  bash exits if any statement returns a non-true return value
set -o errexit ;  # exit if any statement returns a non-true return value
nTime=${1-1}
outPath=${2-out}
zArr=(0.0  0.5  1.5  3.0)
#zArr=(0.0 0.0 0.0  3.0)
echo nTime=$nTime  mapps to: ${zArr[*]}
# this function returns 3 type of values derived from the same 3-byte random int
myRandomF () {
    rndI=`od -A n -t d -N 3 /dev/random | tr -d ' '`
    # This is 3-byte truly random generator, max value: 256^3=16777216-1
    rndF=` echo $rndI | awk  '{printf "%.7f", $1/ 16777216 *2 -1. }'`
    #rnd1eps=` echo $rndF | awk  '{printf "%.7f", $1 * 0.1 }'`
    #echo rndI=$rndI rndF=$rndF rnd1eps=$rnd1eps
}



#OUTPUTS:

# STEP 1 - - - -   generate unique seed for MUSIC
myRandomF 
seed9=$rndI
core=ics_2018-12_b$rndI
musicTempl=ics_template.conf
#musicConf=${core}.conf
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
uOmega_b=$rndF

echo $uOmega_m $uSigma_8 $uN_spec $uOmega_b nTime=$nTime

#phys-params
Omega_m=` echo $uOmega_m | awk '{printf "%f", (1.+$1*0.20)* 0.5 }'` 
Omega_L=` echo $Omega_m | awk '{printf "%f", 1.-$1 }'` 
sigma_8=` echo $uSigma_8 | awk '{printf "%f", (1.+$1*0.20)* 0.75 }'` 
N_spec=`  echo $uN_spec  | awk '{printf "%f", (1.+$1*0.20)* 1.0 }'` 
Omega_b=` echo $uOmega_b | awk '{printf "%f", (1.+$1*0.20)* 0.045  }'` 

echo $Omega_m $Omega_L $sigma_8 $N_spec $Omega_b 
boxlength=512

# - - - - - -  create meta-data file
echo "date: "`date` > $ymlF
echo 'namePar: ' >> $ymlF
echo '- Omega_m ' >> $ymlF
echo '- sigma_8 ' >> $ymlF
echo '- N_spec ' >> $ymlF
echo '- Omega_b ' >> $ymlF


echo 'unitPar:' >> $ymlF
echo "- $uOmega_m" >> $ymlF
echo "- $uSigma_8" >> $ymlF
echo "- $uN_spec" >> $ymlF
echo "- $uOmega_b" >> $ymlF


echo 'physPar:' >> $ymlF
echo "- $Omega_m" >> $ymlF
echo "- $sigma_8" >> $ymlF
echo "- $N_spec" >> $ymlF
echo "- $Omega_b" >> $ymlF

echo "coreStr : $core" >> $ymlF
echo "boxlength : $boxlength" >> $ymlF
echo "seed9 : $seed9" >> $ymlF
echo "physOmega_m:  $Omega_m" >> $ymlF
echo "zList:  [${zArr[*]}]" >> $ymlF

# - - - - - -prepare SED edits
SEDINP=${outPath}/tmp.fix_${core}
echo "s/<boxlength>/$boxlength/g" >$SEDINP
echo "s/<seed9>/$seed9/g" >>$SEDINP
echo "s/<Omega_m>/$Omega_m/g" >>$SEDINP
echo "s/<sigma_8>/$sigma_8/g" >>$SEDINP
echo "s/<N_spec>/$N_spec/g" >>$SEDINP
echo "s/<Omega_b>/$Omega_b/g" >>$SEDINP
echo "s/<Omega_L>/$Omega_L/g" >>$SEDINP
#echo "s/<>/$/g" >>$SEDINP
echo "s|<musicHDF5>|$musicHDF5|g" >>$SEDINP

echo make new config with $musicTempl
cat $SEDINP
[ ! -f $musicTempl ] && { echo "$musicTempl file not found, abort"; exit 98; }
#cat  $musicTempl  |sed -f $SEDINP > ${outPath}/$musicConf


for (( iT=0; iT<$nTime; iT++ )); do
  zstart=${zArr[$iT]}
  echo prep iT=$iT  zstart=$zstart
  cat  $musicTempl  |sed -f $SEDINP  | sed "s/<zstart>/$zstart/g"> ${outPath}/${core}_${iT}.conf

done
exit

echo 'done Music '`date`

