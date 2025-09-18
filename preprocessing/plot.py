import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import seaborn as sns

# 1. CSV 파일 경로 설정 및 데이터 로드
file_path = r'C:\Users\asx12\esp32\preprocessing\data\csi_add_16_home_normalized.csv'
scaled_data = pd.read_csv(file_path)

# 2. 특징(features)과 라벨(labels) 분리
X = scaled_data.drop('label', axis=1)  # 'label' 열을 제외한 나머지 데이터를 특징으로 설정
y = scaled_data['label']  # 'label' 열을 라벨로 설정

# 3. 데이터셋 분리 (80% 학습용, 20% 테스트용)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 모델 초기화 및 학습
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 5. 테스트 데이터로 예측 수행
y_pred = model.predict(X_test)

# 6. 모델 성능 평가
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')  # 정확도 출력

print("Classification Report:")
print(classification_report(y_test, y_pred))  # 정밀도, 재현율, F1-score 출력

'''# 랜덤 포레스트 모델에서 첫 번째 결정 트리를 선택
first_tree = model.estimators_[0]

# 트리 구조를 그래픽으로 출력
plt.figure(figsize=(20, 10))
plot_tree(first_tree, feature_names=X.columns, filled=True, fontsize=10, max_depth=3)
plt.title("First Decision Tree in Random Forest")
plt.show()'''


# 혼동 행렬 계산
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)


# 8. 시각화: 혼동 행렬
def plot_confusion_matrix(conf_matrix):
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['No Person', 'Left', 'Center', 'Right'],
                yticklabels=['No Person', 'Left', 'Center', 'Right'])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()



# 10. 혼동 행렬 시각화
plot_confusion_matrix(conf_matrix)

# 10. Classification Report 시각화
def plot_classification_report(report):
    report_df = pd.DataFrame(report).transpose()
    plt.figure(figsize=(10, 6))
    sns.heatmap(report_df[['precision', 'recall', 'f1-score']], annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Classification Report')
    plt.show()

# Classification Report 계산 및 시각화
report = classification_report(y_test, y_pred, output_dict=True)
plot_classification_report(report)

'''# 11. Feature Importance 시각화
def plot_feature_importance(importance, names, model_type):
    feature_importance = np.array(importance)
    feature_names = np.array(names)
    data={'Feature Names':feature_names, 'Feature Importance':feature_importance}
    fi_df = pd.DataFrame(data)
    fi_df.sort_values(by=['Feature Importance'], ascending=False, inplace=True)
    
    plt.figure(figsize=(12,8))
    sns.barplot(x='Feature Importance', y='Feature Names', data=fi_df)
    plt.title(f'Feature Importance ({model_type})')
    plt.show()

# Feature Importance 시각화
plot_feature_importance(model.feature_importances_, X.columns, 'Random Forest')'''


