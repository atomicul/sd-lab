#include "vector.h"

#include <iostream>

int main() {
    Vec<int> vec(3);

    vec[0] = 1;
    vec[1] = 2;
    vec[2] = 3;
    vec.push_back(4);

    for (size_t i{}; i<vec.size(); i++) {
        std::cout << vec[i] << " ";
    }
    std::cout << "\n";
}
