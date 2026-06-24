import matplotlib.pyplot as plt
import seaborn as sns

data = [10, 15, 7, 18, 22]
labels = ['Запрос 1', 'Запрос 2', 'Запрос 3', 'Запрос 4', 'Запрос 5']

plt.figure(figsize=(10, 5))
sns.barplot(x=labels, y=data)
plt.title('Статистика запросов к приложению')
plt.xlabel('Запросы') 
plt.ylabel('Количество')
plt.savefig('requests_stats.png')
plt.show()