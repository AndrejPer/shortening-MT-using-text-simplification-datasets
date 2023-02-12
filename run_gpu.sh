qsub -l select=1:mem=16gb:scratch_local=10gb:ngpus=1:gpu_cap=cuda60:cuda_version=11.0 -q gpu -l walltime=4:00:00
singularity shell --nv /cvmfs/singularity.metacentrum.cz/NGC/TensorFlow\:21.03-tf2-py3.SIF

module add python/3.8.0-gcc
source ../env/bin/activate
pip install sacrebleu

python dataset.py
