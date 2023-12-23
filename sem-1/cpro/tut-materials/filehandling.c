// Read numbers from a file and output the largest number present in the file
// Read the file name as arguments from the command line
// You dont know how many numbers will be there in the file
// Constraint: all the numbers are >= 0
#include <stdio.h>

int main(int argc, char **argv)
{
  if (argc != 3)
  {
    printf("Usage: ./a.out <input file> <output file>");
    return 0;
  }
  FILE* fileptr = fopen(argv[1], "r");
  int maximum_number = -199;
  while(1)
  {
    int val_here;
    int retval = fscanf(fileptr, "%d", &val_here);
    if(retval == -1)
        break;
    if(maximum_number < val_here)
      maximum_number = val_here;
  }
  FILE *outputFile = fopen(argv[2], "a");
  fprintf(outputFile, "%d\n", maximum_number);
  return 0;
}
