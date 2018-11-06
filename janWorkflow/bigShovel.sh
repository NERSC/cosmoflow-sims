#!/bin/sh
set -u ;  # exit  if you try to use an uninitialized variable
set -e ;    #  bash exits if any statement returns a non-true return value
set -o errexit ;  # exit if any statement returns a non-true return value


nSleep=1
n=0
date
outM=/global/cscratch1/sd/balewski/cosmoData_Jan3/meta/
for K in {1..50} ; do
    echo -n submit K=$K ' ' 
    cd /global/cscratch1/sd/balewski/cosmoUnivers2/10787415-${K}/out/
    #cd /global/cscratch1/sd/balewski/cosmoUnivers4/15954636-${K}/out/
    name1=`ls *conf`
    name2=cosmos_${name1/conf/meta.yaml}
    name0=cosmoMeta.yaml
    echo $name0 $name1 $name2
    cp $name0 $outM/$name2


    #./pack_tfrec.py --npzPath /global/cscratch1/sd/balewski/cosmoUnivers2/10787415-${K}//out/ -X --tfrPath /global/cscratch1/sd/balewski/cosmoData_JanX/
    n=$[ $n +1]
    #sleep $nSleep
done
date
echo sent $n jobs
