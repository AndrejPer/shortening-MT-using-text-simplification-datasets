qsub -q gpu -l select=2:ngpus=2:gpu_mem=1gb:scratch_local=10gb -l walltime=1:00:00

module add python/3.8.0-gcc

python -m venv env

source env/bin/activate

python dataset.py --num_sentences 5 --num_rules 5
