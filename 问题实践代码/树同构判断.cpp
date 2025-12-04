#include<iostream>
#include<string>
using namespace std;
struct node
{
    int degree;
    node**arr;
    node()
    {
        degree=0;
        arr=new node*[2];
        arr[0]=arr[1]=NULL;
    }
};
class tree
{
public:
    tree(string numsequence)
    {
        root=NULL;
        point=0;
        this->numsequence=numsequence;
        root=new node;
        if(judge())
        {
            isnot_error=1;
            buildtree(root);
        }
        else{isnot_error=0;}
        point=0;
    }
    bool judge()
    {
        int num_1=0;
        int num_0=0;
        for(int i=0;i<numsequence.length();i++)
        {
            if(numsequence[i]!='0'&&numsequence[i]!='1')//这里的逻辑不要搞错
            return 0;
            if(num_0>num_1)
                return 0;
            if(numsequence[i]=='0')
                num_0++;
            if(numsequence[i]=='1')
                num_1++;
        }
        return 1;
    }
    int readnum()
    {
        point++;//这里千万不能使用静态变量static int point=0;point++;因为静态变量是类公用的
        //如果其他类对象调用这个函数时，将会更改这个静态变量，即这个静态变量不是某个对象私有的
        return numsequence[point]-'0';//这里如果直接使用int(numsequence[point])返回的是字符的ascell编码，是错误的
    }
    void buildtree(node*nownode)
    {
        while(1)
        {
            int read=readnum();
            if(read==1)
            {nownode->arr[nownode->degree]=new node;
            buildtree(nownode->arr[nownode->degree]);
            (nownode->degree)++;
            }
            else
            {
                return;
            }
        }
    }
    ~tree()
    {
    }
    node*root;
    string numsequence;
    bool isnot_error;
    int point;
};
bool judge_two(node* tr1,node* tr2)
{
    if(tr1==NULL&&tr2==NULL)
    return 1;
    if((tr1==NULL&&tr2!=NULL)||(tr1!=NULL&&tr2==NULL))
    return 0;
    if(tr1->arr[0]==NULL&&tr2->arr[0]==NULL)
    return judge_two(tr1->arr[1],tr2->arr[1]);
    if(tr1->arr[0]!=NULL&&tr2->arr[0]!=NULL)
    {
        int result=judge_two(tr1->arr[0],tr2->arr[0])&&judge_two(tr1->arr[1],tr2->arr[1]);
        if(result==1)
        return 1;
        return judge_two(tr1->arr[0],tr2->arr[1])&&judge_two(tr1->arr[1],tr2->arr[0]);//如果验证失败，那么再给你一次翻转的机会
    }
    else//两个树其中一个的左子树是空
    return judge_two(tr1->arr[0],tr2->arr[1])&&judge_two(tr1->arr[1],tr2->arr[0]);//调换之后才有一线生机
}
int main()
{
    string a,b;
    getline(cin,a);
    getline(cin,b);
    tree aa(a);
    tree bb(b);
    if(aa.isnot_error==0||bb.isnot_error==0)
    {
        cout<<"error";
    }
    else
    {
        if(judge_two(aa.root,bb.root))
            cout<<"isomorphic";
        else
            cout<<"non-isomorphic";
    }
    return 0;
}