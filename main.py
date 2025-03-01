import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Чтение данных из .csv файла 
data = pd.read_csv('student_performance.csv')

#Замена значений оценок для работы с числовыми данными 
grade_mapping = {"A": 5, "B": 4, "C": 3, "D": 2, "F": 1}
data['Final_Grade'] = data['Final_Grade'].map(grade_mapping)

#Разделение по полу и набор средних значений по посещаемости и финальной оценке 
summary = data.groupby('Gender').agg({
    'Attendance (%)': 'mean',
    'Final_Grade': 'mean'
}).reset_index()

#Вычисление среднего значения,дисперсии и медианы оценки 
grade_mean = data["Final_Grade"].mean
grade_var = data["Final_Grade"].var
grade_median = data["Final_Grade"].median
#Обьединение вычисленных значений в тип данных DataFrame для последующего переноса в таблицу exel 
statistics = pd.DataFrame({
    'Statistic': ['Mean', 'Median', 'Variance'],
    'Value': [grade_mean(), grade_median(), grade_var()]
})

#Перенос данных в exel
with pd.ExcelWriter('student_data_and_statistics.xlsx') as writer:
    data.to_excel(writer, sheet_name='Raw Data', index=False)
    summary.to_excel(writer, sheet_name='Summary', index=False)
    statistics.to_excel(writer, sheet_name='Statistics', index=False)


#Разделение по полу для последующего вывода в графике 
for gender in data['Gender'].unique():
    subset = data[data['Gender'] == gender]
    plt.scatter(subset['Attendance (%)'], subset['Final_Grade'], label=gender, alpha=0.6)


#Отрисовка полученных данных 
plt.title('Зависимость финальной оценки от посещаемости')
plt.xlabel('Attendance (%)')
plt.ylabel('Final Grade (Numeric)')
plt.xticks(np.arange(60, 101, 5))
plt.yticks(np.arange(1, 6, 1), ['F', 'D', 'C', 'B', 'A'])
plt.grid()

plt.legend()
plt.show()