import numpy as np
import pandas as pd
import time
import requests
import io

from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score
from collections import defaultdict

# --- 1. 数据配置 ---
DATASET_URLS = {
    # 两个不同的数据集
    "A1A (Small)": "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/a1a",
    "A9A (Large)": "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/a9a"
}

# --- 2. 模型配置 ---
BASE_MODELS = {
    "Logistic Regression (LR)": LogisticRegression(solver='liblinear', random_state=42, max_iter=1000),
    "Naive Bayes (NB)": GaussianNB(),
    "Linear Discriminant Analysis (LDA)": LDA(),
    "Support Vector Machine (SVM-Linear)": SVC(kernel='linear', random_state=42, gamma='auto'),
    "Neural Networks (MLP)": MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42, early_stopping=True)
}

# --- 3. 实验结果存储 ---
all_results = defaultdict(dict)

# ----------------------------------------------------------------------
# 核心函数定义 (已修复)
# ----------------------------------------------------------------------

def load_and_preprocess_data(url):
    """从URL远程加载svmlight格式数据并进行预处理"""
    print(f"尝试从URL加载数据: {url}")
    
    # 步骤 1: 使用 requests 获取远程文件内容
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status() # 检查 HTTP 错误
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        # 如果获取失败，返回空数据或抛出错误
        return np.array([]), np.array([]) 

    # 步骤 2: 将下载的内容（字节流）封装为文件对象
    # load_svmlight_file 期望一个文件句柄，BytesIO 提供了内存中的句柄
    data_io = io.BytesIO(response.content)

    # 步骤 3: 使用 load_svmlight_file 从内存文件对象加载数据
    X_sparse, y = load_svmlight_file(data_io)
    X = X_sparse.toarray() # 转换为密集格式
    
    # 标准化
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    print(f"数据加载和预处理完成。X 形状: {X.shape}, y 形状: {y.shape}")
    
    return X, y

def evaluate_model(model, X_train, y_train, X_test, y_test):
    """训练和评估单个模型"""
    try:
        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='binary', zero_division=0)
        
        return {
            'Accuracy': accuracy,
            'F1-Score': f1,
            'Train Time (s)': training_time
        }
    except Exception as e:
        print(f"模型评估错误: {type(model).__name__} 失败, Error: {e}")
        return {'Accuracy': np.nan, 'F1-Score': np.nan, 'Train Time (s)': np.nan, 'Error': str(e)}

def run_experiment_set(dataset_name, X, y, experiment_tag, models_to_run):
    """运行一组模型的比较实验"""
    if X.size == 0:
        print(f"跳过实验集 {dataset_name}，因为数据加载失败。")
        return
        
    print(f"\n--- 运行实验: {dataset_name} ({experiment_tag}) ---")
    
    # 划分数据集：30% 作为测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    for name, model_instance in models_to_run.items():
        # 确保每次迭代使用新的模型实例
        model = type(model_instance)(**model_instance.get_params())
        print(f"  -> 正在训练 {name}...")
        results = evaluate_model(model, X_train, y_train, X_test, y_test)
        
        # 记录结果
        full_tag = f"{dataset_name} ({experiment_tag})"
        all_results[full_tag][name] = results
        
        # 打印实时结果
        acc = results['Accuracy']
        time_sec = results['Train Time (s)']
        print(f"     Accuracy: {acc:.4f}, Time: {time_sec:.2f}s")


# ----------------------------------------------------------------------
# 主程序：执行实验
# ----------------------------------------------------------------------

# --- (A) 核心实验：比较五种模型 ---

for name, url in DATASET_URLS.items():
    X_data, y_data = load_and_preprocess_data(url)
    run_experiment_set(name, X_data, y_data, "Baseline", BASE_MODELS)

# --- (B) 经验性调查 1: 改变训练集样本大小 (使用 A1A) ---

X_A1A, y_A1A = load_and_preprocess_data(DATASET_URLS["A1A (Small)"])

if X_A1A.size > 0:
    TEST_SIZE_A1A = 0.2
    X_train_full, X_test, y_train_full, y_test = train_test_split(
        X_A1A, y_A1A, test_size=TEST_SIZE_A1A, random_state=42
    )
    
    for sample_ratio in [0.2, 0.5, 0.8]:
        train_size = int(len(X_train_full) * sample_ratio)
        X_train_sub = X_train_full[:train_size]
        y_train_sub = y_train_full[:train_size]
        
        sample_models = {
            "LR": LogisticRegression(solver='liblinear', random_state=42, max_iter=500),
            "SVM-Linear": SVC(kernel='linear', random_state=42, gamma='auto')
        }
        
        print(f"\n--- 运行实验: A1A (Sample Ratio: {sample_ratio:.1f}, N_train={len(X_train_sub)}) ---")
        for name, model_instance in sample_models.items():
            model = type(model_instance)(**model_instance.get_params())
            results = evaluate_model(model, X_train_sub, y_train_sub, X_test, y_test)
            full_tag = f"A1A (Sample Ratio={sample_ratio:.1f})"
            all_results[full_tag][name] = results
            print(f"  -> {name} Acc: {results['Accuracy']:.4f}")

# --- (C) 经验性调查 2: 改变 SVM 核函数 (使用 A9A) ---

X_A9A, y_A9A = load_and_preprocess_data(DATASET_URLS["A9A (Large)"])

if X_A9A.size > 0:
    SVM_MODELS = {
        "SVM (Linear Kernel)": SVC(kernel='linear', random_state=42, gamma='auto'),
        "SVM (RBF Kernel)": SVC(kernel='rbf', random_state=42, gamma='scale'),
        "SVM (Poly Kernel)": SVC(kernel='poly', degree=3, random_state=42, gamma='auto')
    }
    
    run_experiment_set("A9A (Large)", X_A9A, y_A9A, "Kernel Comparison", SVM_MODELS)

# ----------------------------------------------------------------------
# 结果整理和输出
# ----------------------------------------------------------------------

# 将结果字典转换为 Pandas DataFrame 以便分析
df_list = []
for experiment_tag, model_results in all_results.items():
    for model_name, metrics in model_results.items():
        row = {'Experiment': experiment_tag, 'Model': model_name}
        row.update(metrics)
        df_list.append(row)

final_df = pd.DataFrame(df_list)

print("\n\n" + "="*80)
print("最终实验结果表 (按准确率排序)")
print("="*80)
if not final_df.empty:
    print(final_df.sort_values(by='Accuracy', ascending=False)[['Experiment', 'Model', 'Accuracy', 'F1-Score', 'Train Time (s)']].to_markdown(index=False, floatfmt=".4f"))
else:
    print("没有生成结果，请检查网络连接和 requests 库是否安装。")
