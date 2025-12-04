#include <iostream>
#include <vector>
// #include <cmath>
// #include <iomanip>
//#include <algorithm>
#include <sstream>
// #include <string>
using namespace std;

int main(){
    string line;
    vector<int>x,y;
    double num,result=0.0,y_temp;
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

    for(int i=0;i<y.size();i++){
        y_temp=y[i];
        for(int j=0;j<x.size();j++){
            if(i!=j)y_temp*=(xx-x[j])/(x[i]-x[j]);
        }
        result+=y_temp;
    }
    cout<<result;
}