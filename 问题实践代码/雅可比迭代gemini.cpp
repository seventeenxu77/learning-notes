#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <sstream>
#include <string>

using namespace std;

const double EPSILON = 1e-9;
const double EPSILON_JACOBI = 1e-6; // 雅可比法的收敛精度
const int MAX_ITERATIONS = 1000;    // 雅可比法的最大迭代次数

// --- 浮点数格式化函数 (保留您的截断逻辑) ---
double roundToPrecision(double value, int precision) {
    double factor = pow(10.0, precision);
    if (value < 0) {
        return ceil(value * factor) / factor;
    } else {
        return floor(value * factor) / factor;
    }
}
string formatSolution(double value) {
    double final_value = roundToPrecision(value, 4);
    if (abs(final_value - round(final_value)) < EPSILON) {
        return to_string((long long)round(final_value));
    } else {
        stringstream ss;
        ss << fixed << setprecision(4) << final_value;
        string s = ss.str();
        size_t dot_pos = s.find('.');
        if (dot_pos == string::npos) return s;
        size_t last_char = s.size() - 1;
        while (last_char > dot_pos && s[last_char] == '0') last_char--;
        if (s[last_char] == '.') last_char--;
        return s.substr(0, last_char + 1);
    }
}

// --- 雅可比迭代法求解函数 ---
double vectorNorm(const vector<double>& x_new, const vector<double>& x_old) {
    double max_diff = 0.0;
    for (size_t i = 0; i < x_new.size(); ++i) {
        double diff = abs(x_new[i] - x_old[i]);
        if (diff > max_diff) max_diff = diff;
    }
    return max_diff;
}

// 注意：此函数假定输入矩阵 A_aug 已经是方阵且经过高斯消元后是可解的
int jacobiIteration(const vector<vector<double>>& A_aug, vector<double>& sol, int N) {
    sol.assign(N, 0.0);
    vector<double> x_old = sol;
    vector<double> x_new(N);

    // 雅可比迭代必须基于原始（未消元）的矩阵才能保证收敛性。
    // 但是在这个混合模型中，我们假设高斯消元后的矩阵仍然可以被迭代求解，
    // 否则我们将面临收敛性问题。我们按要求进行迭代，并检查对角线。
    
    for (int i = 0; i < N; ++i) {
        if (abs(A_aug[i][i]) < EPSILON) {
            // 对角线为零，无法迭代
            return 2; 
        }
    }

    for (int k = 0; k < MAX_ITERATIONS; ++k) {
        // 计算 x(k+1)
        for (int i = 0; i < N; ++i) {
            double sum = 0.0;
            // 回代过程，使用所有其他旧值 x_old[j]
            for (int j = 0; j < N; ++j) {
                if (i != j) {
                    sum += A_aug[i][j] * x_old[j];
                }
            }
            // 公式：x_i^(k+1) = (b_i - sum) / a_ii
            x_new[i] = (A_aug[i][N] - sum) / A_aug[i][i];
        }

        // 检查收敛条件
        if (vectorNorm(x_new, x_old) < EPSILON_JACOBI) {
            sol = x_new;
            return 0; // 收敛
        }

        x_old = x_new;
    }

    // 超过最大迭代次数
    return 1; // 视为不收敛/无解
}


// --- 高斯消元预处理函数 (只负责消元和秩分析) ---
// 返回值：1: error1, 2: error2, 0: 唯一解 (需要回代/迭代)
int preProcess(vector<vector<double>>& matrix, int m, int n, int& rank) {
    int pivot_row = 0;
    rank = 0;
    
    // 前向消元
    for(int i=0; i<n && pivot_row < m; i++){
        int max_row = pivot_row;
        // 列主元选择
        for(int j=pivot_row+1; j<m; j++){
            if(abs(matrix[j][i]) > abs(matrix[max_row][i])){
                max_row = j;
            }
        }
        if(pivot_row != max_row){
            swap(matrix[pivot_row], matrix[max_row]);
        }
        
        if(abs(matrix[pivot_row][i]) < EPSILON) continue;
        
        rank++;
        // 消元
        for(int j=pivot_row+1; j<m; j++){
            double factor = matrix[j][i] / matrix[pivot_row][i];
            for(int k=i; k<=n; k++){
                matrix[j][k] -= factor * matrix[pivot_row][k];
            }
        }
        pivot_row++;
    }
    
    // 秩分析：
    // 1. 无解 (error1): 零行 = 非零常数
    for(int j=pivot_row; j<m; j++){
        if(abs(matrix[j][n]) > EPSILON) return 1;
    }
    
    // 2. 无穷多解 (error2): 秩 < 变量数
    if(rank < n) return 2;
    
    // 3. 唯一解：秩 = 变量数 (但可能 M > N，多余方程是零行)
    return 0;
}


// --- 主函数 ---
int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string line;
    vector<vector<double>> matrix;
    vector<double> sol;
    double num;
    int n=0, m=0;
    
    // 输入处理 (保持不变)
    while(getline(cin,line)){
        if(line.empty())continue;
        vector<double> equa;
        stringstream ss(line);
        while(ss>>num) equa.push_back(num);
        if(equa.empty())continue;
        if(m==0){
            n=equa.size()-1;
            if(n<=0) return 1; 
        }else{
            if(equa.size()-1!=n)return 1;
        }
        matrix.push_back(equa);
        m++;
    }
    
    if (m == 0 || n <= 0) return 0;
    
    int rank = 0;
    int resultcode = preProcess(matrix, m, n, rank);
    
    // 1. 高斯消元法处理非唯一解或格式错误
    if (resultcode != 0) {
        // resultcode == 1 (error1) 或 resultcode == 2 (error2)
        // main 函数直接处理，高斯法已确定答案
    } 
    // 2. 唯一解：将问题转化为 M=N 的方阵系统
    else {
        // 矩阵已是阶梯形，且 rank = n (唯一解)
        
        // 2.1 构造一个 N x (N+1) 的方阵系统进行迭代
        vector<vector<double>> square_matrix(n, vector<double>(n + 1));
        
        // 提取前 N 个有效行 (即有主元的行) 
        for(int i = 0; i < n; ++i) {
            square_matrix[i] = matrix[i]; // 将有效行复制到方阵
        }

        // 2.2 使用雅可比迭代求解
        // 注意：雅可比法要求对角元素较大，高斯消元后主元在对角线上，但不保证收敛。
        // 这是该混合方法的固有局限。
        resultcode = jacobiIteration(square_matrix, sol, n);

        // 如果雅可比迭代不收敛，则返回 error1
        if (resultcode == 1) {
            resultcode = 1; // 1: 迭代不收敛 (error1)
        } else if (resultcode == 2) {
             // 如果在迭代中发现对角线是零（不该发生，但以防万一），返回 error2
             resultcode = 2;
        }
    }
    
    // 3. 输出结果
    switch(resultcode){
        case 0:
            for(int i=0; i<n; i++){
                cout<<formatSolution(sol[i])<<(i == n - 1 ? "" : " ");
            }
            cout << endl;
            break;
        case 1: 
            cout << "error1" << endl;
            break;
        case 2: 
            cout << "error2" << endl;
            break;
    }
    
    return 0;
}