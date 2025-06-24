#문제 상황: 당뇨병 진단 데이터를 기반으로 기초적인 데이터 전처리 및 
#탐색적 데이터 분석을 수행하는 과제
#
#결측치 처리: Glucose, BloodPressure, SkinThickness, Insulin,
#BMI 열에서 0을 결측치로 간주하고 평균으로 대체
#
#이상치 처리: SkinThicckness, Insulin열에서 상위 1%를 이상치로 
#간주하고 평균으로 대체
#
#정규화: Age 열을 MinMaxScaler로 0~1 범위로 정규화
#
#EDA: 각 열의 결측치 개수 출력, Outcome 별 Glucose 평균 출력,
#전처리 후 데이터프레임 상위 5개 행 출력

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


#데이터셋 로드
df = pd.read_csv('diabetes.csv')

# 결측치 확인
df.isnull().sum()


#결측치 처리할 열들
diabetes_col =  ['Glucose','BloodPressure','SkinThickness', 'Insulin', 'BMI']

#결측치 대체하기
for col in diabetes_col:
    #값이 0인 개수 출력
    print(f'열: {col}, 결측치 개수:{(df[col]==0).sum()}')
    #결측치를 제외한 값의 평균
    mean = df[df[col] != 0].mean()
    #요소가 0이면 평균으로 대체
    #df.loc[df[col] == 0, col] = mean
    #요소가 0이면 NaN으로 대체
    df[col] = df[col].replace(0, np.nan)
    #결측치 채우기
    df[col] = df[col].fillna(mean)


#이상치 처리
#상위 1%는 이상치
col_skin_ins = ['SkinThickness', 'Insulin']
for col in col_skin_ins:
    #이상치 값 설정
    high_1 = df[col].quantile(0.99)
    #이상치 제외 평균
    mean = df[df[col] <= high_1].mean()
    #이상치 개수 출력
    print(f'열: {col}, 결측치 개수:{(df[col] > high_1).sum()}')
    df.loc[df[col] > high_1, col] = mean


#정규화
scaler = MinMaxScaler() #객체 생성
df['scaled'] = scaler.fit_transform(df[['Age']])    #Age열 정규화


#outcome 별 Glucose 평균 출력
#outcume 0일 때
df_outcome_0 = df[df['Outcome'] == 0]
mean_outcome_0 = df_outcome_0['Glucose'].mean()

df_outcome_1 = df[df['Outcome'] == 1]
mean_outcome_1 = df_outcome_1['Glucose'].mean()

print(f'Outcome이 0일 때 Glucose 평균: {mean_outcome_0:.2f}')
print(f'Outcome이 1일 때 Glucose 평균: {mean_outcome_1:.2f}')

#처리 후 데이터프레임 상위 5개 행 출력
print(df.head(5))