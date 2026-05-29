# model_utils.py 이 코드는 임시로 작성한 모델 로딩 코드입니다. 연웅님과의 작업에서 충돌/문제 발생 시 삭제하셔도 됩니다.
import torch
import torch.nn as nn
from torchvision import models, transforms
import streamlit as st

# 1. 클래스 이름 정의 (요청하신 대로 소문자 변수명 사용)
classes = ['glass', 'metal', 'paper', 'plastic']

@st.cache_resource
def load_trained_model(model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(classes))
    
    # map_location=device를 통해 CPU/GPU 환경에 맞게 로드
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model, device

def predict(image, model, device):
    # 전처리 과정
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    img_tensor = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(img_tensor)
        # 소프트맥스 함수를 통해 확률값 계산 (0~1 사이의 값)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
        
    # classes 배열의 순서('glass', 'metal', 'paper', 'plastic')대로 확률(%)을 배열로 생성
    probs_array = [prob.item() * 100 for prob in probabilities]
    
    # 가장 확률이 높은 클래스의 인덱스를 찾아 이름 추출
    top_index = torch.argmax(probabilities).item()
    top_class = classes[top_index]
    
    # 최고 확률 클래스 이름과, 순서를 따르는 확률 배열을 반환
    return top_class, probs_array