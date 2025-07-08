#YOLOv8n 모델 학습
from ultralytics import YOLO
import torch

if __name__=="__main__":
    #모델 정의
    model = YOLO("yolov8n.yaml")  #yolov8n.yaml 파일을 통해 모델 정의


    #모델 학습
    model.train(
        data="data.yaml",       #데이터셋 경로
        epochs=100,             # scratch 학습은 에포크를 늘리는 편이 좋음
        imgsz=640,              #이미지 크기   
        batch=16,               #배치 사이즈
        patience=50,            #early stopping patience
        device="0",             #GPU 사용
        project="runs/scratch", #결과 저장
        name="yolov8_scratch",  #실험별 세부 폴더
        exist_ok=True           #폴더 존재 시 에러 무시
    )


