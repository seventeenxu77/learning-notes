#include<iostream>
#include<algorithm>
#include<sstream>
#include<vector>
using namespace std;
int layer;
vector<vector<int>>numtower;
int dp_process(int i,int j){
    int l,r;
    if(i==layer-1)return numtower[i][j];
        l=dp_process(i+1,j);
        r=dp_process(i+1,j+1);
        return max(l,r)+numtower[i][j];
}
int main(){
    string line;
    int a;
    while(getline(cin,line)){
        if(line.empty())break;
        stringstream ss(line);
        vector<int>num;
        while(ss>>a)num.push_back(a);
        numtower.push_back(num);
    }
    layer=numtower.size();
    cout<<dp_process(0,0);
}