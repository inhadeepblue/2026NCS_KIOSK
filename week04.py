import seaborn as sns
# 유럽 제조 차량 중 연비가 30.0 mpg 이상인 행을 추출하시오.
# 단, 자동차 모델명, 연비, 제조국가만 표시하고 연비가 높은 순으로 정렬하시오.

mpg = sns.load_dataset('mpg')
print(
    mpg[['origin', 'mpg', 'name']]
    .query('origin == "europe" and mpg >= 30.0')
    .sort_values('mpg', ascending=False)
)

