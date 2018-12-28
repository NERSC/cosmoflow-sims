#!/bin/bash

set -u ;  # exit  if you try to use an uninitialized variable
set -e ;    #  bash exits if any statement returns a non-true return value
set -o errexit ;  # exit if any statement returns a non-true return value

pwd
musicConf=$1
outPath=$2
cd $outPath
pwd
MusicExe=/global/homes/b/balewski/prj/cosmoflow-sims/MUSIC/MUSIC
echo start MUSIC $musicConf ' '`date`
time $MusicExe ../$musicConf

echo 'done Music '`date`

