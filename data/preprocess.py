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