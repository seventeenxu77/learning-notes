#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include <vector>
using namespace std;
int kk;
int row;
bool cmp(const vector<string>& v1, const vector<string>& v2) {
    //Kk决定是升序还是逆序，row决定是vector的第几列进行字符串的比较
    if (kk == 1) {
        return v1[row] < v2[row];
    } else {
        return v1[row] > v2[row];
    }
}
void user_compare(vector<vector<string>>&table){
    sort(table.begin(), table.end(), cmp);
}
int main(){
    string line;
    vector<vector<string>>table;
    string instruct;
    cin>>row;
    row--;
    cin>>instruct;
    getline(cin,line); //吸收换行符
    string temp;
    while(getline(cin,line)){
        if(line.empty())break;
        stringstream ss(line);
        vector<string>people;
        while(ss>>temp){
            people.push_back(temp);
        }
        table.push_back(people);
    }
    int state=(instruct=="ascend"?1:0);
    kk=state;
    user_compare(table);
    for (const auto& row_vec : table) {
        for (size_t i = 0; i < row_vec.size(); ++i) {
            cout << row_vec[i];
            if (i < row_vec.size() - 1) {
                cout << "   "; 
            }
        }
        cout << endl; 
    }

}