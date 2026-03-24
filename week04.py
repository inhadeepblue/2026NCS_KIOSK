import seaborn as sns
# 유럽 제조 차량 중 연비가 30.0 mpg 이상인 행을 추출하시오.
# 단, 자동차 모델명, 연비, 제조국가만 표시하고 연비가 높은 순으로 정렬하시오.
# 위 조건과 같이 원본 데이터를 업데이트하고 나머지 칼럼들은 삭제하시오.

mpg = sns.load_dataset('mpg')
mpg = (mpg
       .drop(columns=['cylinders','displacement','horsepower','weight','acceleration','model_year'])
       .query('origin == "europe" and mpg >= 30.0').sort_values('mpg', ascending=False))
print(mpg)
