import pandas as pd
import numpy as np

# 데이터 불러오기
df = pd.read_csv('C:/Users/asx12/esp32/preprocessing/data/1_3_csi_data_normalized.csv')

# rssi, timestamp, label 열을 제외한 나머지 열 선택
data_columns = [col for col in df.columns if col not in ['rssi', 'timestamp', 'label']]
data = df[data_columns]

# 특징 추출 함수 정의
def extract_features(data):
    features = {}
    
    # 각 열별로 특징 추출
    for col in data.columns:
        features[f'{col}_mean'] = data[col].mean()          # 평균
        features[f'{col}_std'] = data[col].std()            # 표준편차
        features[f'{col}_min'] = data[col].min()            # 최소값
        features[f'{col}_max'] = data[col].max()            # 최대값
        features[f'{col}_median'] = data[col].median()      # 중위값
        features[f'{col}_range'] = data[col].max() - data[col].min()  # 범위 (최대값 - 최소값)
        features[f'{col}_iqr'] = data[col].quantile(0.75) - data[col].quantile(0.25)  # 사분위 범위

    return features

# 전체 데이터프레임에 대해 특징 추출
features = extract_features(data)

# 추출된 특징을 데이터프레임으로 변환
features_df = pd.DataFrame([features])

# 특징 추출된 데이터를 새로운 CSV 파일로 저장
output_file_path = 'C:/Users/asx12/esp32/preprocessing/data/1_csi_features.csv'
features_df.to_csv(output_file_path, index=False)

print(f'특징 추출된 데이터를 {output_file_path}에 저장했습니다.')


'''import pandas as pd
import numpy as np

# 데이터 로드 함수
def load_data(file_path):
    try:
        # 첫 번째 행을 열 이름으로 설정하고 CSV 파일 로드
        data = pd.read_csv(file_path, header=0)
        print(f"파일 '{file_path}'에서 데이터 로드 성공")
        print("데이터 열 이름:", data.columns)  # 열 이름 출력
        return data
    except Exception as e:
        print(f"파일 로드 실패: {e}")
        return None

# 기초 통계량 추출 함수
def extract_basic_statistics(data, column_name):
    try:
        # 열이 숫자형인지 확인하고, 숫자형으로 변환
        data[column_name] = pd.to_numeric(data[column_name], errors='coerce')
        mean_val = data[column_name].mean()
        std_val = data[column_name].std()
        min_val = data[column_name].min()
        max_val = data[column_name].max()
        
        stats = {
            'mean': mean_val,
            'std': std_val,
            'min': min_val,
            'max': max_val
        }
        return stats
    except Exception as e:
        print(f"기초 통계량 추출 실패: {e}")
        return None

# 이동 평균 추출 함수
def extract_moving_average(data, column_name, window_size):
    try:
        # 열이 숫자형인지 확인하고, 숫자형으로 변환
        data[column_name] = pd.to_numeric(data[column_name], errors='coerce')
        data[f'moving_average_{window_size}'] = data[column_name].rolling(window=window_size).mean()
        return data
    except Exception as e:
        print(f"이동 평균 추출 실패: {e}")
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
    input_file = "C:\\Users\\asx12\\esp32\\preprocessing\\data\\csi_data3_normalized.csv"
    output_file = "C:\\Users\\asx12\\esp32\\preprocessing\\data\\csi_data_features.csv"
    column_name = 'CSI_DATA'
    window_size = 5  # 이동 평균의 윈도우 크기 설정

    data = load_data(input_file)

    if data is not None:
        print("원본 데이터 일부:")
        print(data.head())

        if column_name in data.columns:
            # 기초 통계량 추출
            stats = extract_basic_statistics(data, column_name)
            if stats:
                print("기초 통계량:")
                print(stats)
            
            # 이동 평균 추출
            data = extract_moving_average(data, column_name, window_size)
            
            print("특징이 추가된 데이터 일부:")
            print(data.head())
            
            save_data(data, output_file)
            print(f"특징이 추출된 데이터가 '{output_file}' 파일에 저장되었습니다.")
        else:
            print(f"열 '{column_name}'이 데이터에 존재하지 않습니다.")
    else:
        print("데이터 로드 실패로 인해 특징 추출이 수행되지 않았습니다.")

if __name__ == "__main__":
    main()
'''