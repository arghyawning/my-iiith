#include <ctime>
#include <cstdio>
#include <cstdlib>
#include <cstdbool>
#include <cstring>
#include <dirent.h> 
#include <immintrin.h>
#include <cmath>
#include <iostream>
#include <chrono>
#include <unistd.h>
#include <getopt.h>
#include <climits>
#include <cctype>

/**
 * @member 	result - The result of the FLOPS computed by the kernel
 * @member	flop_ct - The total number of FLOPS computed by the kernel
 * @member 	mem_accesses - The total number of memory accesses made by the kernel
 */
typedef struct Result{
	double result;
	uint64_t flop_ct;
	uint64_t mem_accesses;
} Result;

/**
 * @member 	iters - The total number of loop iterations to be done
 * @member 	input - Any input data that is to be sent to the kernel, can be casted to anything
 */
typedef struct KernelInfo{
	uint64_t flops, mem_accesses;
} KernelInfo;

/**
 * Returns the current CPU clock time in seconds
 * @param  tinfo - timespec struct pointing to alloc'd memory
 */
long double tick_tock(){
	using Clock = std::chrono::high_resolution_clock;
    auto t1 = Clock::now();
    std::chrono::nanoseconds ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1.time_since_epoch());
    long double nanoseconds = static_cast<long double>(ns.count());
	return nanoseconds * 1e-9;
}

/**
 * Outputs details about the precision of the clocks on the system and other useful hardware spec 
 * information
 */
void output_hwinfo(){
	struct timespec *info = (struct timespec*) malloc(sizeof(struct timespec));
	
	for(int i=0; i<60; i++) printf("-");
	puts("\nHardware timer resolution information: ");
	for(int i=0; i<60; i++) printf("-");
	
	clock_getres(CLOCK_REALTIME, info);
	printf("\nReal time clock: \t\t%.9Lf sec\n", (long double) info->tv_sec + info->tv_nsec * 1e-9);
	clock_getres(CLOCK_MONOTONIC, info);
	printf("Monotonic clock: \t\t%.9Lf sec\n", (long double) info->tv_sec + info->tv_nsec * 1e-9);
	clock_getres(CLOCK_PROCESS_CPUTIME_ID, info);
	printf("Per-process CPU clock: \t\t%.9Lf sec\n", (long double) info->tv_sec + info->tv_nsec * 1e-9);
	clock_getres(CLOCK_THREAD_CPUTIME_ID, info);
	printf("Per-thread CPU clock: \t\t%.9Lf sec\n\n", (long double) info->tv_sec + info->tv_nsec * 1e-9);
	free(info);
}

/**
 * Pretty prints the result returned by a benchmark
 * @param st - The start time of the benchmark
 * @param en - The end time of the benchmark
 * @param ret - The result obtained by the benchmark over all runs
 */
void pretty_print(long double duration, Result ret){
	printf("\nTotal runtime:\t\t\t%Lf\n", duration);
	printf("Result computed:\t\t%lf\n", ret.result);
	printf("Total FLOPS computed:\t\t%lu\n", ret.flop_ct);
	printf("Total memory accesses:\t\t%lu\n", ret.mem_accesses);
	printf("\nScore:\t\t\t\t%Lf\n", (long double) ret.flop_ct / duration * 1e-6);
	printf("Bandwidth:\t\t\t%Lf GB/s\n\n", (long double) ret.mem_accesses / duration * 1e-9);
}

/**
 * Pretty prints only the GFLOPS & Bandwidth info returned by a benchmark
 * @param st - The start time of the benchmark
 * @param en - The end time of the benchmark
 * @param ret - The result obtained by the benchmark over all runs
 */
void compressed_pretty_print(long double duration, Result ret){
	printf("\nScore:\t\t\t\t%Lf\n", (long double) ret.flop_ct / duration * 1e-6);
	printf("Bandwidth:\t\t\t%Lf GB/s\n", (long double) ret.mem_accesses / duration * 1e-9);
}

/**
 * Given some kernel which takes in `args` as params, it runs the kernel repeatedly until a minimum of 
 * `duration` seconds has passed and outputs the GFLOPS/sec achieved by the kernel and other bench info.
 * This is first done on a single thread, then run again over all threads. Information for both tests 
 * is included in the final output.
 * @param 	kernel - A kernel to benchmark
 * @param 	args - The arguments to be passed to the kernel
 * @param 	duration - The minimum amount of time to run the kernel for
 * @param 	name - The name / header to display when outputting benchmark details
 */
template<typename F, typename I, typename... Args>
long double benchmark(F kernel, I reset, KernelInfo info, long double duration, char *name, Args... args){
	// Single thread run
	for(int i=0; i<60; i++) printf("-");
	printf("\nBenchmark - %s\n", name);
	for(int i=0; i<60; i++) printf("-");

	Result ret = {0.0, 0, 0};
	long double min_duration = duration;
	long double runtime = 0, st, en;

	int iters = 0;
	do {
		ret.flop_ct += info.flops;
		ret.mem_accesses += info.mem_accesses;
		reset();
		st = tick_tock();
		kernel(args...);
		en = tick_tock(); 
		runtime += en - st;
		iters++;
	} while(runtime < min_duration);
	pretty_print(runtime, ret);
	return ((long double) ret.flop_ct / duration * 1e-6);
}

/** Intel recommended method to flush the cache */
void mem_flush(const void *p, unsigned int allocation_size){
    const size_t cache_line = 64;
    const char *cp = (const char *)p;
    size_t i = 0;
    if (p == NULL || allocation_size <= 0)
            return;
    for (i = 0; i < allocation_size; i += cache_line) {
            asm volatile("clflush (%0)\n\t" : : "r"(&cp[i]) : "memory");
    }
    asm volatile("sfence\n\t" : : : "memory"); // Really cool instruction
}

static void escape(void *p){
	asm volatile("" : : "g"(p) : "memory");
}

void fill_cache(const char *p, int allocation_size){
	// Cleanup
	for(int i=0; i < allocation_size; i++) {
		char t = p[i];
		escape(&t);
	}
}

/**
 * Concatenate the directory path with filename to generate full 
 * path string.
 * @param  path  Directory path
 * @param  fname File name
 * @return       Pointer to string containing full path string
 */
char *get_filepath(const char *path, const char *fname){
	int plen = strlen(path);
	int flen = strlen(fname);
	char *file_path = (char*) malloc(sizeof(char) * (plen + flen + 1));
	memcpy(file_path, path, sizeof(char) * (plen + 1));
	strcat(file_path, fname);
	return file_path;
}

uint64_t getNextMultipleOf64(uint64_t n) {
    return ((n + 63) >> 6) << 6;
}


/**
 * Parse the input file to get one matrix argument and move fptr to
 * the next argument if any. _n and _m will contain the dimensions of 
 * the argument read if _n and _m are not NULL.
 * 
 * Expected input file format:
 * [int n, int m, contiguous allocation of n*m single-precision numbers]
 */
float* get_farg(FILE *fptr, int *_n, int *_m){
	int n, m, read;
	read = fread(&n, sizeof(int), 1, fptr);
	
	if(!read) return NULL;

	fread(&m, sizeof(int), 1, fptr);
	int help = getNextMultipleOf64(sizeof(float) * n * m);
	float *data = (float*) aligned_alloc(64, getNextMultipleOf64(sizeof(float) * n * m));
	fread(data, sizeof(float), n * m, fptr);
	if(_n) *_n = n;
	if(_m) *_m = m;
	return data;
}

/**
 * Single precision version
 * Given the resultant of some computation and the file containing the data to be 
 * verified against, check if the result matches with check data. 
 * @param  result Data to check
 * @param  n, m   Dimensions of data element
 * @param  dir    Directory containing verification data
 * @param  bench  Name of benchmark
 * @return        True if verified else false
 */
bool fverify_benchmark(float *result, int n, int m, const char *dir, const char *bench){
	char *filepath = get_filepath(dir, bench);
	FILE *fptr = fopen(filepath, "rb");

	float *check = (float*) malloc(sizeof(float) * n * m);
	int read = fread(check, sizeof(float), n*m, fptr);

	bool valid = (read == n * m);
	float eps = 1.0;
	for(int i=0; i<n*m; i++)
		valid &= (fabsf(check[i] - result[i]) < eps);

	fclose(fptr);
	free(filepath);
	free(check);

	return valid;
}

#define ISFILE(X) (strcmp(X, ".") != 0 && strcmp(X, "..") != 0)

/**
 * Comparator to compare two integers stored in string form in ascending
 * order. If a string containing a non-integer is passed it is considered 0. 
 */
int cmp_func(const void *a, const void *b){
	long a_i = strtol(*((char**) a), NULL, 10);
	long b_i = strtol(*((char**) b), NULL, 10);
	return a_i > b_i;
}

/**
 * Memory version of strdup, return a pointer to memory containing duplicated
 * data from src upto `bytes` number of bytes.
 */
void *memdup(void *src, size_t bytes){
	void *ret = aligned_alloc(64, bytes);
	if(!ret) return ret;
	memcpy(ret, src, bytes);
	return ret;
}

/**
 * Given the path to the directory, returns a pointer to a sorted array of 
 * char*'s each of which point to the name of a file in the directory
 * @param  path	The directory path
 * @param  n    Pointer to a variable which will be set to the number
 *              of files in the directory
 * @return      Pointer to sorted char* array containing file names
 */
char** get_files(const char *path, int *n){
	DIR *d; 
	d = opendir(path);
	struct dirent *dir; 
  	
  	int file_count = 0;
	for(;(dir = readdir(d)) != NULL; file_count += ISFILE(dir->d_name));
	
	closedir(d);
	d = opendir(path);

	char **names = (char**) malloc(sizeof(char*) * file_count);
	for(int i=0; (dir = readdir(d)) != NULL;){
		if(ISFILE(dir->d_name)) {
			int len = strlen(dir->d_name);
			names[i] = (char*) malloc(sizeof(char) * (len + 1));
			memcpy(names[i], dir->d_name, sizeof(char) * (len + 1));
			i++;
		}
	}
	closedir(d);
	qsort(names, file_count, sizeof(char*), cmp_func);
	*n = file_count;
	return names;
}

long long byte_parse(char *cptr){
	long long num, mult=1;
	char *eptr;
	num = strtol(cptr, &eptr, 10);
	for(char *c=eptr; *c; c++) *c = tolower(*c);
	
	if(strcmp(eptr, "kb") == 0) mult = 1000;
	else if(strcmp(eptr, "kib") == 0) mult = 1024;
	else if(strcmp(eptr, "mb") == 0) mult = 1000*1000;
	else if(strcmp(eptr, "mib") == 0) mult = 1024*1024;
	else if(strcmp(eptr, "gb") == 0) mult = 1000*1000*1000;
	else if(strcmp(eptr, "gib") == 0) mult = 1024*1024*1024;
	else if(strlen(eptr) != 0) { 
		puts("Incorrect parameters passed");
		exit(1);
	}

	return num*mult;
}

void arg_parse(int argc, char *argv[], long long *min_mem, long long *max_mem){
	long long min = 0, max = LLONG_MAX;
	static struct option long_options[] = {
		{"min", required_argument, 0, 'l'},
		{"max",   required_argument, 0, 'r'},
		{0, 0, 0, 0}
	}; 
	int option_index, c;
	while ((c = getopt_long(argc, argv, "l:r:", long_options, &option_index)) != -1){
		switch (c){
			// Long argument
			case 0:
				if(option_index == 0 && optarg) min = byte_parse(optarg);
				else if(option_index == 1 && optarg) max = byte_parse(optarg);
			break;

			case 'l':
				if(optarg) min = byte_parse(optarg);
			break;

			case 'r':				
				if(optarg) max = byte_parse(optarg);
			break;

			default:
				puts("Usage ./<program_name> --min [number][/KB/MB/GB] --max [number][/KB/MB/GB]");
				exit(1);
        }
    }
    *min_mem = min;
    *max_mem = max;
    printf("min: %lld, max: %lld\n", min, max);
}
