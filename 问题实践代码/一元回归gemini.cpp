#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <sstream>
#include <string>

using namespace std;

// 定义一个结构体来存储坐标点
struct Point {
    double x;
    double y;
};

// 全局常量：用于比较的浮点误差容忍度
const double EPSILON = 1e-9; 
// 专门用于判断是否接近四位小数精度的误差容忍度
const double PRECISION_EPSILON = 1e-5; 

// 修正后的截断函数：保留4位小数（截断）
double roundToPrecision(double value, int precision) {
    double factor = pow(10.0, precision);
    
    // 使用一个小的 epsilon 来处理浮点运算误差，确保截断正确
    const double tiny_epsilon = 1e-12; 
    
    if (value < 0) {
        // 负数截断：向 0 取整。
        return -floor(-value * factor + tiny_epsilon) / factor;
    } else {
        // 正数截断：
        return floor(value * factor + tiny_epsilon) / factor;
    }
}

// 函数：格式化输出，使用截断后的值，并去除末尾零
string format_truncated_double(double value) {
    double final_value = roundToPrecision(value, 4);
    
    // 使用 stringstream 格式化输出为 4 位小数
    stringstream ss;
    ss << fixed << setprecision(4) << final_value;
    string s = ss.str();
    
    // ---- 尾随零去除逻辑 ----
    size_t dot_pos = s.find('.');
    if (dot_pos == string::npos) {
        return s; // 没有小数点，直接返回
    }

    // 1. 去除末尾的 '0'
    size_t last_char = s.size() - 1;
    // 必须确保不删除小数点左边的数字
    while (last_char > dot_pos && s[last_char] == '0') {
        last_char--;
    }

    // 2. 如果最后字符是 '.'，也去除它（即结果是整数）
    if (s[last_char] == '.') {
        last_char--;
    }
    
    // 确保结果至少保留了小数点左边的数字
    return s.substr(0, last_char + 1);
}

// 函数：检查一个浮点数是否足够接近保留4位小数的数值（用于修正a和b）
double correct_near_precise_value(double value) {
    // 乘以 10000 后的值应该非常接近一个整数
    double scaled_value = value * 10000.0;
    
    // 找出最接近 scaled_value 的整数
    double nearest_integer = round(scaled_value);
    
    // 检查它们是否足够接近
    if (abs(scaled_value - nearest_integer) < PRECISION_EPSILON * 10000.0) {
        // 如果是，返回四位小数的精确值
        return nearest_integer / 10000.0;
    }
    
    // 否则，返回原值
    return value;
}


// 函数：执行一元线性回归分析
void linear_regression_analysis() {
    double predict_x;
    vector<Point> points;
    
    // 读取待预测的 x 值
    if (!(cin >> predict_x)) {
        return; 
    }

    // 读取坐标点
    double x, y;
    while (cin >> x >> y) {
        points.push_back({x, y});
    }

    int n = points.size();

    // 1. 数据校验
    if (n <= 1) {
        cout << "error" << endl;
        cout << "error" << endl;
        return;
    }

    // 2. 计算均值
    double sum_x = 0.0, sum_y = 0.0;
    for (const auto& p : points) {
        sum_x += p.x;
        sum_y += p.y;
    }
    double mean_x = sum_x / n;
    double mean_y = sum_y / n;

    // 3. 计算相关系数 r
    double numerator_r = 0.0; 
    double denominator_r_x = 0.0; 
    double denominator_r_y = 0.0; 
    
    for (const auto& p : points) {
        double dx = p.x - mean_x;
        double dy = p.y - mean_y;
        numerator_r += dx * dy;
        denominator_r_x += dx * dx;
        denominator_r_y += dy * dy;
    }

    double r = 0.0;
    if (denominator_r_x > EPSILON && denominator_r_y > EPSILON) {
        r = numerator_r / sqrt(denominator_r_x * denominator_r_y);
        // 对 r 也进行一次校正，避免 -0.99999999 截断成 -0.9999
        r = correct_near_precise_value(r);
    } else {
        r = 0.0; 
    }

    // 4. 输出相关系数 r
    cout << format_truncated_double(r) << endl;

    // 5. 判断相关性
    if (abs(r) < 0.75) {
        cout << "error" << endl;
        cout << "error" << endl;
        return;
    }

    // 6. 计算回归系数 a (斜率) 和 b (截距)
    double a = 0.0;
    if (denominator_r_x > EPSILON) {
        a = numerator_r / denominator_r_x;
    } else {
        cout << "error" << endl;
        cout << "error" << endl;
        return;
    }
    
    // b = mean_y - a * mean_x
    double b = mean_y - a * mean_x;

    // **** 关键修正：对 a 和 b 进行浮点误差校正 ****
    a = correct_near_precise_value(a);
    b = correct_near_precise_value(b);
    
    // 7. 输出回归方程 y = a*x + b
    string str_a = format_truncated_double(a);
    string str_b = format_truncated_double(abs(b));

    // 构建回归方程字符串
    cout << "y=" << str_a << "*x";
    if (b >= 0) {
        // 为了避免输出 "+0"
        if (abs(b) < 1e-12) {
             cout << endl; // b 接近 0，省略 +0
        } else {
            cout << "+" << str_b << endl;
        }
    } else {
        cout << "-" << str_b << endl;
    }

    // 8. 预测 x=predict_x 时的 y 值
    double predict_y = a * predict_x + b;

    // 8.1 输出预测值 y (保留4位小数，截断，去除尾零)
    cout << format_truncated_double(predict_y) << endl;
}

// 主函数
int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    
    linear_regression_analysis();

    return 0;
}