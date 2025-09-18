import numpy as np
import pandas as pd

# CSV 파일 경로
file_path = 'C:/Users/asx12/esp32/preprocessing/data/csidata_0903.csv'

# CSV 파일을 읽어와서 pandas DataFrame으로 변환
df = pd.read_csv(file_path)

# label, rssi, timestamp 등을 제외한 나머지 데이터만 추출
# 필요에 따라 이 부분을 조정하세요
data_columns = df.columns[3:]  # 3번째 열 이후부터가 'data' 열들이라고 가정

# 데이터를 numpy 배열로 변환
normalized_data = df[data_columns].values

'''# 평균과 분산 계산
means = np.mean(normalized_data, axis=0)
variances = np.var(normalized_data, axis=0)

print("Means:", means)
print("Variances:", variances)'''

#normalized_data = normalized_data[~np.isnan(normalized_data).any(axis=1)]

# 결측치(NaN) 확인
nan_count = np.isnan(normalized_data).sum()
print(f"Number of NaN values: {nan_count}")

# 무한대(inf) 값 확인
inf_count = np.isinf(normalized_data).sum()
print(f"Number of Inf values: {inf_count}")

means = np.mean(normalized_data, axis=0)
variances = np.var(normalized_data, axis=0)

print("Means:", means)
print("Variances:", variances)

# 매우 작은 수치들을 0으로 간주하기 위해 임계값 설정
epsilon = 1e-10

# 평균값이 epsilon보다 작은 경우 0으로 설정
means = np.where(np.abs(means) < epsilon, 0, means)

# 결과 출력
print("Means (after applying epsilon):", means)
print("Variances:", variances)