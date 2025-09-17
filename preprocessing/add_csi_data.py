import pandas as pd

# 각 CSV 파일 경로
#file1 = 'C:/Users/asx12/esp32/preprocessing/data/csidata_0903_normalized.csv'
#file2 = 'C:/Users/asx12/esp32/preprocessing/data/1_2_add_data_normalized.csv'
#file1 = r'C:\Users\asx12\esp32\preprocessing\data\csidata_0903_1_6m.csv'
#file2= r'C:\Users\asx12\esp32\preprocessing\data\1_2_add_data.csv'

#df = pd.read_csv('C:/Users/asx12/esp32/new_esp5/components/esp-idf-v5.3/git-esp-csi/esp-csi-master/examples/get-started/csi_recv_router/0923_csi_walk_rlr.csv')

file1 = 'C:/Users/asx12/esp32/new_esp5/components/esp-idf-v5.3/git-esp-csi/esp-csi-master/examples/get-started/csi_recv_router/0923_csi_304_empty.csv'
file2 = 'C:/Users/asx12/esp32/new_esp5/components/esp-idf-v5.3/git-esp-csi/esp-csi-master/examples/get-started/csi_recv_router/0923_csi_304_left.csv'
file3 = 'C:/Users/asx12/esp32/new_esp5/components/esp-idf-v5.3/git-esp-csi/esp-csi-master/examples/get-started/csi_recv_router/0923_csi_304_mid.csv'
file4 = 'C:/Users/asx12/esp32/new_esp5/components/esp-idf-v5.3/git-esp-csi/esp-csi-master/examples/get-started/csi_recv_router/0923_csi_304_right.csv'

# 각 CSV 파일을 읽어오기
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)
df4 = pd.read_csv(file4)

# 데이터프레임을 하나로 합치기
merged_df = pd.concat([df1, df2,df3,df4], ignore_index=True)

# 합친 데이터를 새로운 CSV 파일로 저장
output_file = 'C:/Users/asx12/esp32/preprocessing/data/0923_304/0923_csi_304_add.csv'
merged_df.to_csv(output_file, index=False)

print(f'Merged CSV file saved to {output_file}')
