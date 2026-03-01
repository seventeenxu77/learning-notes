#include<iostream>
#include<algorithm>
using namespace std;
int**dp,**mem;
int mine,people;
int *gold_mine;
int *people_mine;
int dp_process(int i,int j){
    if(i==mine-1)return people_mine[i]<=j?gold_mine[i]:0;

    int yes=0,no=0;
    //要
    if(j>=people_mine[i]){
        if(mem[i+1][j-people_mine[i]]==-1){
            yes=dp_process(i+1,j-people_mine[i])+gold_mine[i];
            mem[i+1][j-people_mine[i]]=yes;
        }
        else{
            yes=mem[i+1][j-people_mine[i]]+gold_mine[i];
        }
    }
    //不要
    if(mem[i+1][j]==-1){
            no=dp_process(i+1,j);
            mem[i+1][j]=no;
        }
        else{
            no=mem[i+1][j];
        }
    return max(yes,no);
}
int main(){
    cin>>people;
    cin>>mine;
    gold_mine=new int[mine];
    people_mine=new int[mine];
    for(int i=0;i<mine;i++)cin>>gold_mine[i];
    for(int i=0;i<mine;i++)cin>>people_mine[i];
    mem=new int*[mine];
    for(int i=0;i<mine;i++)mem[i]=new int[people+1];
    for(int i=0;i<mine;i++){
        for(int j=0;j<=people;j++){
            mem[i][j]=-1;
        }
    }
    for(int i=0;i<mine;i++)mem[i][0]=0;
    for(int i=0;i<=people;i++)mem[0][i]=0;
    cout<<dp_process(0,people);

}