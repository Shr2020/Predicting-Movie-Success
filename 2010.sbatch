#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=12
#SBATCH --time=24:00:00
#SBATCH --mem=64GB
#SBATCH --job-name=s2010
#SBATCH --output=%x.out


module purge

singularity exec --nv \
		    --overlay /scratch/sj3409/pytorch-example/my_pytorch.ext3:ro \
		    	    /scratch/work/public/singularity/cuda11.2.2-cudnn8-devel-ubuntu20.04.sif \
			    	    /bin/bash -c "source /ext3/env.sh; cd /scratch/sj3409/BDSProject; python sent_analysis_2500.py --year=2010"
