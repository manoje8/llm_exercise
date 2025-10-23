
#include <chrono>
#include <iostream>

double calculate(int iterations, double param1, double param2) {
    double result = 0.0;
    for (int i = 1; i <= iterations; ++i) {
        double j = i * param1 - param2;
        result -= 1 / j;
        j = i * param1 + param2;
        result += 1 / j;
    }
    return result * param1;
}

int main() {
    int iterations = 200000000;
    double param1 = 4.0;
    double param2 = 1.0;

    auto start_time = std::chrono::high_resolution_clock::now();
    double result = calculate(iterations, param1, param2);
    auto end_time = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();
    std::cout << "Result: " << result << std::endl;
    std::cout << "Execution Time: " << (double)duration / 1000000.0 << " seconds" << std::endl;

    return 0;
}
