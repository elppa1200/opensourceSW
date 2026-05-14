import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAL_DIR = os.path.join(BASE_DIR, "..", "data", "processed", "val")
MODEL_PATH = os.path.join(BASE_DIR, "efficientnet_b0.pth")

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

# 모델 로드
model = models.efficientnet_b0(weights=None)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, NUM_CLASSES)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model = model.to(device)
model.eval()

print("모델 로드 완료!")

# 평가 함수
def evaluate(model, loader):
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    return np.array(all_preds), np.array(all_labels)


# 메인 실행
if __name__ == "__main__":
    print("\n평가 시작!")
    print("-" * 50)

    preds, labels = evaluate(model, val_loader)

    # 전체 정확도
    acc = (preds == labels).mean() * 100
    print(f"\n전체 정확도: {acc:.2f}%")

    # 클래스별 정확도
    print("\n클래스별 성능:")
    print(classification_report(labels, preds, target_names=class_names))

    # 혼동 행렬
    cm = confusion_matrix(labels, preds)
    print("혼동 행렬:")
    print(cm)