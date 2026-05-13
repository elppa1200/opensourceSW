import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# 경로 설정
VAL_DIR = r"D:\waste_dataset\processed\val"
MODEL_PATH = r"D:\waste_dataset\model\efficientnet_b0.pth"

# 설정
BATCH_SIZE = 32
NUM_CLASSES = 4

# GPU 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"사용 디바이스: {device}")

# 데이터 전처리
val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# 데이터셋 및 로더
val_dataset = datasets.ImageFolder(VAL_DIR, transform=val_transform)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# 클래스 목록
class_names = val_dataset.classes
print(f"클래스 목록: {class_names}")
print(f"검증 데이터: {len(val_dataset)}장")