//  gcc -o lexical lexical.c
// ./lexical
// This demonstrates why lexical closures do NOT work in GNU C.

#include <stdio.h>

typedef int (*f)(int);

f plus(int x) {
  int internal(int y) {
    return x+y;
  }
  return &internal;
}

int main(void) {
  printf("%d\n", plus(3)(4));
  printf("%d\n", plus(5)(4));
  printf("%d\n", plus(9)(10));
  f add3 = plus(3);
  f add5 = plus(5);
  f add9 = plus(9);
  printf("%d\n", add3(4));
  printf("%d\n", add5(4));
  printf("%d\n", add9(10));
}
