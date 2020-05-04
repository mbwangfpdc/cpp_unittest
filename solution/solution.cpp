#include "header.h"
int cls::add(int a, int b) {
    return a + b;
}

int cls::subtract(int a, int b) {
    return a - b;
}

int cls::multiply(int a, int b) {
    return a * b;
}

int cls::multiplyConstRef(const int& a, const int& b) {
    return a * b;
}
