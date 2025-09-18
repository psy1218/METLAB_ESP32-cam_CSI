import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix #모델 성능 평가

# 1. CSV 파일 경로 설정 및 데이터 로드
#file_path = r'C:\Users\asx12\esp32\preprocessing\data\csidata_0903_1_6mnormalized.csv'
#file_path = r'C:\Users\asx12\esp32\preprocessing\data\1_2_add_data_normalized.csv'

file_path ='C:/Users/asx12/esp32/preprocessing/data/0923_304/0923_csi_304_add_scaler.csv'


scaled_data = pd.read_csv(file_path)

# 2. 특징(features)과 라벨(labels) 분리
X = scaled_data.drop('label', axis=1)  # 'label' 열을 제외한 나머지 데이터를 특징으로 설정
y = scaled_data['label']  # 'label' 열을 라벨로 설정
# 모델이 예측할 목표 변수(타겟)

# 3. 데이터셋 분리 (80% 학습용, 20% 테스트용)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#데이터 분리를 재현 가능하게 하기 위해 난수 발생 시드를 설정하는 옵션입니다. 같은 데이터를 넣었을 때 같은 결과를 얻을 수 있게 합니다.

# 4. 모델 초기화 및 학습
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 5. 테스트 데이터로 예측 수행
y_pred = model.predict(X_test)

# 6. 모델 성능 평가
accuracy = accuracy_score(y_test, y_pred) #모델의 예측 결과(y_pred)와 실제 라벨
print(f'Accuracy: {accuracy * 100:.2f}%') #정확도

print("Classification Report:")
print(classification_report(y_test, y_pred))
#예측 결과에 대한 정밀도(precision), 재현율(recall), F1-score

#Recall(재현율 또는 민감도):  모델이 긍정 클래스를 놓친 경우, 
#즉 실제로 긍정 클래스였지만 모델이 부정 클래스로 예측한 샘플 수

#F1-score:  정밀도와 재현율의 조화 평균을 계산한 값
# 값의 조화 평균이기 때문에 둘 중 하나가 매우 낮다면 F1-score도 낮게 나옵니다.

#Support: 각 클래스에 속하는 실제 샘플 수.

#Macro Average: 각 클래스의 메트릭을 단순 평균하여 계산합니다. 클래스의 지원 수에 관계없이 모든 클래스를 동등하게 취급합니다.
#Weighted Average: 각 클래스의 메트릭을 지원 수에 비례하여 가중 평균합니다. 클래스의 빈도를 고려하여 평균을 계산합니다.

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
#예측 결과와 실제 라벨 간의 혼동 행렬을 출력
