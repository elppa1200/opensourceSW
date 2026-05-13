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