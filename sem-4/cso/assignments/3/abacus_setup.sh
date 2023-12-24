mkdir input
mkdir input/sgemm
mkdir verification
mkdir verification/sgemm
module load gcc/12.2.0
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/global/gcc-12/lib64
g++ gen.cpp -o gen -std=c++17 -Ofast -march=native
./gen