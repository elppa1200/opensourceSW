import os
import json
import shutil
import random
from collections import defaultdict

# 경로 설정
TRAIN_IMG_DIR = r"D:\waste_dataset\Training\images_extracted"
TRAIN_LABEL_DIR = r"D:\waste_dataset\Training\labels_extracted"
OUTPUT_DIR = r"D:\waste_dataset\processed"

# Validation 경로 추가
VAL_IMG_DIR = r"D:\waste_dataset\Validation\images_extracted"
VAL_LABEL_DIR = r"D:\waste_dataset\Validation\labels_extracted"

SAMPLES_PER_CLASS = 10000

# 4개 카테고리 매핑
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

def build_dataset():
    # 카테고리별 이미지 목록 수집
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

        # 첫 번째 object의 class_name 사용
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

# Validaiton 처리 함수 추가
def build_validation():
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

# 클래스별 10,000장 샘플링 후 복사
    print(f"\n클래스별 {SAMPLES_PER_CLASS}장 샘플링 및 복사 중...")
    for category, images in class_images.items():
        out_dir = os.path.join(OUTPUT_DIR, "train", category)
        os.makedirs(out_dir, exist_ok=True)

        sampled = random.sample(images, min(SAMPLES_PER_CLASS, len(images)))
        for img_path in sampled:
            shutil.copy(img_path, out_dir)

        print(f"  {category}: {len(sampled)}장 복사 완료")

    print("\n전처리 완료!")
    print(f"저장 위치: {OUTPUT_DIR}")

if __name__ == "__main__":
    build_dataset()
    build_validation()