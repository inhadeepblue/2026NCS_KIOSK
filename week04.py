import pandas as pd
import seaborn as sns

mpg = sns.load_dataset('mpg')
print(mpg.info())
# mpg.dropna(subset=['horsepower'], inplace=True)  # 원본 업데이트
# print(mpg.info())
mpg_clean = mpg.dropna(subset=['horsepower'])  # 사본 생성
print(mpg_clean.info())