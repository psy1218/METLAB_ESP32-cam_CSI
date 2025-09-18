# 🚗 METLAB 연구 프로젝트 (ESP32-CAM + CSI)

본 프로젝트는 **ESP32-CAM 기반 CSI(Channel State Information) 데이터**를 활용하여  
악천후 환경에서 자율주행 시스템의 인식 정확도를 향상시키는 것을 목표로 한다.

---

## 📌 연구 흐름

### 1. 문제 정의
- 자율주행 자동차는 **비, 눈, 안개 등 악천후 상황**에서 카메라 영상 인식 정확도가 급격히 저하됨.
- 영상 기반만으로는 한계 존재 → **무선 채널 정보(CSI)** 를 보조 신호로 활용하여 정확도 개선.

---

### 2. 데이터 수집
- **ESP32-CAM 보드** 활용  
- 공식 Espressif 저장소에서 **esp-csi 라이브러리**를 클론하여 사용  
  - 예제: `examples/get-started/csi_recv_router`  
  - 이 예제를 기반으로 **CSI 데이터 수신 및 CSV 저장** 수행
- 데이터 수집 절차:
  1. ESP-IDF 환경 설정 및 라이브러리 빌드
  2. `csi_recv_router` 예제 펌웨어 빌드 & 플래시
  3. PowerShell을 통해 CSV 파일로 CSI 데이터 저장
- 수집 데이터 예시:
  - `0923_csi_left.csv`
  - `0923_csi_mid.csv`
  - `0923_csi_right.csv`

---

### 3. 데이터 전처리
- **영상 데이터**
  - 해상도 축소
  - Grayscale 변환
  - CNN 입력 특징 추출
- **CSI 데이터**
  - Amplitude, Phase 추출
  - 잡음 제거, 결측치 처리
  - Normalization (정규화, Scaler 적용)
- **라벨링**
  - Left / Mid / Right → `1, 2, 3` 라벨 부여
  - 결측값 제거 후 학습용 데이터셋 생성

---

### 4. 특징 융합 (Feature Fusion)
- 영상 특징 + CSI 특징을 합쳐 **멀티모달 입력 구성**
- 단순 Concatenate 후 분류기에 입력

---

### 5. 학습 및 모델 설계
- **Baseline**: 영상만 사용하는 CNN
- **Proposed Model**: 영상 + CSI 융합 네트워크
- **ML 기법**: 랜덤 포레스트(Random Forest) 적용
- 학습 후 정확도 비교 수행

---

### 6. 평가 (실험 결과)
- 악천후 환경에서는:
  - 영상 단독 모델 → 정확도 감소
  - 영상 + CSI 융합 모델 → 정확도 향상, 안정적 성능 확보
- 결론: CSI 데이터는 악천후 환경에서 **영상 기반 자율주행을 보완**하는 유용한 신호임.

---

## 📊 연구 절차 흐름도

    A[ESP32-CAM 영상] --> C[Feature Fusion]
    B[ESP32-CAM CSI] --> C[Feature Fusion]
  
    C --> D[Classifier]
    D --> E[정확도 평가]



## ⚙️ 실행 과정 (ESP32-CAM 환경)

### 1. ESP-IDF 환경 설정
- ESP-IDF 설치 확인
- 환경 변수 등록 (`export.bat` 실행)

## ESP-IDF 설치
ESP-IDF는 용량이 크기 때문에 레포에 포함하지 않았습니다.  
아래 명령어로 설치하세요:
```bash
git clone -b v5.3 https://github.com/espressif/esp-idf.git esp-idf-v5.3
```

### 2. ESP-CSI 라이브러리 설치
```bash
git clone https://github.com/espressif/esp-csi.git
cd esp-csi/examples/get-started/csi_recv_router
```
### 3. 빌드 및 플래싱
```bash
idf.py set-target esp32
idf.py build
idf.py -p COM5 flash
```
### 4. 모니터링 및 데이터 저장
```bash
powershell -Command "& { idf.py -p COM5 monitor | Tee-Object -FilePath 0923_csi.csv }"
```

- COM 포트 확인 필수
- 결과 CSV 파일 자동 저장됨


## 🗂️ 데이터 처리 및 학습 파이프라인
1. CSV 데이터 수집 (`left`, `mid`, `right`)
2. 결측값 제거 및 Normalization
3. 세 구간 데이터 병합
4. 라벨링 (1=Left, 2=Mid, 3=Right)
5. Scaler 적용 후 학습 데이터 구축
6. 랜덤 포레스트(Random Forest) 학습
7. 새로운 워크 데이터 테스트 및 평가

---

## 📝 결론 및 의의
- CSI 데이터는 영상 기반 자율주행의 한계를 보완할 수 있는 유용한 보조 신호임.
- 악천후 환경에서의 인식 성능을 높여 **자율주행 시스템의 신뢰성과 안정성 향상**에 기여.

