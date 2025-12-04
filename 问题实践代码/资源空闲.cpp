#include<iostream>
#include<sstream>
#include<string>
#include<vector>
#include<algorithm>
using namespace std;
bool cmp(const vector<int>& v1, const vector<int>& v2) {
    return v1[1] < v2[1];
}
void user_compare(vector<vector<int>>&task){
    sort(task.begin(), task.end(), cmp);
}
int main(){
    string line;
    int a,b,c;
    vector<vector<int>>task;
    while(getline(cin,line)){
        stringstream ss(line);
        while(ss>>a&&ss>>b&&ss>>c){
            task.push_back({b,c});
        }
    }
    user_compare(task);
    int size=task.size();
    int *dp=new int[size];
    dp[0]=task[0][1]-task[0][0];
    for(int i=1;i<size;i++){
        dp[i]=dp[i-1];
        int temp=task[i][1]-task[i][0];
        for(int j=i-1;j>=0;j--){
            if(task[j][1]<=task[i][0]){
                temp+=dp[j];
                break;
            }
        }
        dp[i]=max(dp[i],temp);
    }
    cout<<24-dp[size-1];


}