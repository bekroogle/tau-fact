#include <iostream>
#include <cstdlib>
#include <string>
#include "omp.h"



int main(int argc, char * argv[])
{
  double start = omp_get_wtime();
  std::string maxnum = argv[1];

  #pragma omp parllel for
  for (int i = 8; i < 23; i++) {
    std::string str = "python3 /home/ben/Documents/projects/tau-fact/tau-fact.py -t "+ std::to_string((long long)(i)) +" -m "+ maxnum;
    system(str.c_str());
    int threadid = omp_get_thread_num();
    if (threadid == 0) {
      std::cout << "Threads: " << omp_get_num_threads();
    }
  }



  double stop = omp_get_wtime();
  std::cout << stop - start << " seconds\n";
  return 0;
}
