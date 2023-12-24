#include "helper.cpp"
#include "gemm.cpp"
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <immintrin.h>
#include <cassert>

const char *input_dir = "input/sgemm/";
const char *verif_dir = "verification/sgemm/";

int main(int argc, char *argv[]){

	int num_files = 0; 
	char** names = get_files(input_dir, &num_files);

	long long min_mem, max_mem;
	arg_parse(argc, argv, &min_mem, &max_mem);

	/**
	 * sgemm Benchmark
	 * Params:		N, A, B, C
	 * Operation: 	C = A*B + C
	 */
	int M, N;
	long double main_score = 0;
	for(int i=0; i<num_files; i++){
		// Get test-data file
		char *filepath = get_filepath(input_dir, names[i]);
		FILE *file = fopen(filepath, "rb");
		char namebuf[1024];

		// Parse args
		float *A = get_farg(file, &M, &N);
		float *B = get_farg(file, &M, &N);
		float *C = get_farg(file, &M, &N);
		assert(N == M);
		float *CPY = (float*) aligned_alloc(64, getNextMultipleOf64(sizeof(float) * N * M));
		memcpy(CPY, C, N * M * sizeof(float));

		float memory = ((float) (M * N * 3) * sizeof(float));
		if(memory <= min_mem || memory >= max_mem) goto cleanup;
		memory /= (1024 * 1024);

		// Run Fast benchmark ----------------------------------------------------
		{
			sprintf(namebuf, "MyGemm: sgemm %d x %d, Memory: %f MB", M, N, memory);
			auto init = [&](){
				memcpy(C, CPY, N * M * sizeof(float));
				mem_flush(CPY, N * M * sizeof(float));
			};
		 	KernelInfo info = {2ull*N*N*N, 3ull*N*N*N * sizeof(float)};
		 	main_score += benchmark(my_gemm, init, info, 2, namebuf, N, A, B, C);
			printf("Verified:\t\t\t");
			if(fverify_benchmark(C, N*M, 1, verif_dir, names[i])) puts("Yes");
			else puts("No");
		}
		// ------------------------------------------------------------------------
		// Cleanup
		cleanup: 
		free(filepath);
		fclose(file);
		free(A);
		free(B);
		free(C);
		free(CPY);
	}

	for(int i=0; i<num_files; i++)
		free(names[i]);
	free(names);

	puts("");
	printf("Final score: %Lf\n", main_score);
}