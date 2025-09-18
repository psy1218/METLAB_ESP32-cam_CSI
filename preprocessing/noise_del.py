import pandas as pd
import numpy as np
from scipy.signal import medfilt, butter, filtfilt

# 데이터 로드 함수
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# 저주파 대역 필터 함수
def low_pass_filter(data, column_names, cutoff_freq, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_freq / nyquist
    
    # 필터 설계
    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    # 데이터 필터링
    for column_name in column_names:
        if column_name in data.columns:
            try:
                # 데이터를 numpy array로 변환하여 필터 적용
                data[column_name] = filtfilt(b, a, data[column_name].values)
            except Exception as e:
                print(f"Error applying filter to column '{column_name}': {e}")
        else:
            print(f"Warning: Column '{column_name}' not found in data.")
            
    return data

# 중앙값 필터 함수
def median_filter(data, column_names, kernel_size):
    for column_name in column_names:
        if column_name in data.columns:
            data[column_name] = medfilt(data[column_name], kernel_size=kernel_size)
        else:
            print(f"Warning: Column '{column_name}' not found in data.")
    
    return data

# 데이터 저장 함수
def save_data(data, file_path):
    data.to_csv(file_path, index=False)

# 메인 함수
def main():
    input_file = 'C:/Users/asx12/esp32/preprocessing/data/1_csi_data.csv'
    output_file = 'C:/Users/asx12/esp32/preprocessing/data/1_2_csi_data_filtered.csv'
    
    # 필터링할 데이터 열의 이름을 문자열로 설정 (CSV 형식)
    column_names =['data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data','data']
    
    # 문자열을 리스트로 변환 (공백도 제거하고 빈 문자열 제외)
    #column_names = [name.strip() for name in column_name_str.split(',') if name.strip()]
    
    # 저주파 필터의 컷오프 주파수 설정
    cutoff_freq = 0.1
    fs = 1.0
    kernel_size = 5

    # 데이터 로드
    data = load_data(input_file)

    # 데이터프레임의 열 이름 출력
    #print("Available columns in the data:", data.columns)

    # 저주파 대역 필터 적용
    data = low_pass_filter(data, column_names, cutoff_freq, fs)

    # 중앙값 필터 적용
    #data = median_filter(data, column_names, kernel_size)

    # 필터링된 데이터를 저장
    save_data(data, output_file)
    print(f"Filtered data has been saved to '{output_file}'.")

if __name__ == "__main__":
    main()




'''import pandas as pd
import numpy as np
from scipy.signal import medfilt

# 데이터 로드 함수
def load_data(file_path):
    """
    CSV 파일에서 데이터를 불러오는 함수
    :param file_path: CSV 파일의 경로
    :return: pandas DataFrame 객체
    """
    data = pd.read_csv(file_path)
    return data

# 노이즈 제거 함수
def preprocess_data(data, column_name, kernel_size):
    """
    중앙값 필터를 사용하여 데이터에서 노이즈를 제거하는 함수
    :param data: pandas DataFrame 객체
    :param column_name: 필터링할 데이터 열의 이름
    :param kernel_size: 중앙값 필터의 커널 크기
    :return: 필터링된 데이터 (numpy 배열)
    """
    if column_name not in data.columns:
        raise ValueError(f"열 이름 '{column_name}'이(가) 데이터에 존재하지 않습니다.")
    
    # 열 데이터 타입 확인
    print(f"원본 데이터 타입: {data[column_name].dtype}")

    # 숫자형으로 변환 시도
    try:
        data[column_name] = pd.to_numeric(data[column_name], errors='coerce')  # 문자열을 NaN으로 변환
    except ValueError as e:
        print(f"데이터 변환 오류: {e}")
    
    # 변환 후 데이터 타입 확인
    print(f"변환된 데이터 타입: {data[column_name].dtype}")

    # NaN 값을 처리 (예: 앞 또는 뒤의 값으로 대체)
    data[column_name].fillna(method='ffill', inplace=True)
    data[column_name].fillna(method='bfill', inplace=True)

    # 중앙값 필터 적용
    filtered_data = medfilt(data[column_name], kernel_size=kernel_size)
    return filtered_data

# 데이터 저장 함수
def save_data(data, file_path):
    """
    필터링된 데이터를 새로운 CSV 파일로 저장하는 함수
    :param data: pandas DataFrame 객체
    :param file_path: 저장할 CSV 파일의 경로
    """
    data.to_csv(file_path, index=False)

# 메인 함수
def main():
    """
    전체 전처리 과정을 실행하는 메인 함수
    """
    # 입력 CSV 파일 경로 설정
    input_file = 'C:/Users/asx12/esp32/preprocessing/data/csi_data3.csv'
    # 출력 CSV 파일 경로 설정
    output_file = 'C:/Users/asx12/esp32/preprocessing/data/csi_data_filtered3.csv'
    # 필터링할 데이터 열의 이름 설정 (올바른 열 이름으로 수정)
    column_name = 'CSI_DATA'
    # 중앙값 필터의 커널 크기 설정 (홀수여야 함)
    kernel_size = 5

    # 데이터 로드
    data = load_data(input_file)
    
    # 데이터의 열 이름 출력
    print("열 이름:", data.columns)

    # 노이즈 제거
    filtered_data = preprocess_data(data, column_name, kernel_size)
    
    # 필터링된 데이터를 원본 데이터프레임에 'filtered_value'라는 새 열로 추가
    # data['filtered_value'] = filtered_data

    # 결과를 새로운 CSV 파일로 저장
    save_data(data, output_file)
    # 작업 완료 메시지 출력
    print(f"노이즈가 제거된 데이터가 '{output_file}' 파일에 저장되었습니다.")

# 스크립트가 직접 실행될 때만 main() 함수가 호출되도록 설정
if __name__ == "__main__":
    main()'''
