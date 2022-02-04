#!/bin/bash
#SBATCH --job-name=test_pyducadecon
#SBATCH --output=test1.out
#SBATCH --error=test1.err
#SBATCH --mail-user=uqhngu36@uq.edu.au
#SBATCH --mail-type=END
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4800
#SBATCH --tasks-per-node=1
#SBATCH --hint nomultithread # Hyperthreading disabled
#SBATCH --gres=gpu:tesla:1
module load singularity
module load cuda-10.0.130-gcc-4.8.5-kqvlz4i
echo "begin test driver cuda-10.0.130-gcc-4.8.5-kqvlz4i"
#nvidia-smi
singularity exec --nv /scratch/rcc/uqhngu36/conda_base.sif python3 tiff_deskew.py 1test.tiff
#singularity exec --nv /scratch/rcc/uqfmenze/nvidia_base.sif nvidia-smi
echo "end test"
