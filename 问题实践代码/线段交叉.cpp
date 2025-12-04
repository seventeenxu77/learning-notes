#include <iostream>
#include <vector>
#include <cmath>
// #include <iomanip>
//#include <algorithm>
#include <sstream>
// #include <string>
using namespace std;
struct Point{
    double x;
    double y;
};
double vector_cross_product(Point p1,Point p2){
    return p1.x*p2.y-p1.y*p2.x;
}
bool is_cross(Point p1,Point p2,Point p3,Point p4){
    Point v_main_1={p2.x-p1.x,p2.y-p1.y};
    Point v_main_2={p4.x-p3.x,p4.y-p3.y};
    Point v_1={p3.x-p1.x,p3.y-p1.y};
    Point v_2={p4.x-p1.x,p4.y-p1.y};
    Point v_3={p1.x-p3.x,p1.y-p3.y};
    Point v_4={p2.x-p3.x,p2.y-p3.y};
    double re1=vector_cross_product(v_main_1,v_1)*vector_cross_product(v_main_1,v_2);
    double re2=vector_cross_product(v_main_2,v_3)*vector_cross_product(v_main_2,v_4);
    if(re1<0&&re2<0)return 1;
    return 0;
}
bool judegecross(vector<Point>verticles){
    int n=verticles.size();
    for(int i=0;i<n;i++){
        for(int j=i+1;j<n;j++){
            //通过叉乘判断选定的这个线段和其他线段有无相交。
            //如果相交，直接返回1
            bool judge=is_cross(verticles[i],verticles[i+1],verticles[j],verticles[(j+1)%n]);
            if(judge)return 1;
        }
    }
    return 0;
}
// double calarea(vector<Point>verticles){
//     //划分为多个三角形求解
// }
double calarea(const vector<Point>& vertices){
    int n = vertices.size();
    if (n < 3) return 0.0;
    
    double area_sum = 0.0;
    
    for(int i = 0; i < n; i++) {
        // V_i 和 V_{i+1}，注意 V_n = V_0
        double xi = vertices[i].x;
        double yi = vertices[i].y;
        
        double xi_plus_1 = vertices[(i + 1) % n].x;
        double yi_plus_1 = vertices[(i + 1) % n].y;
        
        // 累加叉乘: x_i * y_{i+1} - x_{i+1} * y_i
        area_sum += (xi * yi_plus_1 - xi_plus_1 * yi);
    }
    
    // 面积 = 1/2 * |累加和|
    return fabs(area_sum) / 2.0;
}
int main(){
    string line;
    vector<double>x,y;
    vector<Point>verticles;
    double x_val,y_val,result=0.0,y_temp;
    double xx;
    cin>>xx;
    getline(cin,line);
    while(getline(cin,line)){
        stringstream ss(line);
        if(ss>>x_val&&ss>>y_val){//读入
            x.push_back(x_val);
            y.push_back(y_val);
            verticles.push_back({x_val,y_val});
        }
    }

    for(int i=0;i<y.size();i++){
        y_temp=y[i];
        for(int j=0;j<x.size();j++){
            if(i!=j)y_temp*=(xx-x[j])/(x[i]-x[j]);
        }
        result+=y_temp;
    }
    x.push_back(xx);
    y.push_back(result);
    verticles.push_back({xx,result});
    if(judegecross(verticles)){
        cout<<"cross";
    }
    else{
        cout<<calarea(verticles);
    }
}