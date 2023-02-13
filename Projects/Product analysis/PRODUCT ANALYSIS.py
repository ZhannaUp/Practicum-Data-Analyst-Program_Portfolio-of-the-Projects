#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-block alert-info">
# <font size="5">
# <center><b>АНАЛИЗ ТОВАРНОГО АССОРТИМЕНТА</b></center>
# </font>
#     </div> 

# <span class="mark">**Описание проекта:**</span>
# 
# Интернет-магазин товаров для дома «Пока все ещё тут» в срочном порядке ищет аналитиков. Надо помочь магазину стать лучше, а клиентам — обустроить дом своей мечты. «Пока все ещё тут» — мы создаём уют!
# 
# <span class="mark">**Заказчик отчета:**</span> Менеджер по продукту/категорийный менеджер
# 
# 
# <span class="mark">**Цель:**</span> выяснить «ненужный» товарный ряд для выведения их из продуктовой линейки с помощью выявления основого и дополнительного товаров. Оптимизация товарного ассортимента.
# 
# <span class="mark">**Задачи:**</span>
# 
# * Распределить товар на основной и дополнительный
# * Проведение ииследовательского анализа данных
# * Проверка статистических гипотез
# 

# <span class="mark"> **Описание данных**</span>
# 
# Колонки в ecommerce_dataset.csv :
# - `date` — дата заказа;
# - `customer_id` — идентификатор покупателя;
# - `order_id` — идентификатор заказа;
# - `product` — наименование товара;
# - `quantity` — количество товара в заказе;
# - `price` — цена товара.

# <span class="mark">**Оглавление**</span>
# 
# * [1. Изучение входных данных](#num1)
# 
# * [2. Предобработка данных](#num2)
#     * [2.1. Исходные данные таблицы/создание столбцов](#num3)
#     * [2.2. Проверим дубликаты и пропуски](#num4)
#     * [2.3. Проверка типов данных](#num5)
#     * [2.4. Проверим выбросы](#num6)
#     * [2.5. Проверка на уникальность заказов/клиентов](#num7) 
# 
# * [3. Анализ данных (EDA)](#num8)
#     * [3.1. Количество товаров в разрезе заказов](#num9)
#     * [3.2. Количество уникальных покупателей в разрезе месяца, дня недели и времени](#num10)
#     * [3.3. Количество заказов в разрезе месяца, дня недели и времени](#num11)
#     * [3.4. Лидеры продаж топ-15 товаров](#num12)
#     * [3.5. Аутсайдеры продаж топ-15 товаров](#num13)
#     
# * [4. Детализация исследования: анализ товарного ассортимента](#num14)
#     * [4.1. Сгруппируем данные по категориям и найдем топ-10](#num15)
#     * [4.2. Средняя выручка по категориям и месяцам](#num16)
#     * [4.3. Соотношение основых и дополнительных товаров](#num17)
#     * [4.4. Определим сезонность по категориям](#num18)
#             
# * [5. Проверка гипотез](#num20)    
#     * [5.1. Проверка гипотезы №1](#num21)
#     * [5.2. Проверка гипотезы №1](#num22)  
#     
# * [6. Общий вывод и рекомендации](#result) 
# 
# * [7. Презентация для заказчика](#point)
#     
# * [8. Дашборт](#dashbord)

# <span class="mark">**Выполнение проекта**</span>

# <a name="num1"></a>
# # **Изучение входных данных**

# In[1]:


# Загружаем библиотеки
import pandas as pd
import numpy as np
import datetime as dt
from matplotlib.pyplot import figure
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.pylab as pylab
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from plotly import graph_objects as go
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import folium


# In[2]:


# Путь к внешней таблице
url = 'https://drive.google.com/file/d/1Q89QFO8eNumV6PwHeySnJ7g7kFA4PL0H/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(url)

df.head()


# In[3]:


# Выведим основную информацию о датафрейме с помощью метода `info()` 
# Изучим столбцы и их типы
df.info()


# In[4]:


# Узнаем количество строк и столбцов в датафрейме
df.shape


# In[5]:


# Просмотр сводной статистики
df.describe().T


# <a name="num2"></a>
# # **Предобработка данных**

# <a name="num3"></a>
# ## Исходные данные таблицы/создание столбцов

# Перед обработкой данных выведим на экран исходные данные, чтобы понимать дальнейшие изменения.
# 

# In[6]:


# Количество строк
print('Количество строк:', len(df))
# Количество уникальных покупателей
print('Количество уникальных покупателей:', len(df['customer_id'].unique()))
# Количество уникальных заказов
print('Количество уникальных заказов:', len(df['order_id'].unique()))
# Количество проданного товара
print('Количество проданного товара:', (df['quantity'].sum()))
# Общая выручка 
df['revenue']= (df['price']* df['quantity']) #  добавим новый столбец с выручкой
print('Общая выручка:',df['revenue'].sum())
# Средний чек заказа
order_sum = df.groupby('order_id').agg({'revenue': 'sum'}).reset_index()
print('Средний чек заказа:', order_sum['revenue'].mean())


# <a name="num4"></a>
# ## Проверим дубликаты и пропуски

# In[7]:


# Проверим наличие пропусков в каждом столбце(%)
pd.DataFrame(round(df.isna().mean()*100,)).style.background_gradient('BuPu') 


# In[8]:


# Проверим наличие дубликатов
df.duplicated().sum()


# In[9]:


# Удалим неявные дубликаты при совпадении трех столбцов
df_up= df.drop_duplicates(subset=['customer_id', 'order_id', 'product'], keep='last')


# In[10]:


# Узнаем количество строк и столбцов в датафрейме
df_up.shape


# In[11]:


print('Всего удаленно строк:', len(df)-len(df_up))


# <a name="num5"></a>
# ## Проверка типов данных

# In[12]:


# Изучим столбцы и их типы
df_up.info()


# Заменим тип данных в столбце `date` на datetime64

# In[13]:


df_up['date'] = pd.to_datetime(df['date'], format = '%Y%m%d%H')


# Добавим к таблице новые столбцы:
# 
# * `year`- год;  
# * `quartel`- квартал; 
# * `month`- месяц; 
# * `week`- день недели; 
# * `day`- день; 
# * `hour`- час

# In[14]:


df_up['year'] = df_up['date'].astype('datetime64[Y]')
df_up['quartel'] = df_up['date'].dt.quarter
df_up['month'] = df_up['date'].astype('datetime64[M]')
df_up['week'] = df_up['date'].dt.day_name()
df_up['day'] = df_up['date'].astype('datetime64[D]')
df_up['hour'] = df_up['date'].dt.hour


# In[15]:


# Проверим столбцы и их типы
df_up.info()


# In[16]:


# Проверим столбцы
df_up.head()


# <a name="num6"></a>
# ## Проверим выбросы

# **Проверка столбца `quantity`**

# In[17]:


df_up['quantity'].describe(percentiles=[0.1, 0.5, 0.6
, 0.7, 0.8, 0.88, 0.9, 0.95]).T


# In[18]:


#Найдем заказ с количеством 1000
df_up.sort_values(by='quantity', ascending=False)[:5]


# In[19]:


#Удаляем выбросы, так как это были оптовые покупки
df_up = df_up[(df_up['quantity'] < 1000)]


# In[20]:


# Проверим
df_up['quantity'].describe(percentiles=[0.1, 0.5, 0.6
, 0.7, 0.8, 0.88, 0.9, 0.95]).T


# In[21]:


# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(df_up['quantity'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# **Проверка столбца `price`**

# In[22]:


df_up['price'].describe(percentiles=[0.1, 0.5, 0.6
, 0.7, 0.8, 0.88, 0.9, 0.95]).T


# In[23]:


#Найдем заказ с максимальной ценой
df_up.sort_values(by='price', ascending=False)[:5]


# In[24]:


# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(df_up['price'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# <span class="mark">**Наблюдение:**</span> В данных нашли оптовый заказ 71743, который удалили. По ценам никаких выбросов нет.

# <a name="num7"></a>
# ## Проверка на уникальность заказов/клиентов

# Проверим задвоение заказов на несколько покупателей

# In[25]:


dupl_user = df_up.groupby('order_id').agg({'customer_id': 'nunique', 'revenue': 'sum', 'quantity': 'sum'}).reset_index()
dupl_user = dupl_user.query('customer_id > 1')
print('Всего задвоений покупателей:', len(dupl_user))


# In[26]:


data_check_dup= (df_up.groupby(['order_id', 'product']).agg({'customer_id': 'nunique'}).reset_index().query('customer_id > 1')['order_id'])
data_check_dup


# In[27]:


data = df_up.query('order_id not in @dupl_user')
data.shape


# In[28]:


data = df_up.query('order_id not in @data_check_dup')
data.shape


# <span class="mark">**Наблюдение:**</span> После удаления дубликатов в разрезе покупателей и заказов мы имеем **4784** проданных товаров.

# После обработи данных выведим на экран новые данные

# In[29]:


# Количество строк
print('Количесво строк таблицы: {}, данные после обработки уменьшилось на {:.2%}'.format(len(data), 1 - (len(data) / len(df))))
# Количество уникальных покупателей

print('Кол-во уникальных покупателей: {}, данные после обработки уменьшилось на {:.2%}'
.format(len(data['customer_id'].unique()), 1 - (len(data['customer_id'].unique()) / len(df['customer_id'].unique()))))

# Количество уникальных заказов
print('Количество уникальных заказов:{}, данные после обработки уменьшилось на {:.2%}'
.format(len(data['order_id'].unique()), 1 - (len(data['order_id'].unique()) / len(df['order_id'].unique()))))

# Количество проданного товара
print('Количество проданного товара:{}, данные после обработки уменьшилось на {:.2%}'
.format(data['quantity'].sum(), 1 - ((data['quantity'].sum()) / (df['quantity'].sum()))))
      
# Общая выручка 
print('Общая выручка:{}, данные после обработки уменьшилось на {:.2%}'
.format(data['revenue'].sum(), 1 - (data['revenue'].sum() / df['revenue'].sum())))

# Средний чек заказа
order_sum = df.groupby('order_id').agg({'revenue': 'sum'}).reset_index()
order_sum_after = data.groupby('order_id').agg({'revenue': 'sum'}).reset_index()
print('Средний чек заказа:{}, данные после обработки уменьшилось на {:.2%}'
.format(order_sum_after['revenue'].mean(), 1 - (order_sum_after['revenue'].mean()) / (order_sum['revenue'].mean())))


# In[30]:


data.shape


# **`ВЫВОД`**: 
# <div style="border:solid orange 2px; padding: 20px"> 
# 
# В исходном датасете  6737 строк и 6 столбцов. После чистки данных и добавление столбцов получилось 4784 строк и 13 столбцов.
#                      
# После того, как изучили датасеты, выявили следующие первичные отклонения:
#      
# 1) Изменили тип данных в столбце `date` и добавили новые столбцы:
# * `year`- год;  
# * `quartel`- квартал; 
# * `month`- месяц; 
# * `week`- день недели; 
# * `day`- день; 
# * `hour`- час    
#     
# 2) Добавили столбец `revenue` с данными о выручке по каждому товару.\
# 3) Удалили выброс по количеству товара (заказ 71743).
# 4) Удалили 28,97% данных, где произошло задвоение по покупателям и заказам.
#     
# </div>

# In[31]:


# Выгрузим очищенный датафрэйм для табло

data.to_csv('data.csv', index = False)


# <a name="num8"></a>
# # Анализ данных(EDA)

# <a name="num9"></a>
# ## Количество товаров в разрезе заказов

# Эти данные нам помогут распределить товары на группы

# In[32]:


# Группируем данные по количеству заказов
quan_count = data.groupby('quantity').agg({'order_id': 'count'}).reset_index()
# Переименовываем название столбцов
quan_count.columns = ['quantity','count']
# Добавляем столбец "%", чтобы найти долю с общего объема
quan_count['%'] = round((quan_count['count']/quan_count['count'].sum())*100,2)
# Сортируем данные по убыванию
quan_count[:10].sort_values(by='count', ascending=False).style.format({'%':'{:.2f}%'})

#quan_count[:10].style.bar(subset=['count'], color='#ffe135')


# <span class="mark">**Наблюдение:**</span> Основной объем продаж состоит из 1-2 позиций в заказе.
# 

# Разбиваем данные на группы для визуализации:
# * A: 1 товар
# * B: 2 товара
# * C: 3-10 товаров
# * D: 11-30 товаров
# * E: 31-50 товаров
# * F: < 51 товара

# In[33]:


def group_goods(product):
    try:
        if  1 == product:
            return 'A'
        elif 2 == product:
            return 'B'
        elif 3 <= product <= 10:
            return 'C'
        elif 11 <= product <= 30:
            return 'D'
        elif 31 <= product <= 50:
            return 'E'
        elif product >= 51:
            return 'F'
    except:
        pass
quan_count['category_quantity'] = quan_count['quantity'].apply(group_goods)
quan_count[:10];


# In[34]:


# Группируем данные по количеству заказов
categoties_goods = quan_count.groupby('category_quantity').agg({'count': 'sum'}).reset_index()
# Переименовываем название столбцов
categoties_goods.columns = ['category_quantity','count']
# Добавляем столбец "%", чтобы найти долю с общего объема
categoties_goods['%'] = round((categoties_goods['count']/categoties_goods['count'].sum())*100,1)
# Сортируем данные по убыванию
categoties_goods.sort_values(by='count', ascending=False)

categoties_goods.style.bar(subset=['count'], color='#ffe135')


# In[35]:


# Построим круговую диаграмму для определения доли каждого события 
fig = go.Figure(data=[go.Pie(labels=quan_count['category_quantity'], values=quan_count['%'])])
fig.update_layout(title="Распределение количества заказов по группах (%)"
)
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=10, marker=dict(line=dict(color='#000000', width=1)))
fig.show()


# <span class="mark">**Наблюдение:**</span> Более 78% в одном заказе присутствует только 1 товар, что можно оценить, как неэффективность работы отдела продаж или отдельно продавцов. Также присутствуют заказы, где более 50 товаров в заказе, есть предположение, что это были или оптовые покупатели или технический сбой в программе. 

# <a name="num10"></a>
# ## Количество уникальных покупателей в разрезе месяца, дня недели и времени

# ### Количество уникальных покупателей в разрезе месяца

# In[36]:


# Группируем данные по месяцам
revenue_month = data.groupby('month').agg({'order_id': 'count', 'revenue': 'sum'}).reset_index()
# Переименовываем название столбцов
revenue_month.columns = ['month','orders_Q', 'orders_revenue']

revenue_month.style.bar(subset=['orders_revenue'], color='#ffe135')


# In[37]:


# Найдем среднюю выручку 
month_aver = round(revenue_month['orders_revenue'].sum()/12, 2)
print('Средняя выручка в месяц в разрезе года:', month_aver)


# In[38]:


# Построим график
fig = px.bar(revenue_month, y='orders_revenue', x= 'month') 
# оформляем график
fig.update_layout(title='Ежемесячная выручка(руб.)',
                   xaxis_title='Месяц',
                   yaxis_title='Выручка(руб.)',
                   width=800, # указываем размеры графика
                   height=500)
# добавляем ось X 
fig.add_hline(y=month_aver, line_dash="dash", line_color="grey")

fig.show()


# Найдем среднее количество заказов и среднюю выручку по месяцам

# In[39]:


# Сгруппируем данные
month_user = data.groupby('month')['customer_id'].agg(['nunique']).reset_index()
# Объединим таблицы по месяцу
user_aver = month_user.merge(revenue_month, on = ['month'])
# Добавим столбец со сред кол заказов на одного покупателя
user_aver['Среднее кол-во заказов'] = (user_aver['orders_Q'] / user_aver['nunique']).round(2)
# Добавим столбец со сред выручной на одного покупателя
user_aver['Средняя сумма заказа пок-ля'] = (user_aver['orders_revenue'] /user_aver['nunique']).round(2)
user_aver.columns = ['Месяц','Q покупателей','Q заказов', 'Выручка', 'Среднее кол-во заказов пок-ля', 'Средняя выручка заказа пок-ля']
user_aver


# <span class="mark">**Наблюдение:**</span> Объем выручки пришелся на июнь, хотя сентябрь показал "плохой" месяц по выручке. Лидерами по среднему количеству заказов оказались месяца- май и апрель. Лидерами по среднему чеку стали- июнь и ноябрь.

# ### Количество уникальных покупателей в разрезе дня недели

# In[40]:


# Группируем данные по дням недели
revenue_week = data.groupby('week').agg({'order_id': 'count', 'revenue': 'sum'}).reset_index()
# Переименовываем название столбцов
revenue_week.columns = ['week','orders_Q', 'orders_revenue']

revenue_week.style.bar(subset=['orders_revenue'], color='#ffe135')


# Найдем среднее количество заказов и среднюю выручку по дням недели

# In[41]:


# Сгруппируем данные
week_user = data.groupby('week')['customer_id'].agg(['nunique']).reset_index()
# Объединим таблицы по месяцу
user_aver_week = week_user.merge(revenue_week, on = ['week'])
# Добавим столбец со сред кол заказов на одного покупателя
user_aver_week['Среднее кол-во заказов'] = (user_aver_week['orders_Q'] / user_aver_week['nunique']).round(2)
# Добавим столбец со сред выручной на одного покупателя
user_aver_week['Средняя сумма заказа пок-ля'] = (user_aver_week['orders_revenue'] /user_aver_week['nunique']).round(2)
user_aver_week.columns = ['Месяц','Q покупателей','Q заказов', 'Выручка', 'Среднее кол-во заказов пок-ля', 'Средняя выручка заказа пок-ля']
user_aver_week.style.bar(subset=['Среднее кол-во заказов пок-ля', 'Средняя выручка заказа пок-ля'], color='#ffe135')


# <span class="mark">**Наблюдение:**</span> Объем выручки пришелся на вторник, а суббота показала "плохой" день недели по выручке. Лидерами по среднему количеству заказов оказались дни недели- воскресенье и понедельник. Лидерами по среднему чеку стали- вторник и пятница.

# ### Количество уникальных покупателей в разрезе времени

# In[42]:


# Группируем данные по времени
revenue_hours = data.groupby('hour').agg({'order_id': 'count', 'revenue': 'sum'}).reset_index()
# Переименовываем название столбцов
revenue_hours.columns = ['hour','orders_Q', 'orders_revenue']

revenue_hours.style.bar(subset=['orders_revenue'], color='#ffe135')


# In[82]:


# Построим график
fig = px.bar(revenue_hours, y='orders_revenue', x= 'hour') 
# оформляем график
fig.update_layout(title='Часовая выручка(руб.)',
                   xaxis_title='Час',
                   yaxis_title='Выручка(руб.)',
                   width=1000, # указываем размеры графика
                   height=500)
# добавляем ось X 
#fig.add_hline(y=month_aver, line_dash="dash", line_color="grey")

fig.show()


# Найдем среднее количество заказов и среднюю выручку по часам

# In[43]:


# Сгруппируем данные по времени
hour_user = data.groupby('hour')['customer_id'].agg(['nunique']).reset_index()
# Объединим таблицы по месяцу
user_aver_hour = hour_user.merge(revenue_hours, on = ['hour'])
# Добавим столбец со сред кол заказов на одного покупателя
user_aver_hour['Среднее кол-во заказов'] = (user_aver_hour['orders_Q'] / user_aver_hour['nunique']).round(2)
# Добавим столбец со сред выручной на одного покупателя
user_aver_hour['Средняя сумма заказа пок-ля'] = (user_aver_hour['orders_revenue'] /user_aver_hour['nunique']).round(2)
user_aver_hour.columns = ['Час','Q покупателей','Q заказов', 'Выручка', 'Среднее кол-во заказов пок-ля', 'Средняя выручка заказа пок-ля']
user_aver_hour.style.bar(subset=['Среднее кол-во заказов пок-ля', 'Средняя выручка заказа пок-ля'], color='#ffe135')


# <span class="mark">**Наблюдение:**</span> Объем заказов пришелся на промежуток времени с 8 до 17 часов, большая часть покупателей пришлась на промежуток времени с 9 до 15 часов. Наибольшая выручка пришлась на 15 часов.

# <a name="num11"></a>
# ## Количество заказов в разрезе дня недели и времени

# In[44]:


# Сгруппируем данные по дню
day_order = data.groupby(['day']).agg({'order_id':'nunique', 'revenue': 'sum'}).reset_index()
# Переименовываем название столбцов
day_order.columns = ['day', 'Q_orders','sum_orders']
day_order.head()


# Построим гистограмму распределения заказов

# In[45]:


day_orders_sum = data.groupby(['order_id']).agg({'revenue': 'sum'}).reset_index()
day_orders_sum.columns = ['orders', 'count_sum']
day_orders_sum.head()


# In[46]:


# Просмотр сводной статистики
day_orders_sum['count_sum'].reset_index().describe(percentiles=[0.1, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]).T


# In[47]:


# Построим гистограмму по дате

fig = px.histogram(day_orders_sum.query('count_sum <= 8000'), x="count_sum", nbins=50)
fig.update_layout(title_text='Распределение суммы заказов', xaxis_title="Сумма заказа", yaxis_title="Количество заказов")
fig.show()


# <span class="mark">**Наблюдение:**</span> Согласно гистограмме видно, что 90% заказов ниже 2770 руб., 50% заказов ниже 690 руб. 

# <a name="num12"></a>
# ## Лидеры продаж топ-10 товаров

# In[48]:


top10_goods = data.groupby(['product']).agg({'order_id': 'count', 'revenue': 'sum'}).reset_index()
top10_goods.sort_values(by=['revenue'], ascending=False)[:10]


# <span class="mark">**Наблюдение:**</span> Наибольший доход принесли такие позиции, как простынь вафельная, сумка-тележка и вешалки мягкие.

# <a name="num13"></a>
# ## Аутсайдеры продаж топ-10 товаров

# In[49]:


out10_goods = data.groupby(['product']).agg({'order_id': 'count', 'revenue': 'sum'}).reset_index()
out10_goods.sort_values(by=['revenue'], ascending=True)[:10]


# <span class="mark">**Наблюдение:**</span> Неспросовыми товарами оказались волшебный ковер, горох Амброзия, Цинния Коралловая и огурец. Возможно стоит их убрать из ассортимента.

# <a name="num14"></a>
# # Детализация исследования: анализ товарного ассортимента

# <a name="num15"></a>
# ## Сгруппируем данные по категориям и найдем топ-10

# In[50]:


# Заменим названия товаров
data['product'] = data['product'].str.replace('Мусорный контейнер в ванную комнату BOWL-SHINY полистирол 14х16 см белый, Spirella, 1014964',
 'Контейнер мусорный в ванную комнату BOWL-SHINY полистирол 14х16 см белый, Spirella, 1014964')
data['product'] = data['product'].str.replace('Этажерка цветочная пластиковая ЛИВИЯ 5 кашпо М-пластика M3140',
 'Цветочная этажерка пластиковая ЛИВИЯ 5 кашпо М-пластика M3140')
data['product'] = data['product'].str.replace('Ящик почтовый металлический с врезным замком Почта 1205250',
 'Почтовый ящик металлический с врезным замком Почта 1205250')
data['product'] = data['product'].str.replace('Набор ковров для ванной комнаты, "Офелия", 40х50/50х80см., серый/бежевый, NTBM50804050-26-190',
 'Ковры набор для ванной комнаты,"Офелия", 40х50/50х80см., серый/бежевый, NTBM50804050-26-190')


# Выдедим первое слово в новый столбец `first_name`
# 

# In[51]:


data['first_name'] = data['product'].apply(lambda x: x.split(' ')[0])
# Приведем к нижнему регистру
data['first_name'] = data['first_name'].str.lower()
data[['first_name','product']].head(10)


# После обработки данных в эксель, составляем список, который позволит распределить товара по категориям 

# In[52]:


# 1 Все для цветов
flowers = [
 'примула','калибрахоа','фуксия','вербена','пуансеттия','фиалка',
'дыня','комнатное','базилик','бегония','бальзамин',
 'бакопа','космея','мята','папоротник','календула', 'каланхое',
'тыква', 'гербера','цветущее', 'афеляндра',
 'цитрофортунелла', 'пахира', 'фаленопсис', 'искусственная', 'эхеверия', 'клубника', 'многолетнее', 'кофе',
 'седум', 'табак', 'спатифиллум', 'дендориум', 'калла', 'лавр', 'мирт','львиный', 'дендробиум', 'цветочная',
 'искусственный','колокольчик','декоративная','подвесное', 'нивянник', 'вербейник', 'гардения', 'гортензия', 
 'калатея', 'алое', 'кореопсис', 'укроп', 'вигна', 'скиммия',
 'колеус', 'душица', 'фатсия', 'лантана', 'кабачок','антуриум','огурец','хризантема','эвкалипт','декабрист',
 'томат','гвоздика','арбуз','петрушка','цинния', 'патиссон','алиссум','азалия','тимьян', 'лобелия', 'исскуственная', 
 'капуста', 'газания','циперус','виола', 'хлорофитум', 'лаванда', 'розмарин', 'мимоза','мединилла', 'тагетис', 'земляника', 
 'астра','пеларгония','рассада','томата','пеларгония', 'роза','петуния', 'герань', 'цветок','однолетнее','флокс','цикламен',' зверобой', 'настурция',  'салат', 'осина', 'целозия', 'портулак', 'крассула',
 'аргирантерум', 'хоста', 'цинерария', 'монарда', 'баклажан', 'вероника', 'сальвия', 'кориандр','лен']

# 2 Все для ванной
bathroom = ['ковры','сетка', 'ванна', 'подголовник', 'штора',  'полотенце', 'махровое','вешалка-сушилка', 'карниз','настенная','сушилка','фен','штанга','ёрш','ерш','ковш','пробка','комплект','контейнер', 'сиденье','корзина',
 'бак','стакан','контейнер','халат', 'махровый']

# 3 Все для кухни
kitchen = ['мантоварка-пароварка', 'мантоварка','электроштопор', 'овощечистка','мусорный','кисточка','крышка',
'набор','просеиватель','лоток','емкость', 'тарелка', 'сахарница','салатник','кружка','банка','нож','сковорода','кастрюля','ложка','вилка', 'кухонное',
 'термокружка', 'термос', 'нож', 'кувшин', 'чайный', 'миска','овсянница', 'терка','измельчитель', 'чайная', 'разделочная', 'блюдце', 'рыбочистка', 'термостакан', 'бидон', 'половник', 'толкушка',
 'сервировочная', 'лопатка', 'столовый', 'сахарница', 'сотейник',
'бульонница', 'венчик', 'скалка', 'сотейник','тортница', 'tepмокружка', 'хлебница', 'блюдо', 'чайник', 'модульная',
 'отделитель','весы', 'миксер', 'овощеварка', 'соковарка','котел']

# 4 Товары для хранения вещей
storage = ['полки', 'этажерка','полка', 'обувница-3', 'складной', 'вешалка','вешалки', 'вешалка-плечики', 'сумка',
 'вешалка-стойка', 'комод', 'стеллаж', 'подставка', 'плечики']

# 5 Хозтовары и инвентарь
household = ['лестница-стремянка','тележка','стремянка', 'лестница', 'стремянки', 'урна-пепельница', 'муссорный',
 'урна', 'стремянка-табурет', 'почтовый','сумка-тележка','таз', 'вантуз', 'швабра','ведро','щетка-утюжок',
 'жестяная', 'зубная', 'шнур', 'петля', 'ящик', 'коробка', 'бельевые','новогоднее', 'кондиционер',
 'корыто', 'веник', 'мыло', 'дозатор', 'шило', 'термометр',
'тряпкодержатель',
 'совок', 'бензин', 'мешок', 'шпагат', 'вакумный', 'фал', 'корзинка', 'ваза',
 'подарочный', 'ткань','автоматическая', 'пылесос','щетка-сметка'
, 'окномойка','щётка','щетка','паста','салфетка','насадка',
 'cредство','перчатки', 'муляж', 'измерительный','сверло-фреза','крепеж',
 'многофункциональный', 'петля-стрела','крючок','камнеломка','стяжка', 'стяжки',]

# 6 Все для спальни
bedroom = ['покрывало', 'простыня', 'одеяло', 'светильник','простынь', 'подушка', 'наматрасник', 'двуспальное',
 'наматрацник-чехол', 'наматрацник', 'пододеяльник','наматрицник', 'чехол', 'кофр','плед','ковер', 'ковёр', 'коврик','скатерть','утюг', 'подкладка', 'подрукавник', 'рукав', 'гладильная', 'чехол'
,'покрытие','доска']


# Далее мы с помощью функции распределим все товары по категориям

# In[53]:


def categorie (row):
     if row['first_name'] in flowers:
        return 'Все для цветов'
     if row['first_name'] in bathroom:
        return 'Все для ванной'
     if row['first_name'] in kitchen:
        return 'Все для кухни'
     if row['first_name'] in storage:
        return 'Товары для хранения вещей'
     if row['first_name'] in household:
        return 'Хозтовары и инвентарь'
     if row['first_name'] in bedroom:
        return 'Все для спальни'
     else:
        return 'Другое'
# Добавим категории в новый столбец
data['categories_product'] = data.apply(categorie, axis=1)


# In[54]:


data.head()


# In[55]:


# Группируем данные по категориям
cat = data.groupby('categories_product').agg({'product': 'count'}).reset_index()                                        .sort_values(by='product', ascending=False)
# Добавляем столбец "%", чтобы найти долю с общего объема по категориям
cat ['%'] = round((cat['product']/cat['product'].sum())*100,1)

# Переименовываем название столбцов
cat.columns = ['Категория','Кол-во товара', 'Доля(%)']
cat.style.bar(subset=['Доля(%)'], color='#ffe135')


# In[56]:


cat.plot(y= 'Доля(%)', kind="pie", figsize=(7, 7), autopct='%1.1f%%', labels=cat['Категория'],)
plt.legend(bbox_to_anchor=(0.6, 0, 0.6, 0.9)) # Расположение легенды на графике
plt.title('Доля распределения категорий товара') # Название графика
plt.show()


# <span class="mark">**Наблюдение:**</span> Согласно диаграмме, основной категорией с долей продаж в 50,7% стали товары в категории "Все для цветов", далее 17,1%- "Хозтовары и инвентарь" и 10,1%- "Все для ванной". 

# <a name="num16"></a>
# ## Средняя выручка по категориям и месяцам

# In[57]:



# Объединим таблицы по месяцу
user_aver = month_user.merge(revenue_month, on = ['month'])
# Добавим столбец со сред кол заказов на одного покупателя
user_aver['Среднее кол-во заказов'] = (user_aver['orders_Q'] / user_aver['nunique']).round(2)
# Добавим столбец со сред выручной на одного покупателя
user_aver['Средняя сумма заказа пок-ля'] = (user_aver['orders_revenue'] /user_aver['nunique']).round(2)
user_aver.columns = ['Месяц','Q покупателей','Q заказов', 'Выручка', 'Среднее кол-во заказов пок-ля', 'Средняя выручка заказа пок-ля']
user_aver


# In[58]:


# Сгруппируем данные  
month_category = data.pivot_table(index='categories_product', columns= 'month', values=['revenue'],               aggfunc={'revenue': 'sum' }).reset_index()

cm = sns.light_palette("#5f9bd6", as_cmap=True)

month_category.style.background_gradient(cmap=cm)


# <a name="num17"></a>
# ## Соотношение основых и дополнительных товаров

# * Перед началом детализации каждой категории с разделением на основные и доптовары, мы выделим таблицы для каждой категории.
# * Сгруппируем данные по наименованию товара и месяца.
# * Далее посчитаем частоту покупок в год в разрезе месяца

# **1. Проанализируем категорию "Все для цветов"**

# In[59]:


# Создадим таблицу
flowers_tab = data.query('categories_product == "Все для цветов"')

# Сгруппируем данные по наименованию товара и месяцу

tab_1 = flowers_tab.pivot_table(index=['first_name', 'month'], values='price', aggfunc='median')        .sort_values(by='price',ascending=False)        .reset_index()
        #.rename(columns={'first_name':'Источник','acquisition_cost': 'CAC'})\
        #.round(2)
tab_1[:10]


# Посчитаем частоту покупок 

# In[60]:


# Сгруппируем данные по наименованию и посчитаем частоту покупок по каждой позиции

flowers_freq = tab_1.pivot_table(index=['first_name'], values='month', aggfunc='count')                      .reset_index()

# Выделим топ-10 самых продаваемых позиций в теч года
flowers_freq_year = flowers_freq.query('month >8').sort_values(by='month',ascending=False).head(10)
flowers_freq_year


# <span class="mark">**Наблюдение:**</span>
# 
# За основной товар в категории "Все для цветов" можно взять товар, который продавался каждый месяц.
# 
# * Пеларгония и герань - 12 месяцев
# * Роза и рассада - 11 месяцев
# * Цветок исскуственный - 10 месяцев

# **2. Проанализируем категорию "Все для ванной"**

# In[61]:


# Создадим таблицу
bathroom_tab = data.query('categories_product == "Все для ванной"')
# Сгруппируем данные по наименованию товара и месяцу
tab_2 = bathroom_tab.groupby('first_name').agg({'order_id' : 'count', 'price':'median'})        .sort_values(by='order_id',ascending=False)        .reset_index()
        
tab_2


# <span class="mark">**Наблюдение:**</span>
# 
# Распределить категорию "Все для ванной" можно следующим образом:
# 
# Основной:
# * Ванна
# * Шторы и карнизы
# * Сушилки полотенец
# * Корзины для белья
# 
# Дополнительный:
# 
# * Коврики для ванной
# * Держатели для полотенец
# * Полотенца
# * Халат
# * Фен
# * Пробка

# **3. Проанализируем категорию "Все для кухни"**

# In[62]:


# Создадим таблицу
kitchen_tab = data.query('categories_product == "Все для кухни"')

# Сгруппируем данные по наименованию товара и месяцу
tab_3 = kitchen_tab.groupby('first_name').agg({'order_id' : 'count', 'price':'median'})        .sort_values(by='order_id',ascending=False)        .reset_index()
        
tab_3


# <span class="mark">**Наблюдение:**</span>
# 
# Распределить категорию "Все для кухни" можно следующим образом:
# 
# Основной:
# * Товары для готовки 
# * Чайник
# * Соковарка
# * Мантоварка
# 
# Дополнительный:
# 
# * наборы посуды (тарелки, кружки)
# * Терки
# * Столовые приборы
# * Сахарница
# * Овощечистка
# * Скалки

# **4. Проанализируем категорию "Товары для хранения вещей"**

# In[63]:


# Создадим таблицу
storage_tab = data.query('categories_product == "Товары для хранения вещей"')

# Сгруппируем данные по наименованию товара и месяцу
tab_4 = storage_tab.groupby('first_name').agg({'order_id' : 'count', 'price':'median'})        .sort_values(by='order_id',ascending=False)        .reset_index()
        
tab_4


# <span class="mark">**Наблюдение:**</span>
# 
# Распределить категорию "Товары для хранения вещей" можно следующим образом:
# 
# Основной:
# * Стелаж
# * Этажерка
# * Обувница
# * Комод
# * Вешалки-стойки
# 
# Дополнительный:
# 
# * плечики
# * сумки
# * полка

# **5. Проанализируем категорию "Хозтовары и инвентарь"**

# In[64]:


# Создадим таблицу
household_tab = data.query('categories_product == "Хозтовары и инвентарь"')

# Сгруппируем данные по наименованию товара и месяцу
tab_5 = household_tab.groupby('first_name').agg({'order_id' : 'count', 'price':'median'})        .sort_values(by='order_id',ascending=False)        .reset_index()
        
tab_5


# <span class="mark">**Наблюдение:**</span>
# 
# Распределить категорию "Хозтовары и инвентарь" можно следующим образом:
# 
# Основной:
# * Лестницы и стремянки
# * Сумки-тележки
# * Урны
# * Пылесос
# 
# Дополнительный:
# 
# * тазы, ведра
# * мешки
# * корзинка, щетка, 

# **6. Проанализируем категорию "Все для спальни"**

# In[65]:


# Создадим таблицу
bedroom_tab = data.query('categories_product == "Все для спальни"')
# Сгруппируем данные по наименованию товара и месяцу
tab_6 = bedroom_tab.groupby('first_name').agg({'order_id' : 'count', 'price':'median'})        .sort_values(by='order_id',ascending=False)        .reset_index()
        
tab_6


# <span class="mark">**Наблюдение:**</span>
# 
# Распределить категорию "Все для спальни" можно следующим образом:
# 
# Основной:
# * Гладильная
# * Утюг
# * Матрасы/одеяла/подушки
# * ковер
# 
# Дополнительный:
# 
# * постельное белье
# * чехлы, подкладки, подрукавники, рукава для гладильных досок
# * светильник

# <a name="num18"></a>
# ## Определим сезонность по категориям

# К сезонному товару можно определить только категорию "Все для цветов".
# Проанализируем ее.
# 

# In[84]:


# Сделаем временной срез с апреля по август и группировку по наименованию товара с подчетом заказов

flowers_seas = flowers_tab.query('month == ("2019-04-01","2019-08-01")')                          .groupby('first_name').agg({'order_id' :'count'})                          .reset_index().sort_values(by='order_id', ascending = False)[:10]
flowers_seas


# In[67]:


# Сделаем срез по рассаде и пеларгонии, петунии
rassada = flowers_tab.query('first_name == "рассада"').groupby('month').agg({'order_id' : 'count'}).reset_index()
pel = flowers_tab.query('first_name == "пеларгония"').groupby('month').agg({'order_id' : 'count'}).reset_index()
tomat = flowers_tab.query('first_name == "томата"').groupby('month').agg({'order_id' : 'count'}).reset_index()
petun = flowers_tab.query('first_name == "петуния"').groupby('month').agg({'order_id' : 'count'}).reset_index()
# Построим график
ax =rassada.plot(kind='bar', y = 'order_id', figsize = (15, 5), label='рассада', color='#008080',)
pel.plot(kind='bar', y = 'order_id', figsize = (15, 5), ax=ax, alpha=0.5, color='#da70d6', label='пеларгония')
tomat.plot(kind='bar', y = 'order_id', figsize = (15, 5), ax=ax, alpha=0.5, color='#cf0', label='томата')
petun.plot(kind='bar', y = 'order_id', figsize = (15, 5), ax=ax, alpha=0.5, color='#000080', label='петуния')
plt.xlabel('Месяц')
plt.ylabel('Количество заказов')
plt.title('График количества заказов растений')
ax.legend()
plt.show()


# <span class="mark">**Наблюдение:**</span>
# 
# К сезонному товару можно отнести
# * рассаду
# * петунью
# * томата
# 

# <a name="num20"></a>
# # Проверка гипотез

# Для проверки двух гипотез выберем метод `scipy.stats.ttest_ind`( гипотеза о равенстве средних двух совокупностей)
# 
# Три аспекта, которые должны быть соблюдены:
# * генеральная совокупность не должна зависеть друг от друга;
# * выборочная средняя должна быть нормально распределена;
# * дисперсии рассматриваемых генеральных совокупностей должны быть равны

# <a name="num21"></a>
# ## Проверка гипотезы №1 : "Среднии ежемесячные доходы по категориям "Все для цветов" и "Все для ванной"  одинаковый"

# Перед проверкой гипотезы найдем средний доходза месяц

# In[68]:


# Сгруппируем данные по месяцу и категории
data_hypoth = data.groupby(['month','categories_product'])['revenue'].agg(['sum']).reset_index()
data_hypoth


# In[69]:


# Сделаем срез по категории "Все для цветов" и "Все для ванной" и найдем среднию

data_hypoth_flowers = data_hypoth.query('categories_product == "Все для цветов"')['sum']
print('Средний доход в месяц по категории "Все для цветов"', round(data_hypoth_flowers.mean(),1))

data_hypoth_bath = data_hypoth.query('categories_product == "Все для ванной"')['sum']
print('Средний доход в месяц по категории "Все для ванной"', round(data_hypoth_bath.mean(), 1))


# После определения среднего дохода приступим к формулировке гипотез

# <span class="girk">Формулировка гипотез:</span>
# 
# * `Нулевая гипотеза(H_0)`: data_hypoth_flowers = data_hypoth_bath - Средние доходы категорий "Все для цветов" и "Все для ванной" **одинаковые**
# * `Альтернативная гипотеза (H_a)`: data_hypoth_flowers ≠ data_hypoth_bath- Средние доходы категорий "Все для цветов" и "Все для ванной" **разные**
# 
# alpha = 0.05 - выберим данный уровень значимости (вероятный порог "необычности")
# 
# **data_hypoth_flowers** - средний доход за месяц категории "Все для цветов"\
# **data_hypoth_bath** -  средний доход за месяц категории "Все для ванной"

# In[70]:


from scipy import stats as st

results = st.ttest_ind(
   data_hypoth_flowers, 
   data_hypoth_bath, equal_var = False) # results = вызов метода для проверки гипотезы
 
alpha = .05 # alpha уровнь значимости
 
print('p-значение:', results.pvalue) # вывод значения p-value на экран 

if results.pvalue < alpha:
    print("Отвергаем нулевую гипотезу")
else:
    print("Не получилось отвергнуть нулевую гипотезу, средний ежемесячный доход категорий одинаковый")# условный оператор с выводом строки с ответом


# Найдем дисперссию двух генеральных совокупностей

# In[71]:


a = np.var(data_hypoth_flowers)
b = np.var(data_hypoth_bath)
print(np.average(a))
print(np.average(b))


# Построим гистограмму распределения среднего дохода категорий "Все для цветов" и "Все для ванной"

# In[72]:


# Выведим таблицу в разрезе категорий, периода и дохода
month_category


# In[73]:


# Построим гостограмму по среднему ежемесячному доходу двух категорий
figure(figsize=(10, 5), dpi=100)
data.query('categories_product == ["Все для цветов","Все для ванной"] & revenue> 1000')    .groupby('categories_product')['revenue']    .plot(kind='hist', bins=30, alpha=0.5)
plt.legend(["Все для цветов","Все для ванной"])
plt.xlabel('Выручка')
plt.ylabel('Кол-во')
plt.show()


# **Наблюдение:** Вероятность *p-value* высока и равна 91%, что говорит о том, что нулевая гипотеза верна и значима. Кроме этого, данные математического расчета также это подтвердили. На гистограмме видно, многочисленное совпадение оценки пользователей двух категорий.

# <a name="num22"></a>
# ## Проверка гипотезы №2 : "Средний чек на одного покупателя по категориям "Все для цветов" и "Все для ванной"  одинаковый"

# Перед проверкой гипотезы найдем среднюю чек покупателя

# In[74]:


# Сгруппируем данные по покупателю и категории
data_hypoth_user = data.groupby(['customer_id','categories_product'])['revenue'].agg(['sum']).reset_index()
data_hypoth_user


# In[75]:


# Сделаем срез по категории "Все для цветов" и "Все для ванной" и найдем среднию 

data_hypoth_flowers_user = data_hypoth_user.query('categories_product == "Все для цветов"')['sum']
print('Средний чек покупателя в месяц по категории "Все для цветов"', round(data_hypoth_flowers_user.mean(),1))

data_hypoth_bath_user = data_hypoth_user.query('categories_product == "Все для ванной"')['sum']
print('Средний чек покупателя по категории "Все для ванной"', round(data_hypoth_bath_user.mean(), 1))


# После определения среднего чека приступим к формулировке гипотез

# <span class="girk">Формулировка гипотез:</span>
# 
# * `Нулевая гипотеза(H_0)`: ddata_hypoth_flowers_user = data_hypoth_bath_user - Средний чек на покупателя категорий "Все для цветов" и "Все для ванной" **одинаковые**
# * `Альтернативная гипотеза (H_a)`: data_hypoth_flowers_user ≠ data_hypoth_bath_user- Средний чек на покупателя категорий "Все для цветов" и "Все для ванной" **разные**
# 
# alpha = 0.05 - выберим данный уровень значимости (вероятный порог "необычности")
# 
# **data_hypoth_flowers_user** - Средний чек на покупателя категории "Все для цветов"\
# **data_hypoth_bath_user** -  Средний чек на покупателя категории "Все для ванной"

# In[76]:


from scipy import stats as st

results = st.ttest_ind(
   data_hypoth_flowers_user, 
   data_hypoth_bath_user, equal_var = False) # results = вызов метода для проверки гипотезы
 
alpha = .05 # alpha уровнь значимости
 
print('p-значение:', results.pvalue) # вывод значения p-value на экран 

if results.pvalue < alpha:
    print("Отвергаем нулевую гипотезу, средние чеки на одного покупателя разные")
else:
    print("Не получилось отвергнуть нулевую гипотезу, средний чек на одгого покупателя двух категорий одинаковый")# условный оператор с выводом строки с ответом


# Найдем дисперссию двух генеральных совокупностей

# In[77]:


a = np.var(data_hypoth_flowers_user)
b = np.var(data_hypoth_bath_user)
print(np.average(a))
print(np.average(b))


# Построим гистограмму распределения среднего чека на одного покупателя категорий "Все для цветов" и "Все для ванной"

# In[78]:


figure(figsize=(10, 5), dpi=100)
data.query('categories_product == ["Все для цветов","Все для ванной"] & revenue> 2000').groupby('categories_product')['revenue']                                                             .plot(kind='hist', bins=30, alpha=0.5)
plt.legend(["Все для цветов","Все для ванной"])
plt.xlabel('Выручка')
plt.ylabel('Кол-во')
plt.show()


# <span class="mark">**Наблюдение:**</span>  Получив крайне маленькое значение p-value, мы отвергли Нулевую гипотезу. Таким образом, у нас практически нет вероятности получить одинаково средние чеки на одного покупателя. Перепроверка математическим путем и визуализация гистограммы нам это тоже показала.

# <a name="result"></a>
# # Общий вывод и рекомендации

# **`ВЫВОД`**: 
# <div style="border:solid orange 2px; padding: 20px"> 
# 
# В исходном датасете  6737 строк и 6 столбцов. После чистки данных и добавление столбцов получилось 4784 строк и 13 столбцов.
#                      
# <span class="mark"> 1.После того, как изучили датасеты, выявили задвоения данных:</span>
# 
#     БЫЛО
# * Количество строк: 6737
# * Количество уникальных покупателей: 2451
# * Количество уникальных заказов: 2784
# * Количество проданного товара: 16853
# * Общая выручка: 4851280.0
# * Средний чек заказа: 1742.5
# 
#     СТАЛО
#     
# * Количесво строк таблицы: 4784, данные после обработки уменьшилось на 28.99%
# * Кол-во уникальных покупателей: 2393, данные после обработки уменьшилось на 2.37%
# * Количество уникальных заказов:2754, данные после обработки уменьшилось на 1.08%
# * Количество проданного товара:12437, данные после обработки уменьшилось на 26.20%
# * Общая выручка:3411515.0, данные после обработки уменьшилось на 29.68%
# * Средний чек заказа:1238.7, данные после обработки уменьшилось на 28.91%
# 
# <span class="pirk">Рекомендация:</span> Стоит проверить выгрузку данных, перед составлением отчета, чтобы оптимизировать время.
# 
# <span class="mark">2. Категории товаров</span>\
# После распределения товаров на группы, видно что более 78% заказов с одним товаром находятся в категориях "Все для цветов" и "Все для ванной".
#     
# <span class="pirk">Рекомендация:</span> Рекомендуем подробней изучить эти категории на предмет ассортимента. Возможно стоит предлагать дополнительный товар к этим группам для увеличения корзины.
# 
# <span class="mark">3. Динамика продаж</span>
#     
# Четвертый квартал 2018 года был самый прибыльный из всех остальных кварталов 2019 года. В этом квартале были дорогие покупки в категориях "Все для кухни", "Все для ванной", "Все для спальни". Стоит детально изучить проданные товары на предмет мотивации у покупателей и понять, почему спрос упал.   
#     
# <span class="pirk">Рекомендация:</span>
# Стоит увеличить ассортимент основгого товара в категориях "Все для кухни", например закупить современные и дизайнерские столы, стулья, технику. В категории "Все для ванной" дополнить ассортимент раковинами, зеркалами, ваннами, тумбами.
#     
# Если говорить про дополнительный товар, то в категорию "Все для цветов" стоит добавить удобрения, свертства для роста и ухода цветов.
#     
#     
# </div>

# <a name="point"></a>
# # Презентация для заказчика
# 
# 
# 
# Подготовим презентацию исследования для заказчика. 
# 
# Презентация: [ссылка на облачное хранилище с презентацией](https://drive.google.com/file/d/1bCFENA1YUXyUmH4jrT97eraeLxJAu0j1/view?usp=share_link)
# 

# <a name="dashbord"></a>
# # Дашборт

# Просмотр дашборта: [ссылка](https://public.tableau.com/app/profile/zhanna3390/viz/Products_analysis/Dashboard1)
# 

# In[ ]:




