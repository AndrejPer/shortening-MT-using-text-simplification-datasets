#!/bin/bash
#PBS -N runScript
#PBS -l select=1:ncpus=2:mem=4gb:scratch_local=10gb
#PBS -l walltime=10:00:00
#PBS -m abe
#PBS -o z_hardware
#PBS -e z_time

# define a DATADIR variable: directory where the input files are taken from and where output will be copied to
DATADIR=/storage/praha1/home/andrejp/MT/shortening-MT-using-text-simplification-datasets # substitute username and path to to your real username and path

# append a line to a file "jobs_info.txt" containing the ID of the job, the hostname of node it is run on and the path to a scratch directory
# this information helps to find a scratch directory in case the job fails and you need to remove the scratch directory manually
echo "$PBS_JOBID is running on node `hostname -f` in a scratch directory $SCRATCHDIR" >> $DATADIR/jobs_info.txt

#loads Python
module add python/3.8.0-gcc

# test if scratch directory is set
# if scratch directory is not set, issue error message and exit
test -n "$SCRATCHDIR" || { echo >&2 "Variable SCRATCHDIR is not set!"; exit 1; }

# copy input file "h2o.com" to scratch directory
# if the copy operation fails, issue error message and exit
cp $DATADIR/opus-100/opus.en-sr-train.en  $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }

# move into scratch directory
cd $SCRATCHDIR

# run dataset script
source ../env/bin/activate
python dataset.py --num_processors 100 || { echo >&2 "Calculation ended up erroneously (with a code $?) !!"; exit 3; }

# move the output to user's DATADIR or exit in case of failure
cp dataset.out $DATADIR/ || { echo >&2 "Result file(s) copying failed (with a code $?) !!"; exit 4; }

# clean the SCRATCH directory
clean_scratch