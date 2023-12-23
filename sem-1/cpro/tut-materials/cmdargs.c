#include <stdio.h>

int main(int argc, char **argv)
{
  printf("First argument is: %s\n", argv[0]);
  char message[] = "hello";
  printf("%s ", message);
  for(int i = 1; i < argc; i++)
      printf("%s ", argv[i]);
  printf("\n");
  return 0;
}
