import pandas as pd

# CSV 파일 경로 설정 및 데이터 로드
file_path = 'C:/Users/asx12/esp32/preprocessing/data/0923_304/0923_csi_304_add_scaler.csv'
scaled_data = pd.read_csv(file_path)

# NaN 값 확인
print(f"NaN values in entire dataset: \n{scaled_data.isnull().sum()}")

# 공백이나 빈 문자열이 있는지 확인
print("Rows with empty or whitespace values in 'label' column:")
print(scaled_data[scaled_data['label'].apply(lambda x: pd.isna(x) or str(x).strip() == '')])
