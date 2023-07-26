#!/bin/bash
# define a DATADIR variable: directory where the input files are taken from and where output will be copied to
DATADIR=/storage/praha1/home/andrejp/MT/shortening-MT-using-text-simplification-datasets
PYTHONPROG=model-train-pt.py
PROGDIR=./
echo "$PBS_JOBID is running on node `hostname -f` in a scratch directory $SCRATCHDIR" >> $DATADIR/jobs_info.txt
# load Python
module add python/3.8.0-gcc
# test if scratch directory is set
# if scratch directory is not set, issue error message and exit
test -n "$SCRATCHDIR" || { echo >&2 "Variable SCRATCHDIR is not set!"; exit 1; }

# copy input files to scratch directory
# if the copy operation fails, issue error message and exit
cp $DATADIR/$PROGDIR/$PYTHONPROG $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/opus_15838_1000000_l.en-sr-train.en $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/corrected.opus.en-sr-train.sr $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/opus.en-sr-test.en $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/corrected.opus.en-sr-test.sr $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/opus.en-sr-dev.en $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }
cp $DATADIR/opus-100/opus.en-sr-dev.sr $SCRATCHDIR || { echo >&2 "Error while copying input file(s)!"; exit 2; }

# move into scratch directory
cd $SCRATCHDIR

# run Python script
source $DATADIR/../env/bin/activate
python $PYTHONPROG || { echo >&2 "Calculation ended up erroneously (with a code $?) !!"; exit 3; }

# move the output to user's DATADIR or exit in case of failure
NEWDIR=results_just_train_L
[[ -d $DATADIR/$NEWDIR ]] || mkdir $DATADIR/$NEWDIR
cp -r ./* $DATADIR/$NEWDIR || { echo >&2 "Result file(s) copying failed (with a code $?) !!"; exit 4; }

# clean the SCRATCH directory
clean_scratch