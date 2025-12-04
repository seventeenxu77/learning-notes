#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <sstream>
#include <string>
using namespace std;
const double epison=1e-9;
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
    if (abs(final_value - round(final_value)) < epison) {
        return to_string((long long)round(final_value));
    } else {
        stringstream ss;
        ss << fixed << setprecision(4) << final_value;
        string s = ss.str();
        size_t dot_pos = s.find('.');
        if (dot_pos == string::npos) {
            return s;
        }
        size_t last_char = s.size() - 1;
        while (last_char > dot_pos && s[last_char] == '0') {
            last_char--;
        }
        if (s[last_char] == '.') {
            last_char--;
        }
        return s.substr(0, last_char + 1);
    }
}
int guass(vector<vector<double>>&matrix,vector<double>&sol,int m,int n){
    int pivot_row=0;
    int rank=0;
    for(int i=0;i<n&& pivot_row < m;i++){//增加行小于列矩阵的检查
        int max_row=pivot_row;
        for(int j=pivot_row+1;j<m;j++){
            if(abs(matrix[j][i])>abs(matrix[max_row][i])){
                max_row=j;
            }
        }
        if(pivot_row!=max_row){
            swap(matrix[pivot_row],matrix[max_row]);
        }
        if(abs(matrix[pivot_row][i])<epison)continue;
        rank++;
        //消元
        for(int j=pivot_row+1;j<m;j++){
            double factor=matrix[j][i]/matrix[pivot_row][i];
            for(int k=i;k<=n;k++){//增广列消元
                matrix[j][k]-=factor*matrix[pivot_row][k];
            }
        }
        pivot_row++;
    }
    //检测无解和无穷解情况
    for(int j=pivot_row;j<m;j++){
        if(abs(matrix[j][n])>epison)return 1;//无解
    }
    if(rank<n)return 2;//w无穷解，要放在无解之后
    //代入过程
    sol.assign(n,0.0);
    for(int j=n-1;j>=0;j--){
        if (abs(matrix[j][j]) < epison) {
             return 2; 
        }
        double sum=0.0;
        for(int k=j+1;k<n;k++){
            sum+=sol[k]*matrix[j][k];
        }
        sol[j]=(matrix[j][n]-sum)/matrix[j][j];
    }
    return 0;
}

int main(){
    string line;
    vector<vector<double>>matrix;
    vector<double> sol;
    double num;
    int n=0,m=0;
    while(getline(cin,line)){
        if(line.empty())continue;//
        vector<double> equa;//每次while会自动清空
        stringstream ss(line);
        while(ss>>num){
            equa.push_back(num);
        }
        if(equa.empty())continue;//
        if(m==0){
            n=equa.size()-1;
        }else{
            if(equa.size()-1!=n)return 1;
        }
        matrix.push_back(equa);
        m++;
    }
    if (m == 0 || n <= 0) return 0;
    int resultcode=guass(matrix,sol,m,n);
    switch(resultcode){
        case 0:
        for(int i=0;i<n;i++){
            cout<<formatSolution(sol[i])<<" ";
        }
        break;
        case 1: 
        cout << "error1" << endl;
        break;
        case 2: // 无穷多解
        cout << "error2" << endl;
        break;
    }
}