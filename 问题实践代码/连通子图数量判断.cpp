#include<iostream>
#include<string>
#define maxnum 20
int group[maxnum];
int dist[maxnum][maxnum];
using namespace std;
void dfs(int i,int n)
{
    group[i]=1;
    for(int j=0;j<n;j++)
    {
        if(dist[i][j]==1)
        {
            if(group[j]==0)
            dfs(j,n);
        }
    }
}
void initial_fisrt()
{
    for(int i=0;i<maxnum;i++)
    {
        for(int j=0;j<maxnum;j++)
        {
            dist[i][j]=0;
        }
        group[i]=1;//将所有的数假设为已经访问过了，随后的初始化过程将存在的节点group变成0即可
    }
}
int readnum(int &i,string wait_to_process,int &status)
{
    int c=0;
    while(i<wait_to_process.length()&&(wait_to_process[i]>='0'&&wait_to_process[i]<='9'))//一定要取等号
    {
        c*=10;
        c+=wait_to_process[i]-'0';
        i++;
    }
    if(i==wait_to_process.length())
    {
        status=0;
        return c;
    }//输入彻底结束
    if(wait_to_process[i]==' ')
    status=1;//输入结束
    if(wait_to_process[i]=='-')
    status=2;//等待下一个数字
    return c;
}
int initial(string wait_to_be_process)
{
    int i=0;
    int a=0,b=0,status=0;
    while(i<wait_to_be_process.length())
    {
        a=readnum(i,wait_to_be_process,status);
        if(status==0)
        {
            group[a]=0;
            return maxnum;
        }
        if(status==1)
        {
            group[a]=0;
            i++;
        }
        if(status==2)
        {
            i+=2;
            status=0;
            b=readnum(i,wait_to_be_process,status);
            group[a]=0;
            group[b]=0;
            dist[a][b]=1;
            dist[b][a]=1;
            if(status==0)
            return maxnum;
            i++;
        }
        a=0;
        b=0;
        status=0;
    }
    return maxnum;
}
int process_result(int n)
{
    int k=0;
    for(int i=0;i<n;i++)
    {
        if(group[i]==0)
        {
            dfs(i,n);
            k++;
        }
    }
    return k;
}
int main()
{
    initial_fisrt();
    string wait_to_be_process="";
    getline(cin,wait_to_be_process);
    int n=initial(wait_to_be_process);
    int result=process_result(n);
    if(result==1)
    cout<<"1";
    else
    cout<<result;
    return 0;
}