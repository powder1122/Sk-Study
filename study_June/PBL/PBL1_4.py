# 문제 상황: 1년간의 매출 데이터를 분석하여 월별 매출 추이를 시각화해 비즈니스 인사이트를 도출하고자 함
# pandas, numpy, matplotlib 사용
# SalesAnalysis 클래스 정의
# 2024년 1월~12월까지의 날짜 생성
# 일별 매출(1000~10000)을 난수로 생성하여 저장
# 월별 매출 총합 계산 후 시각화
# __init__()에서 pd.date_range로 날짜 생성, 매출 데이터 생성
# 월별 집계: groupby 활용
# 시각화: plt.plot() + 한글 폰트 설정 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# SalesAnalysis 클래스 정의
class SalesAnalysis:

    #__init__()에서 날짜 및 매출 데이터 생성
    def __init__(self):
        #1월부터 12월 날짜 생성
        self.dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')   #2024년 1월 1일부터 12월 31일까지 일별로 생성

        #일별 매출 100~10000 난수 생성
        self.sales = np.random.randint(1000,10001, size=len(self.dates)) #1000부터 10000까지 365개의 난수 생성

        #DataFrame으로 저장 일, 월, 매출
        self.df = pd.DataFrame({
            'date': self.dates,
            'month': self.dates.month,
            'sales': self.sales
        })

    #월별 집계 : groupby
    def monthly_sales(self):
        #월별 매출 총합 계산하기
        monthly_sum = self.df.groupby('month')['sales'].sum().reset_index() #월을 기준으로 그룹화. 월별로 매출을 더하여 총합 구하기. --> reset_index()로 DataFrame 형태로 만들기.
        return monthly_sum

    #시각화
    def plot_monthly_sales(self):
        #월별 매출 데이터
        monthly = self.monthly_sales()  
        #한글 폰트 설정: 맑은 고딕
        plt.rc('font', family='Malgun Gothic')
        plt.rcParams['axes.unicode_minus'] = False # 마이너스 깨짐 방지. (한글 폰트 설정 시 음수 기호가 깨져서 네모 등으로 보일 수 있음)

        #월별 매출 추이 시각화
        plt.plot(monthly['month'], monthly['sales'], marker='o', linestyle='-', color='b', label='월별 매출')
        plt.title('2024년 월별 매출 추이')
        plt.xlabel('월')
        plt.ylabel('매출(만원)')
        plt.legend() #범례 표시

        #그래프 출력
        plt.grid(True) #격자 추가
        plt.show()

if __name__ == "__main__":
    sales_data = SalesAnalysis()
    print(sales_data.monthly_sales()) #월별 매출 총합
    sales_data.plot_monthly_sales() #월별 매출 시각화





