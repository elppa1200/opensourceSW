import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# 경로 설정(상대 경로)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = r"D:\waste_dataset\processed\train"
VAL_DIR = r"D:\waste_dataset\processed\val"
MODEL_SAVE_PATH = r"D:\waste_dataset\model\efficientnet_b0_v2.pth"

# 하이퍼파라미터 설정
BATCH_SIZE = 32       # 한 번에 처리할 이미지 수
EPOCHS = 10           # 전체 데이터 학습 반복 횟수
LEARNING_RATE = 0.001 # 학습률
NUM_CLASSES = 4       # 분류 클래스 수 (glass, metal, paper, plastic)

# GPU 사용 가능 여부 확인 (없으면 CPU 사용)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"사용 디바이스: {device}")

# 데이터 전처리 설정(강화버전)
train_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3),
    transforms.RandomGrayscale(p=0.1),
    transforms.RandomPerspective(distortion_scale=0.3, p=0.3),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# 데이터셋 및 로더
train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=train_transform)
val_dataset = datasets.ImageFolder(VAL_DIR, transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

print(f"클래스 목록: {train_dataset.classes}")
print(f"학습 데이터: {len(train_dataset)}장")
print(f"검증 데이터: {len(val_dataset)}장")

# EfficientNet-B0 모델 불러오기
model = models.efficientnet_b0(weights="IMAGENET1K_V1")

# 마지막 분류 레이어를 4개 클래스로 교체
model.classifier[1] = nn.Linear(model.classifier[1].in_features, NUM_CLASSES)

model = model.to(device)

# 손실함수 및 옵티마이저
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

print("EfficientNet-B0 모델 로드 완료")
print(f"출력 클래스 수: {NUM_CLASSES}")

# 학습 함수
def train_one_epoch(model, loader, criterion, optimizer):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
        total += labels.size(0)

    acc = 100 * correct / total
    avg_loss = total_loss / len(loader)
    return avg_loss, acc

# 검증 함수
def validate(model, loader, criterion):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()
            total += labels.size(0)

    acc = 100 * correct / total
    avg_loss = total_loss / len(loader)
    return avg_loss, acc

# 메인 학습 루프
if __name__ == "__main__":
    print(f"\n학습 시작! (총 {EPOCHS} 에폭)")
    print("-" * 50)

    best_val_acc = 0

    for epoch in range(EPOCHS):
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer)
        val_loss, val_acc = validate(model, val_loader, criterion)

        print(f"에폭 [{epoch+1}/{EPOCHS}]")
        print(f"  Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"  Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.2f}%")
        print("-" * 50)

        # 최고 성능 모델 저장
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"  모델 저장 완료! (Val Acc: {val_acc:.2f}%)")

    print(f"\n학습 완료! 최고 Val Acc: {best_val_acc:.2f}%")