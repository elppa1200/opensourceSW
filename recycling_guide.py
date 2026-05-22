"""
분리수거 클래스별 안내문을 관리하고 Streamlit 화면에 출력하는 모듈입니다.

main.py에서는 AI 모델이 예측한 클래스명만 이 모듈에 넘기면 됩니다.
예: render_recycling_guide("paper")
"""

import streamlit as st


# AI 모델/데이터셋에서 사용하는 영문 클래스명을 화면 표시용 한글명으로 매핑한다.
# 만약 분류 클래스가 늘어나거나 줄어들면 여기에 '분류 클래스명 : 한글명' 을 추가하면 된다.
CLASS_DISPLAY_NAMES = {
    "paper": "종이(Paper)",
    "glass": "유리(Glass)",
    "metal": "금속/캔(Metal)",
    "plastic": "플라스틱(Plastic)",
}


# 클래스별 분리수거 안내문
# 각 클래스마다 제목(title), 요약(summary), 분류 단계(steps) 등으로 구성되어있다.
RECYCLING_GUIDES = {
    "paper": {
        "title": "종이류 분리수거 안내",
        "summary": "종이는 물기와 이물질을 제거한 뒤 가능한 한 펼치거나 묶어서 배출하세요.",
        "steps": [
            "음식물, 기름, 테이프, 스티커 등 이물질을 제거합니다.",
            "상자류는 접어서 부피를 줄입니다.",
            "코팅지, 영수증, 오염된 종이는 일반쓰레기로 배출합니다.",
        ],
    },
    "glass": {
        "title": "유리류 분리수거 안내",
        "summary": "유리병은 내용물을 비우고 헹군 뒤 뚜껑을 분리해서 배출하세요.",
        "steps": [
            "병 안의 내용물을 완전히 비우고 가볍게 헹굽니다.",
            "뚜껑, 라벨 등 다른 재질은 가능한 한 분리합니다.",
            "깨진 유리, 거울, 도자기, 내열유리는 재활용 유리병과 따로 배출합니다.",
        ],
    },
    "metal": {
        "title": "금속/캔류 분리수거 안내",
        "summary": "캔과 금속류는 내용물을 비우고 가능한 한 압착해서 배출하세요.",
        "steps": [
            "음료캔, 통조림캔 내부를 비우고 헹굽니다.",
            "플라스틱 뚜껑이나 라벨이 있으면 분리합니다.",
            "부탄가스, 스프레이 캔은 반드시 구멍을 뚫거나 완전히 비운 뒤 배출 기준에 맞게 버립니다.",
        ],
    },
    "plastic": {
        "title": "플라스틱류 분리수거 안내",
        "summary": "플라스틱 용기는 내용물을 비우고 헹군 뒤 라벨과 뚜껑을 가능한 한 분리하세요.",
        "steps": [
            "용기 안의 내용물을 비우고 물로 헹굽니다.",
            "라벨, 뚜껑, 펌프 등 다른 재질은 가능한 한 분리합니다.",
            "오염이 심하거나 복합재질이라 분리가 어려운 경우 일반쓰레기로 배출합니다.",
        ],
    },
}


def normalize_class_name(class_name):
    """AI 모델이 반환한 클래스명을 내부 표준 클래스명으로 변환합니다."""
    if class_name is None:
        return None

    # 넘겨진 클래스 문자열을 공백 제거 및 소문자로 변환한다.
    normalized = str(class_name).strip().lower()

    alias_map = {
        "paper": "paper",
        "종이": "paper",
        "glass": "glass",
        "유리": "glass",
        "metal": "metal",
        "can": "metal",
        "cans": "metal",
        "금속": "metal",
        "캔": "metal",
        "plastic": "plastic",
        "plastics": "plastic",
        "플라스틱": "plastic",
    }

    return alias_map.get(normalized)


def get_recycling_guide(class_name):
    """클래스명에 맞는 안내문 딕셔너리를 반환합니다."""

    normalized = normalize_class_name(class_name)
    if normalized is None:
        return None

    guide = RECYCLING_GUIDES.get(normalized)
    if guide is None:
        return None

    return {
        "class_name": normalized,
        "display_name": CLASS_DISPLAY_NAMES[normalized],
        **guide,
    }


def render_recycling_guide(class_name, confidence=None):
    """Streamlit 화면에 분리수거 안내문을 출력합니다."""
    guide = get_recycling_guide(class_name)

    #
    if guide is None:
        st.warning("분류 결과에 맞는 분리수거 안내문을 찾을 수 없습니다.")
        return

    confidence_text = ""
    if confidence is not None:
        confidence_text = f" · 예측 확률: {confidence * 100:.1f}%"

    # 화면에 나오는 분류 안내문 디자인
    st.markdown(
        f"""
        <div style="
            margin-top: 24px;
            padding: 22px 26px;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
            background-color: #f9fafb;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        ">
            <div style="font-size: 18px; color: #4b5563; margin-bottom: 6px;">
                분류 결과: <b>{guide['display_name']}</b>{confidence_text}
            </div>
            <div style="font-size: 24px; font-weight: 700; margin-bottom: 10px;">
                {guide['title']}
            </div>
            <div style="font-size: 17px; color: #374151; line-height: 1.6;">
                {guide['summary']}
            </div>
        </div>
        """,
        # html 태그를 이용해 렌더링이 가능하도록 허용함
        unsafe_allow_html=True,
    )
    # 자세한 배출 방법을 드롭다운을 이용해서 보여준다.
    with st.expander("자세한 배출 방법 보기", expanded=True):
        for step in guide["steps"]:
            st.write(f"- {step}")
