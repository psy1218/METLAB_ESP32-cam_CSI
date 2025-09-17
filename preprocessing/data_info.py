import pandas as pd

# CSV 파일 로드
file_path = r'C:\Users\asx12\esp32\preprocessing\data\1_2_add_data.csv'
data = pd.read_csv(file_path)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
features = data.drop('label', axis=1)  # 'label' 열은 제외하고 정규화
labels = data['label']

scaled_features = scaler.fit_transform(features)

# 정규화된 데이터를 다시 DataFrame으로 변환
scaled_data = pd.DataFrame(scaled_features, columns=features.columns)
scaled_data['label'] = labels  # 라벨 추가