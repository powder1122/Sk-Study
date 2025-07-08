## YOLOv8n 모델 학습 마지막 시도
from ultralytics import YOLO
if __name__=="__main__":
    
    model = YOLO('yolov8s.yaml')  # 모델 아키텍처 정의 파일 (가중치 아님)


    # 학습 수행
    model.train(
        data='food.yaml',      # 클래스 및 경로 정의한 데이터 설정 파일
        epochs=150,            # 학습 반복 횟수
        imgsz=640,             # 입력 이미지 크기
        batch=16,              # 배치 크기 (GPU 메모리에 따라 조절)
        workers=4,             # DataLoader 병렬 처리 수
        device=0,              # GPU 번호 (0부터 시작), CPU만 있다면 'cpu'
        pretrained=False,      # 완전 랜덤 초기화 상태로 학습 시작
        patience=30,           # 조기 종료를 위한 patience 설정
        augment=True,          # 데이터 증강 사용
        project="src/back2/runs",  # 결과 저장 폴더
        name="food_ingredient_fresh", # 실험별 폴더 이름
        exist_ok=True          # 폴더가 이미 존재해도 덮어쓰기 허용
    )
