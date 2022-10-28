import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Размер надписей на графиках
PLOT_LABEL_FONT_SIZE = 14
# Генерация цветовой схемы
# Возвращает список цветов
def getColors(n):
    COLORS = []
    cm = plt.cm.get_cmap('hsv', n)
    for i in np.arange(n):
        COLORS.append(cm(i))
    return COLORS

def dict_sort(my_dict):
    keys = []
    values = []
    my_dict = sorted(my_dict.items(), key=lambda x:x[1], reverse=True)
    for k, v in my_dict:
        keys.append(k)
        values.append(v)
    return (keys,values)

df = pd.read_csv('./evdataset.csv', escapechar='`', low_memory=False)

# График кол-ва моделей электромобилей у производителей
make_label_count = pd.value_counts(df['Make'].values)
make_count = pd.value_counts(df['Make'].values, sort=True)
make_count_keys, make_count_values = dict_sort(dict(make_count))
TOP_make = len(make_count_keys)
plt.title('Количество моделей электромобилей у производителей', fontsize=PLOT_LABEL_FONT_SIZE)
plt.bar(np.arange(TOP_make), make_count_values, color=getColors(TOP_make))
plt.xticks(np.arange(TOP_make), make_count_keys, rotation=45, fontsize=12)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Количество моделей', fontsize=PLOT_LABEL_FONT_SIZE)

plt.show()

sb.set_style("darkgrid")
sb.barplot(data=df, x="Make", y="Top Speed")
plt.xticks(rotation=45)
plt.ylabel('Максимальная скорость', fontsize=PLOT_LABEL_FONT_SIZE)
plt.xlabel('Марки', fontsize=PLOT_LABEL_FONT_SIZE)

plt.show()

plt.figure(figsize=(15,6))
df['Name'] = df['link'].apply(lambda x: x.split('/')[-1])
data = df.sort_values(by="Acceleration 0 - 100 km/h", ascending=True)[0:50]
sb.set_style("darkgrid")
sb.barplot(data=data, x=data["Name"], y=data["Acceleration 0 - 100 km/h"])
plt.xticks(rotation=90)
plt.ylabel('Разгон от 0 до 100 км/ч', fontsize=PLOT_LABEL_FONT_SIZE)
plt.xlabel('Модели', fontsize=PLOT_LABEL_FONT_SIZE)

plt.show()

cols = ["City - Cold Weather","Highway - Cold Weather","Combined - Cold Weather","City - Mild Weather","Highway - Mild Weather","Combined - Mild Weather"]

for i in range(len(cols)-1):   
    data=df.sort_values(cols[i],ascending=False)[0:30]
    plt.title(cols[i])
    g = sb.barplot(x=data['Name'],y=data[cols[i]],color="#FFA500",data=data)
    g.tick_params(axis='x', labelrotation=90)
    plt.show()