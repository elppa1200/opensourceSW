import os
import json
import shutil
import random
from collections import defaultdict

# 경로 설정
TRAIN_IMG_DIR = r"D:\waste_dataset\Training\images_extracted"
TRAIN_LABEL_DIR = r"D:\waste_dataset\Training\labels_extracted"
OUTPUT_DIR = r"D:\waste_dataset\processed"

# 어플리케이션 데이터 경로 (종이/유리 보강용)
APP_IMG_DIR = r"D:\waste_dataset\TS_application_C\307.생활폐기물 데이터 활용ㆍ환류\01-1.정식개방데이터\Training\01.원천데이터"
APP_LABEL_DIR = r"D:\waste_dataset\TL_application_C\307.생활폐기물 데이터 활용ㆍ환류\01-1.정식개방데이터\Training\02.라벨링데이터"

# 보강할 카테고리 (종이/유리만)
BOOST_CATEGORIES = ["paper", "glass"]

# Validation 경로 추가
VAL_IMG_DIR = r"D:\waste_dataset\Validation\images_extracted"
VAL_LABEL_DIR = r"D:\waste_dataset\Validation\labels_extracted"

# 클래스별 샘플링 수 (클래스 불균형 방지)
SAMPLES_PER_CLASS = 10000

# AI Hub 라벨 -> 4개 카테고리 매핑
# 이물질 포함 라벨도 같은 카테고리로 통합
LABEL_MAP = {
    # 종이
    "c_1": "paper", "c_1_01": "paper",
    "c_2_01": "paper", "c_2_02": "paper", "c_2_02_01": "paper",
    # 금속
    "c_3": "metal", "c_3_01": "metal",
    # 유리
    "c_4_01_02": "glass", "c_4_02_01_02": "glass",
    "c_4_02_02_02": "glass", "c_4_02_03_02": "glass",
    "c_4_03": "glass", "c_4_03_01": "glass",
    # 플라스틱
    "c_5_02": "plastic", "c_5_02_01": "plastic",
    "c_6": "plastic", "c_6_01": "plastic",
    "c_7": "plastic", "c_7_01": "plastic",
}

def build_training(): # build_dataset -> build_training 으로 함수명 변경
    """ 학습 데이터 전처리 함수
    - JSON 라벨 파일 읽어서 이미지-카테고리 매핑
    - 클래스별로 최대 10,000장 샘플링
    - processed/train 폴더에 복사
    """
    class_images = defaultdict(list)

    print("라벨 파일 읽는 중...")
    for json_file in os.listdir(TRAIN_LABEL_DIR):
        if not json_file.endswith(".json"):
            continue

        json_path = os.path.join(TRAIN_LABEL_DIR, json_file)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        image_name = data.get("Image", "")
        objects = data.get("objects", [])

        if not objects:
            continue

        # 첫 번째 객체의 클래스명으로 카테고리 결정
        class_name = objects[0].get("class_name", "")

        # 4개 카테고리로 매핑
        category = LABEL_MAP.get(class_name)
        if category is None:
            continue

        image_path = os.path.join(TRAIN_IMG_DIR, image_name)
        if os.path.exists(image_path):
            class_images[category].append(image_path)

    # 카테고리별 현황 출력
    print("\n카테고리별 이미지 수:")
    for cat, imgs in class_images.items():
        print(f"  {cat}: {len(imgs)}장")

    # 클래스별 10,000장 샘플링 후 복사
    print(f"\n클래스별 {SAMPLES_PER_CLASS}장 샘플링 및 복사 중...")
    for category, images in class_images.items():
        out_dir = os.path.join(OUTPUT_DIR, "train", category)
        os.makedirs(out_dir, exist_ok=True)

        # 최대 10,000장 랜덤 샘플링
        sampled = random.sample(images, min(SAMPLES_PER_CLASS, len(images)))
        for img_path in sampled:
            shutil.copy(img_path, out_dir)

        print(f"  {category}: {len(sampled)}장 복사 완료")

    print("\n전처리 완료!")
    print(f"저장 위치: {OUTPUT_DIR}")


# Validation 처리 함수 추가
def build_validation():
    """ 검증 데이터 전처리 함수
    - JSON 라벨 파일 읽어서 이미지-카테고리 매핑
    - 전체 검증 데이터 복사 (샘플링 없음)
    - processed/val 폴더에 복사
    """
    class_images = defaultdict(list)

    print("Validation 라벨 파일 읽는 중...")
    for json_file in os.listdir(VAL_LABEL_DIR):
        if not json_file.endswith(".json"):
            continue

        json_path = os.path.join(VAL_LABEL_DIR, json_file)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        image_name = data.get("Image", "")
        objects = data.get("objects", [])

        if not objects:
            continue

        class_name = objects[0].get("class_name", "")
        category = LABEL_MAP.get(class_name)
        if category is None:
            continue

        image_path = os.path.join(VAL_IMG_DIR, image_name)
        if os.path.exists(image_path):
            class_images[category].append(image_path)

    print("\nValidation 카테고리별 이미지 수:")
    for cat, imgs in class_images.items():
        print(f"  {cat}: {len(imgs)}장")

    print("\nValidation 이미지 복사 중...")
    for category, images in class_images.items():
        out_dir = os.path.join(OUTPUT_DIR, "val", category)
        os.makedirs(out_dir, exist_ok=True)

        for img_path in images:
            shutil.copy(img_path, out_dir)

        print(f"  {category}: {len(images)}장 복사 완료")

    print("\nValidation 전처리 완료!")

def build_app_boost():
    """어플리케이션 데이터에서 종이/유리만 추가 수집하는 함수
    - 실내형분류기 데이터의 종이/유리 부족분 보강
    - processed/train 폴더에 추가 복사
    """
    class_images = defaultdict(list)

    print("어플리케이션 라벨 파일 읽는 중...")
    for root, dirs, files in os.walk(APP_LABEL_DIR):
        for json_file in files:
            if not json_file.endswith(".json"):
                continue
            json_path = os.path.join(root, json_file)
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            image_name = data.get("Image", "")
            objects = data.get("objects", [])

            if not objects:
                continue

            class_name = objects[0].get("class_name", "")
            category = LABEL_MAP.get(class_name)

            # 종이/유리만 수집
            if category not in BOOST_CATEGORIES:
                continue

        # C_1~C_5 폴더에서 이미지 찾기
        for c_folder in ["TS_어플리케이션_C_1", "TS_어플리케이션_C_2",
                         "TS_어플리케이션_C_3", "TS_어플리케이션_C_4",
                         "TS_어플리케이션_C_5"]:
            image_path = os.path.join(APP_IMG_DIR, c_folder, image_name)
            if os.path.exists(image_path):
                class_images[category].append(image_path)
                break

    print("\n어플리케이션 데이터 카테고리별 이미지 수:")
    for cat, imgs in class_images.items():
        print(f"  {cat}: {len(imgs)}장")

    print("\n어플리케이션 데이터 복사 중...")
    for category, images in class_images.items():
        out_dir = os.path.join(OUTPUT_DIR, "train", category)
        os.makedirs(out_dir, exist_ok=True)

        # 최대 10,000장 추가 (기존 데이터 포함 총 20,000장)
        sampled = random.sample(images, min(10000, len(images)))
        for img_path in sampled:
            shutil.copy(img_path, out_dir)

        print(f"  {category}: {len(sampled)}장 추가 완료")

    print("\n어플리케이션 데이터 보강 완료!")

if __name__ == "__main__":
    build_training()    # build_dataset -> build_training 으로 함수명 변경
    build_validation()
    build_app_boost()   # 종이/유리 보강