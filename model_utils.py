# model_utils.py 이 코드는 임시로 작성한 모델 로딩 코드입니다. 연웅님과의 작업에서 충돌/문제 발생 시 삭제하셔도 됩니다.
import torch
import torch.nn as nn
from torchvision import models, transforms
import streamlit as st

CLASS_NAMES = ['glass', 'metal', 'paper', 'plastic']

@st.cache_resource
def load_trained_model(model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(CLASS_NAMES))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model, device


def predict(image, model, device):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence = probabilities[0][predicted].item() * 100
    return CLASS_NAMES[predicted.item()], confidence