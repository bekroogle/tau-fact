#ifndef NUMBER_H
#define NUMBER_H
#include <vector>
#include "factorization.h"

class Number
{
  public:
    Number(name);
    virtual ~Number();
    void addFactorization(Factorization);
  protected:
  private:
    int name;
    vector<Factorization> factorizations;

};

#endif // NUMBER_H
