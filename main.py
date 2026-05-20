import streamlit as st
from PIL import Image
from streamlit_image_select import image_select
from io import BytesIO

from recycling_guide import render_recycling_guide

# PIL(Python Imaging Library)은 이미지 처리 라이브러리입니다. 
# 이미지를 열고, 변환하고, 조작하는 기능을 제공합니다. --> image.open, .convert, .resize 등

# streamlit_image_select는 Streamlit에서 이미지 선택 기능을 제공하는 라이브러리입니다.
# 사이드 바에 있는 이미지 목록 중 하나를 선택해서 중앙에 나오도록 하는 기능을 구현하기 위해 사용됩니다.

# BytesIO는 바이트 데이터를 메모리에서 파일처럼 다룰 수 있게 해주는 클래스입니다.
# 이미지 데이터를 디스크에 저장하지 않고 메모리에서 바로 처리하기 위해 사용됩니다.

# 프로그램 전체 구조는 사용자가 버튼 클릭, 입력, 파일 업로드 같은 이벤트 발생 시
# Streamlit이 다시 main.py 전체를 처음부터 실행하는 방식으로 작동한다.
# 그래서 세션 상태를 이용해서 이미지 리스트, 선택된 이미지 인덱스, 업로더 키, 사이드바 키 같은 데이터를 유지한다.
# 세션이란 사용자와 웹 애플리케이션 간 연결 상태를 의미한다.
# 그래서 각 사용자 마다 고유한 세션이 생성되고, 세션 상태는 그 사용자에 대한 데이터를 저장하는 공간이다.
st.set_page_config(page_title="이미지 업로드 페이지", layout="wide")

st.title("이미지 업로드 확인 페이지")

MAX_IMAGES = 10
PREVIEW_WIDTH = 500
SIDEBAR_PREVIEW_WIDTH = 180

# 첫 연결 시 세션 상태 초기화
# 세션 상태는 프로그램 처음 시작에만 초기화 되고, 이후에는 유지된다.
# 그래서 아래 코드는 프로그램 시작시 한번만 실행된다.
if "images" not in st.session_state:
    st.session_state.images = []

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "sidebar_key" not in st.session_state:
    st.session_state.sidebar_key = 0

# 이미지를 로드하는 함수
def load_image(image_data):
    
    # main.py는 사용자가 업로드한 이미지를 메모리에서 계속 유지하기에
    # 파일 경로 혹은 파일 객체를 필요로 하는 open을 위해서
    # BytesIO로 바이트 데이터를 메모리 파일 객체로 변환하여 이미지를 로드한다.
    image = Image.open(BytesIO(image_data["bytes"]))
    # 이미지 처리 관련 모듈 streamlit_image_select이 내부에서 강제로 JPEG로 변환하여
    # 이미지를 저장한다. JPEG는 RGB까지만 지원하기 때문에 PNG의 RGBA에서 A가 제거되어 RGB로 저장해야한다.
    # 아래 코드는 RGBA인 경우 RGB로 변환하는 코드이다.
    if image.mode != "RGB":
        image = image.convert("RGB")

    return image


def make_resized_preview(image, max_width):
    # 미리보기용 이미지를 만들기 위해서 원본에서 복사한 것을 preview로 사용한다.
    preview = image.copy()
    width, height = preview.size

    # 개발자가 정한 최대 너비보다 원본 이미지가 더 넓은 경우에만 리사이즈한다.
    if width > max_width:
        # 원본 비율을 유지하면서 리사이즈 하기 위해 너비 간 비율을 높이에도 적용한다.
        new_height = int(height * (max_width / width))
        preview = preview.resize((max_width, new_height))

    return preview


# -----------------------------
# 이미지 가져오기 / 실제 업로드
# -----------------------------
# st.form은 웹 페이지 상에 입력 창을 띄어준다.
# 이는 업로드 버튼과 파일 업로더를 하나의 폼으로 묶는 역할도 한다.
with st.form("upload_form"):
    # st.file_uploader는 사용자가 파일을 업로드할 수 있게 해주는 Streamlit 컴포넌트입니다.
    # "이미지 가져오기"라는 글자가 들어간 버튼이다.
    # st.file_uploader는 여러 파일 객체들이 담긴 리스트를 반환한다.
    # 파일 객체는 UploadedFile 객체로, 파일명, 타입, 크기, 그리고 파일 내용을 바이트 형태로 담고 있다.
    # 이를 모두 uploaded_files라는 리스트에 저장한다.
    uploaded_files = st.file_uploader(
        "이미지 가져오기",
        type=["png", "jpg", "jpeg"],
        # 다수의 파일 업로드를 허용한다.
        accept_multiple_files=True,
        # key는 Streamlit 컴포넌트의 고유 식별자 역할을 한다. 이를 통해 컴포넌트의 상태를 관리할 수 있다.
        # key가 필요한 이유는 업로드 버튼을 누른 후 입력창을 초기화 하기 위해서 이다.
        key=f"uploader_{st.session_state.uploader_key}"
    )
    # st.form_submit_button은 폼 내에서 제출 버튼을 만들어준다. 
    # 사용자가 이 버튼을 클릭하면 upload_button이 True가 된다.
    upload_button = st.form_submit_button("이미지 업로드")

# 사용자가 업로드 버튼을 클릭했고, 업로드된 파일이 있는 경우에만 아래 코드가 실행된다.
if upload_button and uploaded_files:
    for file in uploaded_files:
        # 업로드된 파일 객체에서 필요한 정보를 추출하여 세션 상태의 이미지 리스트에 추가한다.
        st.session_state.images.append({
            "name": file.name,
            "type": file.type,
            "size": file.size,
            "bytes": file.getvalue(),
            # 학습 모델이 분류한 클래스와 confidence를 저장하기 위한 key,value쌍이다.
            # 기본값으로 None이 저장된다. 이후에 학습모델로 인해 갱신된다.
            "predicted_class" : None,
            "confidence" : None
        })

    # 이미지 리스트는 큐 구조로 저장한다.
    # 새로운 이미지는 리스트의 끝에 추가되고, 오래된 이미지는 리스트의 앞에서 제거된다.

    # 최대 MAX_IMAGES 개수만큼(현재는 10개) 유지한다.
    # 만약 이미지를 추가하려 할 때 허용 개수를 초과하면 가장 오래된 이미지부터 삭제
    if len(st.session_state.images) > MAX_IMAGES:
        st.session_state.images = st.session_state.images[-MAX_IMAGES:]

    # 디폴트 선택: 가장 최근 이미지
    st.session_state.selected_index = len(st.session_state.images) - 1

    # 입력창 초기화
    st.session_state.uploader_key += 1

    # 사이드바 강제 갱신
    st.session_state.sidebar_key += 1

    # 페이지 다시 갱신
    st.rerun()


# -----------------------------
# 선택된 이미지 표시
# -----------------------------
if st.session_state.images:
    # 아래 두 if문은 선택된 이미지가 없거나 리스트 범위를 벗어나서 선택하는 경우
    # 에러 발생을 막기 위해 디폴트로 가장 최근 이미지를 선택하도록 하는 코드이다.
    if st.session_state.selected_index is None:
        st.session_state.selected_index = len(st.session_state.images) - 1

    if st.session_state.selected_index >= len(st.session_state.images):
        st.session_state.selected_index = len(st.session_state.images) - 1

    #display_images는 사이드바에 최근에 업로드 된 이미지가 위에 오도록 뒤집힌 리스트이다.
    display_images = list(reversed(st.session_state.images))

    #sidebar_images는 display_images의 이미지들을 사이드바에 맞게 리사이즈한 이미지 리스트이다.
    sidebar_images = [
        make_resized_preview(load_image(img), max_width=SIDEBAR_PREVIEW_WIDTH)
        for img in display_images
    ]
    #captions는 이미지 아래 정보를 표시하기 위한 리스트이다.
    captions = [
        f"{i + 1}. {img['name']}"
        for i, img in enumerate(display_images)
    ]

    
    display_selected_index = (
        len(st.session_state.images) - 1 - st.session_state.selected_index
    )
    # 사이드 바 부분
    with st.sidebar:
        st.title("업로드된 이미지")
        # image_select 컴포넌트는 사이드바에 이미지 목록을 보여주고
        # 사용자가 하나를 선택할 수 있게 해준다.
        # 가장 위에서 부터 0,1,2,... 순서로 index가 매겨진다.
        selected_display_index = image_select(
            label="이미지를 클릭해서 선택하세요",
            images=sidebar_images,
            captions=captions,
            index=display_selected_index,
            return_value="index",
            # 여기서 key도 사이드바에서 이미지 삭제 시 상태를 초기화 하기 위해서 사용된다.
            # key값이 변경되면 해당 컴포넌트가 강제로 다시 렌더링 된다.
            key=f"sidebar_image_select_{st.session_state.sidebar_key}"
        )

        # 사이드바 표시용 index를 실제 저장 index로 변환
        real_index = len(st.session_state.images) - 1 - selected_display_index
        st.session_state.selected_index = real_index

        # 시각적으로 구분선을 보여주는 함수이다.
        st.divider()

        selected_image_data = st.session_state.images[st.session_state.selected_index]
        st.write("현재 선택:", selected_image_data["name"])

        # 아래부터는 이미지 삭제 부분이다.
        if st.button("현재 선택 이미지 삭제"):
            del st.session_state.images[st.session_state.selected_index]

            #이미지가 하나도 없는 경우 index를 None으로 설정
            if not st.session_state.images:
                st.session_state.selected_index = None
            else:
                # 삭제 후 가장 최근 이미지 선택
                st.session_state.selected_index = len(st.session_state.images) - 1

            # 사이드바 강제 갱신
            st.session_state.sidebar_key += 1

            st.rerun()

    # -----------------------------
    # 중앙: 선택된 이미지 리사이즈 미리보기
    # -----------------------------
    selected_image_data = st.session_state.images[st.session_state.selected_index]
    selected_image = load_image(selected_image_data)
    preview_image = make_resized_preview(selected_image, max_width=PREVIEW_WIDTH)

    st.subheader("선택된 이미지 미리보기")
    # st.columns은 페이지를 여러 개의 열로 나누는 Streamlit 함수입니다.
    # 아래는 3개의 열을 이용하여 좌, 중, 우를[1, 3, 1]이라는 비율로 만들고 있습니다.
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        # 리사이즈 된 미리보기 이미지를 캡션 달아서 중앙에 출력한다.
        st.image(
            preview_image,
            caption=selected_image_data["name"]
        )
        #=================================================
        #여기서 부분에 AI 모델을 호출하여 분류한뒤 결과물을 아래와 같이 저장해주면 됩니다.
        #selected_image_data["predicted_class"] = "Paper"
        #selected_image_data["confidence"] = 0.98


        # -------------------------------------------------------
        # AI 모델 예측 결과에 따른 분리수거 안내문 출력 부분
        # -------------------------------------------------------
        

        #현재 선택된 이미지에서 에측 클래스와 신뢰도를 가져온다.
        predicted_class = selected_image_data.get("predicted_class")
        confidence = selected_image_data.get("confidence")

        # 아직 모델 통합 전에도 화면 확인이 가능하도록 임시 선택 UI 제공
        if predicted_class is None:
            predicted_class = st.selectbox(
                "모델 통합 전 테스트용 분류 결과 선택",
                options=["paper", "glass", "metal", "plastic"],
                index=0,
                key=f"mock_class_{st.session_state.selected_index}",
            )

        render_recycling_guide(predicted_class, confidence)

else:
    st.info("아직 업로드된 이미지가 없습니다.")