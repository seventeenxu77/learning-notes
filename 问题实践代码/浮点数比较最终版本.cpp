#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <string>
#include <ctype.h>
using namespace std;
double epsilon=1e-8;
double isdouble(int &t,const string line){
    double sum=0.0;
    double ra=10.0;
    bool flag=0;
    while(isdigit(line[t])||line[t]=='.'){
        if(line[t]=='.'){
            ra=0.1;
            flag=1;
        }
        else{
            if(!flag){
                sum=sum*ra+(line[t]-'0');
            }
            else{
                sum=sum+(line[t]-'0')*ra;
                ra*=0.1;
            }
        }
        t++;
    }
    t--;
    return sum;
}
string istoken(int pre,int back,const string line){
    string new_str(line.substr(pre,back-pre+1));
    int i=0,j=0;
    while(i<new_str.length()){
        if(isalpha(new_str[i])){
            if(i+1<new_str.length())j=i+1;
            while(j<new_str.length()&&(new_str[j]==' '||new_str[j]=='\t'))j++;
            if(j==new_str.length()){
                new_str.erase(i+1,j-i);
                return new_str;
            }
            if(isalpha(new_str[j]))i=j;
            else{
                new_str.erase(i+1,j-i-1);
                i++;
            }
        }
        else{
            if(new_str[i]==' '||new_str[i]=='\t')new_str.erase(i,1);
            else{
                i++;
            }
        }
    }
    // cout<<new_str<<endl;
    return new_str;
}
void process(string line,vector<double>& num,vector<string>& token){
    int t=0;
    int pre=0;
    int back=0;
    while(t<line.length()){
        if(!isdigit(line[t])){
            back=t;
            if(t+1==line.length()||(t+1<line.length()&&isdigit(line[t+1]))){
                token.push_back(istoken(pre,back,line));
            }
        }
        else{
            num.push_back(isdouble(t,line));
            pre=t+1;
            back=t+1;
        }
        t++;
    }
}

int main(){
    string line;
    vector<double>first;
    vector<double>second;
    vector<string>token1;
    vector<string>token2;
    double x;
    getline(cin,line);
    x=stod(line.erase(0,1));
    string temp="";
    int flag=0;
    while(getline(cin,line)){
        if(line[0]=='#'&&flag){
            break;
        }
        flag=1;
        temp+=line;
    }
    // cout<<"---"<<endl;
    // cout<<temp;
    // cout<<"---"<<endl;
    process(temp,first,token1);
    //第二个
    temp=line;
    while(getline(cin,line)){
        if(line.empty())break;
        temp+=line;
    }
    process(temp,second,token2);
    for(int i=0;i<first.size();i++){
        if(fabs(first[i]-second[i])<=x+epsilon)continue;
        // cout<<first[i]<<" "<<second[i]<<"  "<<x<<"  "<<fabs(first[i]-second[i])<<endl;
        cout<<"N";
        return 0;
    }
    //调试信息
    // for(int i=0;i<token1.size();i++){
    //     cout<<token1[i];
    // }
    // cout<<"hi"<<endl;
    // for(int i=0;i<token2.size();i++){
    //     cout<<token2[i];
    // }
    // cout<<"hi"<<endl;
    string aa="";
    string bb="";
    for(int i=0;i<token1.size();i++){
        aa.append(token1[i]);
    }
    for(int i=0;i<token2.size();i++){
        bb.append(token2[i]);
    }
    if(aa!=bb){
        cout<<"N";
        return 0;
    }
    cout<<"Y";
    return 0;
}