import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일을 읽어옵니다
df = pd.read_csv('C:/Users/asx12/esp32/preprocessing/data/1_2_add_data.csv')

# 공백을 제거한 새로운 컬럼명을 적용합니다
df.columns = df.columns.str.strip()

# 'rssi', 'timestamp', 'label'을 제외한 컬럼 중에서 숫자형 데이터만 선택합니다
numeric_columns = df[data_columns].select_dtypes(include='number').columns

# 하나의 좌표 안에 모든 데이터를 겹쳐서 히스토그램을 그립니다
plt.figure(figsize=(10, 6))

for col in numeric_columns:
    df[col].plot(kind='hist', bins=50, alpha=0.5, label=col)

plt.title('Histogram of All Numeric Data Columns')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend(loc='upper right', fontsize='small', ncol=2)  # 범례 추가 및 조정
plt.grid(True)
plt.show()


'''import pandas as pd
import matplotlib.pyplot as plt
import math

# CSV 파일을 읽어옵니다
df = pd.read_csv('C:/Users/asx12/esp32/preprocessing/data/1_2_add_data.csv')

# 공백을 제거한 새로운 컬럼명을 적용합니다
df.columns = df.columns.str.strip()

# 'rssi', 'timestamp', 'label'을 제외한 컬럼들을 선택합니다
data_columns = [col for col in df.columns if col not in ['rssi', 'timestamp', 'label']]

# 서브플롯의 크기 계산 (한 줄에 4개씩 표시하도록 설정)
num_columns = 4
num_rows = math.ceil(len(data_columns) / num_columns)

plt.figure(figsize=(20, num_rows * 5))

# 각 컬럼에 대한 히스토그램을 서브플롯으로 그립니다
for i, col in enumerate(data_columns):
    plt.subplot(num_rows, num_columns, i + 1)
    df[col].hist(bins=50)
    plt.title(col)

plt.tight_layout()
plt.show()'''
