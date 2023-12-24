mkdir input
mkdir input/sgemm
mkdir verification
mkdir verification/sgemm
g++ gen.cpp -o gen -std=c++17 -Ofast -march=native
./gen