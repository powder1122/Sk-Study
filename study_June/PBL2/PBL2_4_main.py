import pandas as pd
from PBL2_4_module import LogDataPreprocess, LogisticPipeline
'''
정확도를 높이기 위해 전처리 과정에서 ip열을 제거
데이터 전처리 클래스와 로지스틱 회귀 모델 클래스를 작성하여 사용
'''
def main():
    #데이터셋 불러오기
    log_data = pd.read_csv('web_server_logs_2.csv')

    #클래스 객체 생성
    preprocessor = LogDataPreprocess(log_data)
    logistic_model = LogisticPipeline()


    #데이터 전처리하기
    log_data = preprocessor.transform()

    #라벨 분리하기
    log_data_X, log_data_y = preprocessor.separate_label()
    


    #로지스틱 회귀 사용
    logistic_model.train_data(log_data_X, log_data_y)


if __name__=="__main__":
    main()
