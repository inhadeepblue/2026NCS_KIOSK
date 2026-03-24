import pandas as pd
import seaborn as sns

mpg = sns.load_dataset('mpg')
print(mpg.info())
hp_median = mpg['horsepower'].median()
mpg_filled = mpg.copy()
mpg_filled['horsepower'] = mpg_filled['horsepower'].fillna(hp_median)
print(mpg_filled.info())