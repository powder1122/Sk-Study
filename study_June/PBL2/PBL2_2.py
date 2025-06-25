import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

#데이터셋 로드
df = pd.read_csv('train.csv')

#결측치 확인
print('결측치 확인')
print(df.isnull().sum())

#결측치 총 개수
print('결측치 총 개수: ',df.isnull().sum().sum())

#Id 삭제
df_1 = df.drop('Id', axis=1)

#LotFrontage열 결측치 평균값으로 대체
df_1['LotFrontage'] = df_1['LotFrontage'].fillna(df_1['LotFrontage'].mean())
df_1['LotFrontage'] = df_1['LotFrontage'].replace('(all)', df_1['LotFrontage'].mean())
df_1['LotFrontage'].head(10)

#결측치 제거
df_1 = df_1.dropna(axis=1)
#결측치 총 개수
#print(df_1.isnull().sum().sum())

#범주형 데이터 처리를 위한 열 반환
object_cols = df_1.select_dtypes(include=['object','bool','category']).columns
#print("범주형 데이터 열:", list(object_cols))

#범주형 데이터 인코딩: pd.get_dummies로 처리
df_encoded = pd.get_dummies(df_1, columns=object_cols)

#학습 테스트 분리
x = df_encoded.drop('SalePrice', axis=1) #집값 제외
y = df_encoded['SalePrice']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#모델 생성 및 학습
model = DecisionTreeRegressor(max_depth=3, random_state=42)
model.fit(x_train, y_train)

#예측 및 평가
y_pred = model.predict(x_test)

#점수 계산

print('DecisionTree를 이용한 가격 예측 모델')
print('평가 지표: MAE, MSE, R2')
print(f'MAE: {mean_absolute_error(y_test, y_pred):.2f}')
print(f'MSE: {mean_squared_error(y_test, y_pred):.2f}')
print(f'R2 Score: {r2_score(y_test, y_pred):.2f}')