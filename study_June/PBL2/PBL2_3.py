#  PBL2-3번
import pandas as pd
from PBL2_3_module import run_kmeans, scaled_data, plot_kmeans_result, plot_elbow, plot_scatter, run_silhouette
from sklearn.model_selection import train_test_split




def main():
    #데이터 가져오기
    customer_data = pd.read_csv('Mall_Customers.csv')

    #열의 이름을 바꾸기
    customer_data = customer_data.rename(columns={'Annual Income (k$)': 'Annual Income', 'Spending Score (1-100)': 'Spending Score'})
    
    #사용할 열 선택하기
    df_selected = customer_data[['Annual Income', 'Spending Score']]

    #데이터 표준화
    X_scaled = scaled_data(df_selected)

    #표준화된 데이터를 다시 데이터프레임 형태로 변환
    df_scaled = pd.DataFrame(X_scaled, columns=df_selected.columns)

    #학습/테스트 데이터 분리
    X_train, X_test = train_test_split(X_scaled, test_size=0.2, random_state=42)
    
    #K-Means 학습
    train_model =  run_kmeans(X_train, 5)

    #학습 데이터
    train_lables = train_model.predict(X_train)

    #테스트 데이터
    test_model = run_kmeans(X_test,5)

    test_labels = test_model.predict(X_test)

    #K의 최적값을 찾기 위한 엘보우 그래프 --> K는 5선택
    print('K의 최적값을 찾기 위한 엘보우 그래프')
    elbow_graph = plot_elbow(X_train)

    #K-Means 군집 결과 시각화
    print('K-Means 군집 결과 시각화')
    kmeans_train = plot_kmeans_result(X_train, model=train_model)

    #학습 데이터 및 테스트 데이터 산점도
    print('학습 데이터 산점도')
    plot_scatter(X_train, train_lables)

    print('테스트 데이터 산점도')
    plot_scatter(X_test, test_labels)

    #실루엣 점수 확인
    print('실루엣 점수 그래프')
    sil_score = run_silhouette(X_train, train_model.labels_)  #train_model[3] == labels

    #실루엣 점수 분석
    print('')
    print('전체적으로 막대 개수가 차이가 나 데이터 분포가 불균형할 수 있다.')
    print('군집 0번은 평균 이상의 데이터들이 많이 있어 나쁘지 않게 형성된 집단이다. 데이터가 가장 많다.')
    print('군집 1번은 데이터가 많이 없지만 점수가 좋은 편이다.')
    print('군집 2번은 1번과 비슷하게 데이터가 많지 않지만 가장 균형잡혀있다고 볼 수 있다.')
    print('군집 3번은 값 차이가 많이 나 겹치는 데이터가 많을 수 있다.')
    print('군집 4번은 점수 차이가 크게 나진 않지만 평균 이하의 데이터가 많아 뚜렷하게 나뉘어지지 않았을 수 있다.')

    #정리
    print('')
    print('정리: 엘보우 그래프를 통해 기울기가 급격하게 줄어드는 값인 5를 선택하였다')
    print('시각화를 통해 5개의 군집으로 나뉘는 것을 확인할 수 있었다.')
    print('각 클러스터의 특징')
    print('1.소득이 적은데 소비 점수가 높은 그룹')
    print('2. 소득이 적고 소비 점수가 낮은 그룹')
    print('3. 소득과 소비 점수가 중간인 그룹')
    print('4. 소득이 많고 소비 점수가 높은 그룹')
    print('5. 소득이 많고 소비 점수가 낮은 그룹')


#메인
if __name__=="__main__":
    main()

