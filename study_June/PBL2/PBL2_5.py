#라이브러리 로드
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report

#데이터 생성
df = pd.read_csv('customer_data_balanced.csv')

#데이터 전처리
#특성과 타깃을 분리
#특성: X
X = df.drop('IsChurn', axis=1) 
#타깃: y
y = df['IsChurn']

#원 핫 인코딩
df = pd.get_dummies(df, columns=['ContractType'])

#데이터 분할
X_train, X_temp, y_train, y_temp = train_test_split(
    df, 
    y, 
    test_size=0.3, 
    random_state=42)

#나머지 데이터(30%)를 검증 데이터와 테스트 데이터로 분할
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, 
    y_temp,
    test_size=0.5,
    random_state=42)

#데이터 전처리
#데이터 정규화
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

# #데이터 크기 확인
# print('train data size: ', X_train.shape, y_train.shape)
# print('validatioin data size: ', X_val.shape, y_val.shape)
# print('test data size: ', X_test.shape, y_test.shape)

#모델 설계
#입력층, 은닉층, 출력층으로 구성된 이진 분류 모델

model = tf.keras.Sequential([
    #입력층
    tf.keras.layers.Input(shape=(X_train.shape[1],)),
    #첫 번째 은닉층
    tf.keras.layers.Dense(64, activation='relu'),
    #과적합 방지를 위한 Dropout
    tf.keras.layers.Dropout(0.5),
    #두 번째 은닉층
    tf.keras.layers.Dense(32, activation='relu'),
    #출력층(Sigmoid)
    tf.keras.layers.Dense(1, activation='sigmoid')
])

#모델 컴파일
#손실함수: Binary Crossentropy
#최적화 알고리즘: Adam
#평가지표: Accuracy,F1-Score, Confusion Matrics, Classification_report
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])


#Early Stopping 설정. 0.000001보다 작게 개선되면 조기 종료
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', 
    patience=5, 
    min_delta=0.000001, 
    restore_best_weights=True)

#모델 훈련
history = model.fit(X_train, 
                    y_train,
                    validation_data=(X_val, y_val),
                    epochs=50,
                    batch_size=32,
                    callbacks=[early_stopping])

#모델 평가
#테스트 데이터로 성능 평가
test_loss, test_accuracy = model.evaluate(X_test, y_test)

#예측
predictions = model.predict(X_test)
predicted_classes = (predictions > 0.5).astype(int) #0.5 기준으로 클래스 결정


#테스트 데이터로 성능 평가(Loss, Accuracy)
print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}')

#분류 보고서 출력
print('Classicication Report: \n', classification_report(y_test, predicted_classes))

#혼동 행렬 출력
print('Confusion Matrix: ')
print(confusion_matrix(y_test, predicted_classes))

''' 
분석 결과:
모든 데이터들을 정확하게 분류. TP, TN 100%.
'''