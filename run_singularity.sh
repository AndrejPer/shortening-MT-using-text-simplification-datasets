#!/bin/bash
#PBS -N train_trans_S
#PBS -q gpu
#PBS -l select=1:ncpus=1:mem=200gb:scratch_local=200gb:ngpus=1
#PBS -l walltime=15:00:00
#PBS -m abe

export PYTHONUSERBASE=/storage/praha1/home/andrejp/PUB-PyTorch21.11
singularity exec --nv -B $SCRATCHDIR /cvmfs/singularity.metacentrum.cz/NGC/PyTorch\:21.11-py3.SIF /storage/praha1/home/andrejp/MT/shortening-MT-using-text-simplification-datasets/run.sh