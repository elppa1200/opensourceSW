# Recycling Image Classifier Streamlit App (오픈소스SW개론 11조)

## 1. 프로젝트 개요

이 프로젝트는 사용자가 업로드한 이미지 파일을 Streamlit 웹 화면에서 확인하고, 별도의 테스트 파일에서는 학습된 이미지 분류 모델을 이용해 재활용 품목을 예측하는 애플리케이션입니다.

- `main.py`: 이미지 업로드, 업로드 목록 표시, 이미지 선택, 학습된 모델을 불러와 이미지 분류를 수행하고 분리수거 안내를 출력하는 테스트용 Streamlit 앱입니다
- `model_utils.py`: PyTorch와 torchvision을 이용해 EfficientNet-B0 모델을 로드하고 예측을 수행하는 함수가 들어 있습니다.
- `recycling_guide.py`: 모델 예측 결과에 따라 종이, 유리, 금속, 플라스틱 분리수거 안내 문구를 Streamlit 화면에 출력합니다.
- `model/efficientnet_b0_v2.pth`: `main.py`에서 사용하는 학습된 모델 가중치 파일입니다.

AI Hub의 데이터로 제작되었습니다.
[https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&amp;topMenu=100&amp;dataSetSn=71385](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71385)

## 2. 코드의 용도

이 코드는 이미지 기반 재활용 분류 앱을 만들기 위한 Streamlit 앱입니다.

사용자는 이미지 파일을 업로드할 수 있고, 업로드한 이미지 목록 중 하나를 선택하여 중앙 화면에서 미리 볼 수 있습니다. `main.py`를 실행하면 선택된 이미지를 모델에 입력하여 `glass`, `metal`, `paper`, `plastic` 중 하나로 분류하고, 해당 분류 결과에 맞는 분리수거 안내를 표시합니다.

## 3. 주요 기능

### 3.1 이미지 업로드

- `png`, `jpg`, `jpeg` 형식의 이미지 업로드를 지원합니다.
- 여러 이미지를 한 번에 업로드할 수 있습니다.
- 업로드된 이미지는 Streamlit `session_state`에 저장됩니다.
- 최대 `10`개의 이미지만 유지하며, 개수를 초과하면 오래된 이미지부터 제거됩니다.

### 3.2 이미지 선택 및 미리보기

- 업로드된 이미지는 사이드바에 목록 형태로 표시됩니다.
- 사용자는 사이드바에서 이미지를 선택할 수 있습니다.
- 선택된 이미지는 중앙 영역에 리사이즈된 미리보기 형태로 출력됩니다.
- 사이드바에서 현재 선택된 이미지를 삭제할 수 있습니다.

### 3.3 모델 예측 기능

- `model/efficientnet_b0_v2.pth` 파일에서 학습된 모델 가중치를 불러옵니다.
- `model_utils.py`의 `load_trained_model()` 함수가 모델을 생성하고 가중치를 로드합니다.
- `predict()` 함수가 선택된 이미지를 전처리한 뒤 모델 예측을 수행합니다.
- 예측 클래스는 다음 네 가지입니다.
  - `glass`
  - `metal`
  - `paper`
  - `plastic`

### 3.4 분리수거 안내 출력

- 모델 예측 결과를 `recycling_guide.py`의 `render_recycling_guide()` 함수에 전달합니다.
- 예측된 품목에 따라 분리수거 방법을 화면에 표시합니다.
- 모델 예측이 실패한 경우 테스트용 선택 상자를 통해 분류 결과를 수동으로 선택할 수 있습니다.

## 4. 실행 환경

권장 실행 환경은 다음과 같습니다.

- < Python 3.13
- Streamlit
- Pillow
- PyTorch
- torchvision

## 5. 설치 방법

### 5.1 저장소 폴더로 이동

PowerShell 또는 터미널에서 프로젝트 폴더로 이동합니다.

### 5.2 기본 의존성 설치 (Python 3.13 이하 버전으로)

```powershell
pip install -r requirements.txt
```

### 5.3 기본 이미지 업로드 앱 실행

```powershell
streamlit run main.py
```

실행 후 브라우저에서 Streamlit 앱이 열립니다. 브라우저가 자동으로 열리지 않으면 터미널에 표시되는 로컬 주소로 접속합니다.

## 7. 사용 방법

1. 앱을 실행합니다.
2. 화면의 이미지 업로드 영역에서 `png`, `jpg`, `jpeg` 파일을 선택합니다.
3. 업로드 버튼을 누릅니다.
4. 사이드바에서 업로드된 이미지 목록을 확인합니다.
5. 사이드바의 이미지를 클릭하여 현재 이미지를 변경합니다.
6. 중앙 화면에서 선택된 이미지 미리보기를 확인합니다.
7. 이미지 아래쪽에서 모델 예측 결과와 분리수거 안내를 확인합니다.
8. 필요하면 사이드바의 삭제 버튼으로 현재 선택된 이미지를 삭제합니다.

## 8. 파일 구조

```txt
opensourceSW/
├── main.py
├── model_utils.py
├── recycling_guide.py
├── requirements.txt
├── README.md
├── data/
    └── preprocess.py
└── model/
    ├── efficientnet_b0_v2.pth
    ├── evaluate.py
    └── train.py
```

## 9. 주요 파일 설명

### `main.py`

기능:

- 페이지 설정
- 이미지 업로드
- 업로드 이미지 목록 관리
- 사이드바 이미지 선택
- 이미지 삭제
- 선택 이미지 미리보기
- 모델 로드
- 모델 예측
- 분리수거 안내 출력

### `model_utils.py`

모델 로드와 예측을 담당합니다.

주요 구성:

- `classes = ['glass', 'metal', 'paper', 'plastic']`
- `load_trained_model(model_path)`
- `predict(image, model, device)`

모델은 `torchvision.models.efficientnet_b0(weights=None)` 기반으로 생성되며, 마지막 분류기를 네 개 클래스에 맞게 변경한 뒤 `.pth` 가중치를 로드합니다.

### `recycling_guide.py`

분류 결과에 맞는 분리수거 안내를 출력합니다.

주요 구성:

- 클래스명 정규화
- 클래스별 안내 문구 저장
- Streamlit 화면 출력 함수 제공
