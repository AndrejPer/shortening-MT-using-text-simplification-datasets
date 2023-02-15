#!/bin/bash
#PBS -N PyTorch_Job
#PBS -q gpu
#PBS -l select=1:ncpus=1:mem=10gb:scratch_local=10gb:ngpus=1
#PBS -l walltime=24:00:00
#PBS -m abe
#PBS -o z_output
#PBS -e z_error

# define a DATADIR variable: directory where the input files are taken from and where output will be copied to
DATADIR=/storage/praha1/home/andrejp/MT/shortening-MT-using-text-simplification-datasets

# copy input files to scratch directory
# if the copy operation fails, issue error message and exit
cp $DATADIR/opus-100/opus_7007_1000000.en-sr-train.en  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/opus.en-sr-train.sr  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/opus.en-sr-test.en  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/opus.en-sr-test.sr  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/opus.en-sr-dev.en  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/opus.en-sr-dev.sr  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/model-train-pt.py  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }

# move into scratch directory
cd $SCRATCHDIR

# run dataset script
singularity run --nv /cvmfs/singularity.metacentrum.cz/NGC/PyTorch\:20.09-py3.SIF
module add python/3.8.0-gcc
source $DATADIR/../env/bin/activate

python $DATADIR/model-train.py || { echo >&2 "Calculation ended up erroneously (with a code $?) !!"; exit 3; }

# move the output to user's DATADIR or exit in case of failure
cp ./* $DATADIR/results || { echo >&2 "Result file(s) copying failed (with a code $?) !!"; exit 4; }

# clean the SCRATCH directory
clean_scratch



