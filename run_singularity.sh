#!/bin/bash
#PBS -N trans_raw
#PBS -l select=1:ncpus=1:mem=128gb:scratch_local=128gb
#PBS -l walltime=8:00:00
#PBS -m abe

export PYTHONUSERBASE=/storage/praha1/home/andrejp/PUB-PyTorch21.11
singularity exec --nv -B $SCRATCHDIR /cvmfs/singularity.metacentrum.cz/NGC/PyTorch\:21.11-py3.SIF /storage/praha1/home/andrejp/MT/shortening-MT-using-text-simplification-datasets/run.sh