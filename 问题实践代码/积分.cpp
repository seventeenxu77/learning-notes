#include <iostream>
#include <vector>
// #include <cmath>
#include <iomanip>
#include <algorithm>
#include <sstream>
// #include <string>
using namespace std;

double laglangr(double xx,vector<double>&x,vector<double>&y){
    double y_temp;
    double result=0;
    for(int i=0;i<y.size();i++){
        y_temp=y[i];
        for(int j=0;j<x.size();j++){
            if(i!=j)y_temp*=(xx-x[j])/(x[i]-x[j]);
        }
        result+=y_temp;
    }
    return result;
}
double integral(vector<double>&x,vector<double>&y,double a, double b,int N){

    double h = (b - a) / N;
    double sum = 0.0;
    
    sum += laglangr(a, x, y); 
    for (int k = 1; k < N; k++) {
        double x_k = a + k * h;
        double f_k = laglangr(x_k, x, y);
        
        if (k % 2 == 1) {
            sum += 4 * f_k;
        } else {
            sum += 2 * f_k;
        }
    }
    sum += laglangr(b, x, y); 
    return sum * h / 3.0;
}
int main(){
    string line;
    vector<double>x,y;
    double num;
    double xx;
    cin>>xx;
    getline(cin,line);
    while(getline(cin,line)){
        stringstream ss(line);
        ss>>num;
        x.push_back(num);
        ss>>num;
        y.push_back(num);
    }
    double a=*min_element(x.begin(),x.end());
    double b=*max_element(x.begin(),x.end());
    int N=1000;
    double inter_result=integral(x,y,a,b,N);
    cout << fixed << setprecision(2) << inter_result << endl;
}