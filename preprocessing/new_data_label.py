import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. 학습 데이터 경로 설정 및 로드 (라벨링이 되어 있는 데이터)
file_path = r'C:\Users\asx12\esp32\preprocessing\data\0923_304\0923_csi_304_add_scaler.csv'
data = pd.read_csv(file_path)

# 2. 특징(features)과 라벨(labels) 분리
X = data.drop('label', axis=1)  # 'label' 열 제외한 나머지 데이터를 특징으로 설정
y = data['label']  # 'label' 열을 라벨로 설정 (0: 사람없음, 1: 왼쪽, 2: 가운데, 3: 오른쪽)

# 3. 데이터셋 분리 (80% 학습용, 20% 테스트용)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 랜덤 포레스트 모델 학습
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 5. 모델 성능 평가 (테스트 데이터로 예측)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')  # 정확도 출력
print("Classification Report:")
print(classification_report(y_test, y_pred))  # 정밀도, 재현율, F1-score 출력
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))  # 혼동 행렬 출력

# 6. 라벨링되지 않은 새로운 데이터 불러오기
new_file_path = r'C:\Users\asx12\esp32\preprocessing\data\0923_304\0923_csi_304_walk_rl_scaler.csv'
new_data = pd.read_csv(new_file_path)

# 7. 학습된 모델로 예측 수행 (특징만 추출해서 사용)
#new_X = new_data  # 새로운 데이터에서 특징만 사용
# 7. 학습된 모델로 예측 수행 (특징만 추출, label 컬럼 제외)
if 'label' in new_data.columns:
    new_X = new_data.drop('label', axis=1)
else:
    new_X = new_data

# 8. 학습된 모델로 예측 수행
new_labels = model.predict(new_X)

# 9. 예측된 라벨을 새로운 데이터에 추가
new_data['predicted_label'] = new_labels

# 라벨 설명 추가 (0: 사람없음, 1: 왼쪽 감지, 2: 가운데 감지, 3: 오른쪽 감지)
label_mapping = {0: '사람없음', 1: '왼쪽 감지', 2: '가운데 감지', 3: '오른쪽 감지'}
new_data['label_description'] = new_data['predicted_label'].map(label_mapping)

# 10. 새로운 라벨링된 데이터 저장
output_file_path = r'C:\Users\asx12\esp32\preprocessing\data\0923_304\labeled_0923_walk_rl_scaler.csv'
new_data.to_csv(output_file_path, index=False)

print(f'라벨링된 데이터가 "{output_file_path}"에 저장되었습니다.')
