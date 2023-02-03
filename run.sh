#!/bin/bash
#PBS -N runScript
#PBS -l select=1:ncpus=2:mem=4gb:scratch_local=10gb
#PBS -l walltime=10:00:00
#PBS -m abe
#PBS -o z_hardware
#PBS -e z_time

# define a DATADIR variable: directory where the input files are taken from and where output will be copied to
DATADIR=/storage/praha1/home/andrejp/MT/shortening-MT-using-text-simplification-datasets

echo "$PBS_JOBID is running on node `hostname -f` in a scratch directory $SCRATCHDIR" >> $DATADIR/jobs_info.txt

# load Python
module add python/3.8.0-gcc

# test if scratch directory is set
# if scratch directory is not set, issue error message and exit
test -n "$SCRATCHDIR" || { echo >&2 "Variable SCRATCHDIR is not set!"; exit 1; }

# copy input files to scratch directory
# if the copy operation fails, issue error message and exit
cp $DATADIR/opus-100/opus.en-sr-train.en  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/dataset.py  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/sorted_ppdb_small.csv  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }

# move into scratch directory
cd $SCRATCHDIR

# run dataset script
source $DATADIR/../env/bin/activate
python dataset.py --num_rules 100 || { echo >&2 "Calculation ended up erroneously (with a code $?) !!"; exit 3; }

# move the output to user's DATADIR or exit in case of failure
cp opus_100_1000000.en-sr-train.en $DATADIR/ || { echo >&2 "Result file(s) copying failed (with a code $?) !!"; exit 4; }

# clean the SCRATCH directory
clean_scratch