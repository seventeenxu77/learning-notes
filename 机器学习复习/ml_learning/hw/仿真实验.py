import numpy as np
DIMENSIONS = [100, 500, 1000] 
N_SAMPLES = 10000            
results = {}

for d in DIMENSIONS:
    X_samples = np.random.uniform(low=-1.0, high=1.0, size=(N_SAMPLES, d))
    squared_norm = np.sum(X_samples**2, axis=1)
    is_in_unit_ball = squared_norm <= 1.0
    N_in_unit_ball = np.sum(is_in_unit_ball)
    ratio = N_in_unit_ball/ N_SAMPLES
    results[d] = (N_in_unit_ball, ratio)
    print(f"\n维度 d = {d}:")
    print(f"  落在单位球内的样本数: {N_in_unit_ball}")
    print(f"  样本比率 R: {ratio:.8e}")
