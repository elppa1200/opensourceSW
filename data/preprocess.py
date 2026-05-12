import os
import json
import shutil
import random
from collections import defaultdict

# 경로 설정
TRAIN_IMG_DIR = r"D:\waste_dataset\Training\images_extracted"
TRAIN_LABEL_DIR = r"D:\waste_dataset\Training\labels_extracted"
OUTPUT_DIR = r"D:\waste_dataset\processed"

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