#!/bin/bash
#PBS -N PyTorch_Job
#PBS -q gpu
#PBS -l select=1:ncpus=1:mem=16gb:scratch_local=16gb:ngpus=1
#PBS -l walltime=24:00:00
#PBS -m abe
#PBS -o z_output
#PBS -e z_error

export PYTHONUSERBASE=/storage/praha1/home/andrejp/PUB-PyTorch21.11

singularity exec --nv -B /scratch/cvmfs/singularity.metacentrum.cz/NGC/PyTorch\:21.11-py3.SIF /storage/praha1/home/andrejp/MT/shortening-MT-using-text-simplification-datasets/run.sh