#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

// 全局变量，用于记录当前正在解析的字符串索引
int global_index;
string tree_sequence;

// 检查输入是否为合法的括号序（0-1序列）
bool is_valid_sequence(const string& s) {
    if (s.empty()) return false;
    int balance = 0;
    for (char c : s) {
        if (c == '1') {
            balance++;
        } else if (c == '0') {
            balance--;
        } else {
            return false; // 包含非0/1字符
        }
        if (balance < 0) {
            return false; // 0比1多
        }
    }
    return balance == 0; // 最终1和0数量相等
}

// 递归地计算当前子树的规范编码 (Canonical Encoding)
// 从 global_index 开始解析，返回当前子树的规范编码
string get_canonical_encoding() {
    // 当前字符必须是 '1'，表示一个新节点/子树的开始
    if (global_index >= tree_sequence.length() || tree_sequence[global_index] != '1') {
        // 理论上不应该发生，因为 is_valid_sequence 已经检查了合法性
        return ""; 
    }
    
    global_index++; // 跳过开头的 '1'

    vector<string> children_encodings;

    // 循环解析所有子树，直到遇到当前节点的结束 '0'
    while (global_index < tree_sequence.length() && tree_sequence[global_index] == '1') {
        // 递归计算子树的规范编码
        string child_encoding = get_canonical_encoding();
        if (child_encoding.empty()) {
            // 递归调用返回空，说明解析失败或输入不合法，直接返回空串
            return "";
        }
        children_encodings.push_back(child_encoding);
    }
    
    // 检查当前节点是否正确结束于 '0'
    if (global_index >= tree_sequence.length() || tree_sequence[global_index] != '0') {
        // 序列不完整或不合法 (例如: 110)
        return "";
    }
    
    global_index++; // 跳过结束的 '0'

    // 1. 对所有子树的规范编码进行字典序排序
    sort(children_encodings.begin(), children_encodings.end());

    // 2. 将排序后的子编码连接起来
    string sorted_children_concat;
    for (const string& encoding : children_encodings) {
        sorted_children_concat += encoding;
    }

    // 3. 加上当前节点的 '1' 和 '0' 形成最终规范编码
    return "1" + sorted_children_concat + "0";
}

string get_tree_canonical_encoding(const string& s) {
    if (!is_valid_sequence(s)) {
        return "error"; // 不合法序列
    }
    
    tree_sequence = s;
    global_index = 0;
    
    string canonical_code = get_canonical_encoding();
    
    // 检查是否恰好用完整个序列，确保是单棵完整的树
    if (global_index != s.length()) {
        return "error"; 
    }
    
    return canonical_code;
}

int main() {
    string a, b;
    // 使用 cin.tie(nullptr)->sync_with_stdio(false); 优化输入速度
    // 但对于本题规模不需要，使用 getline 保证读取完整行
    if (!getline(cin, a) || !getline(cin, b)) {
        return 0; // 处理输入结束
    }

    string code1 = get_tree_canonical_encoding(a);
    string code2 = get_tree_canonical_encoding(b);

    if (code1 == "error" || code2 == "error") {
        cout << "error" << endl;
    } else {
        // 如果两棵树的规范编码相同，则同构
        if (code1 == code2) {
            cout << "isomorphic" << endl;
        } else {
            cout << "non-isomorphic" << endl;
        }
    }

    return 0;
}