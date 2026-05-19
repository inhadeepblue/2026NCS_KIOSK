import seaborn as sns
import matplotlib.pyplot as plt

titanic = sns.load_dataset('titanic')
new_titanic = titanic.drop(columns=['alive', 'class', 'embark_town', 'deck'])
# print(new_titanic['age'].value_counts())
# print(new_titanic['age'].sort_values(ascending=False))
# print(new_titanic[new_titanic['age'].isnull()])
# print(new_titanic[new_titanic['survived']==1])
# print(titanic.info())
# print(new_titanic.info())
# print(titanic['survived'].head())
# print(titanic['alive'].head())
# print(titanic['embarked'].tail())
# print(titanic['embark_town'].tail())
# print(titanic['pclass'].tail())
# print(titanic['class'].tail())

sns.histplot(titanic['age'], bins=30, kde=True)
plt.title("Age Distribution (with NaN)")
plt.show()