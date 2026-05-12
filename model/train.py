import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# 경로 설정
TRAIN_DIR = r"D:\waste_dataset\processed\train"
VAL_DIR = r"D:\waste_dataset\processed\val"
MODEL_SAVE_PATH = r"D:\waste_dataset\model\efficientnet_b0.pth"

# 하이퍼파라미터
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001
NUM_CLASSES = 4

# GPU 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"사용 디바이스: {device}")