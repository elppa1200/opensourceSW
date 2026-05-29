# opensourceSW
쓰레기 사진을 입력받아 어떤 분류의 쓰레기인지 인식하고 알려주는 웹사이트입니다.

AI Hub의 데이터로 제작되었습니다.

https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71385

# 목표

- 사용자 업로드 이미지 AI 모델 분석
- 플라스틱, 종이, 금속, 유리 등 주요 분리배출 카테고리를 분류
- 예측 결과와 신뢰도 화면에 보기 쉽게 표시
- 결과별 분리배출 안내 문구 함께 제공

# Required

- CUDA 11
- torch: 2.7.1+cu118
- torchvision: 0.22.1+cu118
- Streamlit
