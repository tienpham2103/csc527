/*********************************
 *	Author: Tien Pham        *
 *	Homework 1 - CSC 527     *
 *********************************/

#include <iostream>
#include <cstdlib>
#include <vector>

int main() {
	bool cont = true;
	while (cont) {
		std::vector<int> xVals;
		for (int i = 1; i <= 5; i++) {
			int x = 0;
			std::cout << "Value for x" << i << ": ";
			std::cin >> x;
			xVals.push_back(x);
		}
		int bk = 0;
		std::cout << "Value for bk: ";
		std::cin >> bk;
		int yk = 0;
		int sum = 0;
		for (int i = 1; i <= 5; i++) {
			sum += xVals[i-1];
		}
		if (sum + bk >=0)
			std::cout << "yk = 1" << std::endl;
		else std::cout << "yk = 0" << std::endl;
		char prompt;
		std::cout << "Do you want to continue? (Y/N)";
		std::cin >> prompt;
		if (prompt == 'N' || prompt == 'n')
			cont = false;
	}
}
