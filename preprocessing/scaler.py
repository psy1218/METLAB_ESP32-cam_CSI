import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

# CSV 파일 읽어오기

df = pd.read_csv('C:/Users/asx12/esp32/preprocessing/data/0923_304/0923_csi_304_walk_rl_normalized.csv')
#df = pd.read_csv('C:/Users/asx12/esp32/new_esp5/components/esp-idf-v5.3/git-esp-csi/esp-csi-master/examples/get-started/csi_recv_router/0923_csi_walk_rlr.csv')
# 'rssi', 'timestamp', 'label'을 제외한 나머지 컬럼만 선택
data_columns = [col for col in df.columns if col not in ['rssi', 'timestamp', 'label']]

# 결측값(NaN) 및 무한대(inf) 값을 확인하고 처리
# 무한대 값을 NaN으로 변환
#df[data_columns] = df[data_columns].replace([np.inf, -np.inf], np.nan)

# NaN 값이 있는 행을 삭제
df = df.dropna(subset=data_columns)

# StandardScaler 초기화
scaler = StandardScaler()

# 선택한 data 컬럼들에 대해 정규화를 수행
df[data_columns] = scaler.fit_transform(df[data_columns])


#df = df.iloc[1:].reset_index(drop=True)

# 정규화된 데이터프레임 확인
print(df.head())

# 필요에 따라 정규화된 데이터를 새로운 CSV 파일로 저장
df.to_csv('C:/Users/asx12/esp32/preprocessing/data/0923_304/0923_csi_304_walk_rl_scaler.csv', index=False)

#df.to_csv('C:/Users/asx12/esp32/preprocessing/data/0923_csi_walk_rlr_normalization.csv', index=False)


'''import pandas as pd
import numpy as np

# 데이터 로드 함수
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"파일 '{file_path}'에서 데이터 로드 성공")
        print("데이터 열 이름:", data.columns)  # 열 이름 출력
        return data
    except Exception as e:
        print(f"파일 로드 실패: {e}")
        return None

# 최소-최대 정규화 함수
def min_max_normalize(data, column_name):
    try:
        min_val = data[column_name].min()
        max_val = data[column_name].max()
        # 데이터 값의 스케일을 0~1로 정규화
        normalized_data = (data[column_name] - min_val) / (max_val - min_val)
        return normalized_data
    except Exception as e:
        print(f"정규화 실패: {e}")
        return None

# Z-점수 정규화 함수
def z_score_normalize(data, column_name):
    try:
        mean_val = data[column_name].mean()
        std_val = data[column_name].std()
        # 데이터의 평균과 표준편차를 사용해 정규화
        normalized_data = (data[column_name] - mean_val) / std_val
        return normalized_data
    except Exception as e:
        print(f"정규화 실패: {e}")
        return None

# 데이터 저장 함수
def save_data(data, file_path):
    try:
        data.to_csv(file_path, index=False)
        print(f"파일 '{file_path}'로 데이터 저장 성공")
    except Exception as e:
        print(f"파일 저장 실패: {e}")

# 메인 함수
def main():
    input_file = "C:\\Users\\asx12\\esp32\\preprocessing\\data\\csi_data_filtered3.csv"
    output_file = "C:\\Users\\asx12\\esp32\\preprocessing\\data\\csi_data3_normalized.csv"
    column_name = 'CSI_DATA'

    data = load_data(input_file)

    if data is not None:
        print("원본 데이터 일부:")
        print(data.head())

        if column_name in data.columns:
            data['normalized_value_minmax'] = min_max_normalize(data, column_name)
            # data['normalized_value_zscore'] = z_score_normalize(data, column_name)

            print("정규화된 데이터 일부:")
            print(data[['normalized_value_minmax']].head())

            save_data(data, output_file)
            print(f"정규화된 데이터가 '{output_file}' 파일에 저장되었습니다.")
        else:
            print(f"열 '{column_name}'이 데이터에 존재하지 않습니다.")
    else:
        print("데이터 로드 실패로 인해 정규화가 수행되지 않았습니다.")

if __name__ == "__main__":
    main()'''