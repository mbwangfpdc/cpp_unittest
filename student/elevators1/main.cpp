#include <iostream>
#include "header.h"

using std::cout;
using std::endl;

int main() {
    cls c;
    cout << "5 + 2 == " << c.add(5, 2) << endl;
    cout << "5 - 2 == " << c.subtract(5, 2) << endl;
    cout << "5 * 2 == " << c.multiply(5, 2) << endl;
    return 0;
}
