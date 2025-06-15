# 문제 상황: 고객의 구매 데이터를 기반으로 마케팅 전략 수립을 위한 월별 매출 및 고객별 누적 기여도 분석이 필요
# 시계열 데이터 처리
# 캡슐화를 활용한 데이터 관리
# CustomerSalesAnalysis 클래스 정의
# 데이터 항목: 고객명, 구매일자, 상품명, 수량, 단가
# 분석 및 시각화: 월별 매출 총합 막대 그래프, 고객별 누적 매출 파이 차트
# 데이터프레임 초기화 및 총 매출 파생열 생성
# groupby를 활용한 집계 및 시각화(bar, pie)
import pandas as pd
import matplotlib.pyplot as plt  

#예시 데이터
data = pd.DataFrame({
    '고객명': ['홍길동','고길동','홍길동','김길동','한길동','고길동'],
    '구매일자': ['2024-01-10', '2024-01-15', '2024-02-10', '2024-02-20', '2024-03-10','2024-03-23'],
    '상품명': ['참치','로봇청소기','수건','모니터','삼겹살','냉장고'],
    '수량':[1,1,3,1,5,2],
    '단가(만원)': [25,50,1,30,2,300]
})

class CustomerSalesAnalysis:
    def __init__(self,data):
        # data = ['고객명', '구매일자','상품명','수량','단가']

        self.df = data.copy()   #원본 DataFrame 변경을 막기 위해 복사본 사용
        self.df['구매일자'] = pd.to_datetime(self.df['구매일자']) #구매일자 열의 문자열 (날짜)값을 datetime 형식으로 변환. (YYYY-MM-DD)
        self.df['총매출'] = self.df['수량'] * self.df['단가(만원)'] # 판매 수량 * 단가로 총 매출 파생 열을 생성
        self.df['월'] = self.df['구매일자'].dt.to_period('M') # 구매일자의 datetime 형식에서 연-월만 추출.

    #월 총매출 구하기
    def monthly_sales(self):
        monthly = self.df.groupby('월')['총매출'].sum() #월 열을 기준으로 데이터 그룹화. 같은 연도+월끼리 묶은 후 총 매출 열만 선택하여 합산.
        return monthly  #월별로 집계된 총매출 Series

    #월별 매출 총합 막대 그래프 출력
    def plot_monthly_sales(self):
        monthly = self.monthly_sales()
        #한글 폰트 설정
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(monthly.index.astype(str), monthly.values, color='green', edgecolor='black') # bar는 x축 값으로 문자열이나 숫자만 가능하다. Period --> str로 변환
        plt.title('월별 매출 총합')
        plt.xlabel('월')
        plt.ylabel('총매출')
        plt.show()
        
    #고객별 누적 매출 그룹화 
    def customer_sales(self):
        customer = self.df.groupby('고객명')['총매출'].sum()
        return customer
    
    #고객별 누적 매출 파이 차트 만들기
    def plot_customer_sales(self):
        customer = self.customer_sales()
        #한글 폰트 설정
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
        #pie(customer.values = 누적매출, customer.indexc = 고객명). 값이 먼저, 라벨에 조각의 이름
        plt.pie(customer.values, labels=customer.index, autopct='%.1f%%')
        plt.title('고객별 누적 매출 기여도')
        plt.tight_layout() #레이아웃 설정
        plt.show()


#메인
if __name__ == "__main__":
    c_analysis = CustomerSalesAnalysis(data)
    c_analysis.plot_monthly_sales()
    c_analysis.plot_customer_sales()



    