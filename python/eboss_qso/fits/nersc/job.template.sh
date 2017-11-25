#!/bin/bash

#SBATCH -p {{ partition }}
#SBATCH -J {{ job }}.{{ cores }}
#SBATCH -o {{ output_file }}
#SBATCH -N {{ nodes }}
#SBATCH -t {{ time }}
{{ haswell_config }}

cd $EBOSS_DIR

# activate environment
source /usr/common/contrib/bccp/conda-activate.sh 3.6

# install correct nbodykit version to computing nodes
bcast-pip python
bcast $TAR_DIR/$NERSC_HOST/pyRSD.tar.gz

cd $SLURM_SUBMIT_DIR

# call run-tests with desired number of cores
echo ===== Running with {{ cores }} cores =====
srun -n {{ cores }} {{ command }}
