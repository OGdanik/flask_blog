import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure

figure(figsize=(14, 10), dpi=80)

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

df = pd.read_csv('./games-features-edit.csv', escapechar='`', low_memory=False)


# График кол-ва платных и бесплатных игр
frees_label_count = pd.value_counts(df['IsFree'].values)
for label in list(frees_label_count.keys()):
    if label:
        s = 'Free'
    else:
        s = 'NonFree'
    df['IsFree'] = df['IsFree'].replace(to_replace=label, value=s)
games_count = pd.value_counts(df['IsFree'].values, sort=True)
games_count_keys, games_count_values = dict_sort(dict(games_count))
TOP_GAMES = len(games_count_keys)
plt.subplot(2, 2, 1)
plt.title('Соотношение платных игр к бесплатным', fontsize=PLOT_LABEL_FONT_SIZE)
plt.bar(np.arange(TOP_GAMES), games_count_values, color=getColors(TOP_GAMES))
plt.xticks(np.arange(TOP_GAMES), games_count_keys, rotation=0, fontsize=12)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Количество игр', fontsize=PLOT_LABEL_FONT_SIZE)

# График цен и кол-ва игр

df_prices = df
price_label_count = pd.value_counts(df_prices['PriceInitial'].values)
for label in list(price_label_count.keys()):
    df_prices['PriceInitial'] = df_prices['PriceInitial'].replace(to_replace=label, value=int(round(label)))
df_prices = df_prices.drop(df_prices[df_prices.PriceInitial == 0].index)
df_prices = df_prices.drop(df_prices[df_prices.PriceInitial < 5].index)
df_prices = df_prices.drop(df_prices[df_prices.PriceInitial > 50].index)
price_count = pd.value_counts(df_prices['PriceInitial'].values, sort=True)
price_count_keys, price_count_values = dict_sort(dict(price_count))
TOP_PRICES = len(price_count_keys)
plt.subplot(2, 2, 2)
plt.title('Цены на игры и их количество(начальные цены округлены до целого)', fontsize=PLOT_LABEL_FONT_SIZE)
plt.bar(np.arange(TOP_PRICES), price_count_values, color=getColors(TOP_PRICES))
plt.xticks(np.arange(TOP_PRICES), price_count_keys, rotation=60, fontsize=12)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Количество игр', fontsize=PLOT_LABEL_FONT_SIZE)


# График кол-ва игр разных жанров

GAMES_COUNT = [0 for i in range(13)]
GAMES_GENRES = ["NonGame","Indie",
                "Action","Adventure",
                "Casual","Strategy",
                "RPG","Simulation",
                "EarlyAccess","FreeToPlay",
                "Sports","Racing",
                "MassivelyMultiplayer"]
df_genre = df.iloc[0:, 5:18]
n = 0
for i in df_genre:
    cnt = pd.value_counts(df_genre[i].values)
    GAMES_COUNT[n] = cnt.values[1]
    n += 1

plt.subplot(2, 2, 3)
plt.bar(np.arange(13), GAMES_COUNT, color=getColors(13))
plt.xticks(np.arange(13), GAMES_GENRES, rotation=45, fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Количество', fontsize=PLOT_LABEL_FONT_SIZE)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.title('Кол-во игр с указанным жанром', fontsize=PLOT_LABEL_FONT_SIZE)

#График даты выхода игр

date_label_count = pd.value_counts(df['ReleaseDate'].values)
for label in list(date_label_count.keys()):
    if label[-4:].isnumeric():
        df['ReleaseDate'] = df['ReleaseDate'].replace(to_replace=label, value=label[-4:])
    else: 
        df = df.drop(df[df.ReleaseDate == label].index)
date_count = pd.value_counts(df['ReleaseDate'].values, sort=True)
date_count_keys, date_count_values = dict_sort(dict(date_count))
COUNT_GAMES = len(date_count_keys)
plt.subplot(2, 2, 4)
plt.title('Количество выпущенных игр в разные года до 2016', fontsize=PLOT_LABEL_FONT_SIZE)
plt.bar(np.arange(COUNT_GAMES), date_count_values, color=getColors(COUNT_GAMES))
plt.xticks(np.arange(COUNT_GAMES), date_count_keys, rotation=30, fontsize=12)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Количество игр', fontsize=PLOT_LABEL_FONT_SIZE)

plt.show()