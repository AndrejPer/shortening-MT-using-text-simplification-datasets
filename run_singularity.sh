#!/bin/bash
#PBS -N PyTorch_Job
#PBS -q gpu
#PBS -l select=1:ncpus=1:mem=16gb:scratch_local=16gb:ngpus=1
#PBS -l walltime=24:00:00
#PBS -m abe
#PBS -o z_output
#PBS -e z_error

singularity run --nv /cvmfs/singularity.metacentrum.cz/NGC/PyTorch\:20.09-py3.SIF bash /storage/praha1/home/andrejp/MT/shortening-MT-using-text-simplification-datasets/run.sh
