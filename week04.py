import seaborn as sns
import pandas as pd

mpg = sns.load_dataset('mpg')
# print(mpg.groupby(by='origin'))
group_mpg = pd.DataFrame(mpg.groupby(by='origin'))
print(group_mpg)
print(mpg['origin'].nunique())
print(mpg.describe())
