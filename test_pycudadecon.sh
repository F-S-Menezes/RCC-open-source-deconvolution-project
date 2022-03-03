#!/bin/bash
#SBATCH --job-name=test_pyducadecon
#SBATCH --output=test.out
#SBATCH --error=test.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4800
#SBATCH --tasks-per-node=1
#SBATCH --hint nomultithread # Hyperthreading disabled
#SBATCH --gres=gpu:tesla:1
module load singularity
module load cuda-10.0.130-gcc-4.8.5-kqvlz4i
printf "\nbeginning conda_base tests\n"
printf "test otf creation"
singularity exec --nv /scratch/rcc/uqfmenze/conda_base.sif python3 tiff_process.py -p /scratch/rcc/uqfmenze/good_psf.tif

printf "test single file processing"
singularity exec --nv /scratch/rcc/uqfmenze/conda_base.sif python3 tiff_process.py -t  /scratch/rcc/uqfmenze/1test.tiff --otf pycudadecon_output/otf.tif

printf "test folder processing"
singularity exec --nv /scratch/rcc/uqfmenze/conda_base.sif python3 tiff_process.py -f '/scratch/rcc/uqfmenze/test-data/*.tiff' --otf pycudadecon_output/otf.tif

printf "finished conda_base tests, beginning nvidia_base tests "

printf "test otf creation"
singularity exec --nv /scratch/rcc/uqfmenze/nvidia_base.sif python3 tiff_process.py -p /scratch/rcc/uqfmenze/good_psf.tif

printf "test single file processing"
singularity exec --nv /scratch/rcc/uqfmenze/nvidia_base.sif python3 tiff_process.py -t  /scratch/rcc/uqfmenze/1test.tiff --otf pycudadecon_output/otf.tif

printf "test folder processing"
singularity exec --nv /scratch/rcc/uqfmenze/nvidia_base.sif python3 tiff_process.py -f '/scratch/rcc/uqfmenze/test-data/*.tiff' --otf pycudadecon_output/otf.tif

printf "finished all tests"
