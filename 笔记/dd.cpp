#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <sstream>
#include <string>
using namespace std;
const double EPSILON = 1e-9; 
double roundToPrecision(double value, int precision) {
    double factor = pow(10.0, precision);
    
    // 使用 std::floor 和 std::ceil 实现向零截断 (Truncation)
    if (value < 0) {
        // 负数使用 ceil (如 -9.27779 -> -9.2777)
        return ceil(value * factor) / factor;
    } else {
        // 正数使用 floor (如 9.27779 -> 9.2777)
        return floor(value * factor) / factor;
    }
}
int gaussianElimination(vector<vector<double>>& A, vector<double>& solution, int M, int N) {
    int pivot_row = 0; // 当前处理的主元行
    int rank = 0;      // 系数矩阵的秩

    // --- 步骤 2.1: 前向消元 (Forward Elimination) ---
    for (int k = 0; k < N && pivot_row < M; ++k) { 
        
        // 1. 列主元选择 (Partial Pivoting)
        int max_row = pivot_row;
        for (int i = pivot_row + 1; i < M; ++i) {
            if (abs(A[i][k]) > abs(A[max_row][k])) {
                max_row = i;
            }
        }
        // 交换行
        if (max_row != pivot_row) {
            swap(A[pivot_row], A[max_row]);
        }

        // 2. 检查主元
        if (abs(A[pivot_row][k]) < EPSILON) {
            continue; 
        }
        rank++;

        // 3. 消元操作
        for (int i = pivot_row + 1; i < M; ++i) {
            double factor = A[i][k] / A[pivot_row][k];
            for (int j = k; j <= N; ++j) {
                A[i][j] -= factor * A[pivot_row][j];
            }
        }
        pivot_row++; 
    }

    // --- 步骤 2.2: 判断解的状态 (秩分析) ---
    for (int i = pivot_row; i < M; ++i) {
        if (abs(A[i][N]) > EPSILON) {
            return 1; // error1: 无解 (0 = 非零数)
        }
    }
    
    if (rank < N) {
        return 2; // error2: 无穷多解
    }
    
    // --- 步骤 2.3: 回代法 (Back Substitution) ---
    solution.assign(N, 0.0);
    
    for (int i = N - 1; i >= 0; --i) {
        int p_row = i; 
        
        if (abs(A[p_row][i]) < EPSILON) {
             return 2; 
        }

        double sum = 0.0;
        for (int j = i + 1; j < N; ++j) {
            sum += A[p_row][j] * solution[j];
        }

        solution[i] = (A[p_row][N] - sum) / A[p_row][i];
    }

    return 0; // 唯一解
}
string formatSolution(double value) {
    // 1. 使用截断（或四舍五入）到小数点后4位
    double final_value = roundToPrecision(value, 4); // 注意：函数名仍为 roundToPrecision，但内部已是截断逻辑

    // 2. 判断是否是整数
    if (abs(final_value - round(final_value)) < EPSILON) {
        // 如果非常接近整数，直接输出整数形式
        return to_string((long long)round(final_value));
    } else {
        // 3. 浮点数格式化：强制 4 位小数，然后去除尾随零
        stringstream ss;
        // 强制固定4位小数
        ss << fixed << setprecision(4) << final_value;
        string s = ss.str();

        // 查找小数点位置
        size_t dot_pos = s.find('.');
        if (dot_pos == string::npos) {
            return s;
        }

        // 从末尾开始删除尾随的 '0'
        size_t last_char = s.size() - 1;
        while (last_char > dot_pos && s[last_char] == '0') {
            last_char--;
        }

        // 如果删除 '0' 后，最后一个字符是小数点，则也删除它
        if (s[last_char] == '.') {
            last_char--;
        }

        // 返回截断后的字符串
        return s.substr(0, last_char + 1);
    }
}

int main() {
    
    vector<vector<double>> A;
    string line;
    int N = -1; 
    int M = 0;  
    
    // --- 步骤 3.1: 读取输入，构建矩阵 A ---
    while (getline(cin, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        double coeff;
        vector<double> current_equation;

        while (ss >> coeff) {
            current_equation.push_back(coeff);
        }

        if (current_equation.empty()) continue;

        if (M == 0) {
            N = current_equation.size() - 1;
        } else if (current_equation.size() - 1 != N) {
            return 1; // 输入格式错误
        }
        
        A.push_back(current_equation);
        M++;
    }

    if (M == 0 || N <= 0) {
        return 0;
    }
    
    // --- 步骤 3.2: 调用求解器 ---
    vector<double> solution;
    int result_code = gaussianElimination(A, solution, M, N);

    // --- 步骤 3.3: 输出结果 ---
    switch (result_code) {
        case 0: { // 唯一解
            for (int i = 0; i < N; ++i) {
                // 使用 formatSolution 函数处理输出格式
                cout << formatSolution(solution[i]);
                
                // 输出分隔符
                if (i != N - 1) {
                    cout << " ";
                }
            }
            cout << endl;
            break;
        }
        case 1: // 无解
            cout << "error1" << endl;
            break;
        case 2: // 无穷多解
            cout << "error2" << endl;
            break;
    }

    return 0;
}