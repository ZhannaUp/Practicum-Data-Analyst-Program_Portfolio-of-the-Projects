#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-block alert-info">
# <font size="5">
# <center><b>ИССЛЕДОВАНИЕ ОБЪЯВЛЕНИЙ О ПРОДАЖЕ КВАРТИР</b></center>
# </font>
#     </div> 

# В нашем распоряжении данные сервиса Яндекс.Недвижимость — архив объявлений о продаже квартир в Санкт-Петербурге и соседних населённых пунктов за несколько лет. Нужно научиться определять рыночную стоимость объектов недвижимости. Ваша задача — установить параметры. Это позволит построить автоматизированную систему: она отследит аномалии и мошенническую деятельность. 
# 
# По каждой квартире на продажу доступны два вида данных. Первые вписаны пользователем, вторые — получены автоматически на основе картографических данных. Например, расстояние до центра, аэропорта, ближайшего парка и водоёма. 

# <span class="mark">**Оглавление:**</span>
# 
# [1. Изучение данных](#num1)
# 
# * Скачать датасет
# * Загрузите данные из файла в датафрейм.
# * Изучите общую информацию о полученном датафрейме.
# * Постройте общую гистограмму для всех столбцов таблицы. 
# 
# [2. Предобработка данных](#num2)
# 
# В данном разделе нам предстоит сделать следующие шаги:
# * оставим в таблице необходимые для анализа столбцы;
# * проверяем и корректируем данные в каждом столбце на предмет:
#       > тип столбца => преобразуем в нужный тип
#       > пустые значения => просавляем "0"/находим median или mean/ удаляем
#       > уникальные значения => корректное написание значений/ явные/неявные дубликаты 
#       > аномалии => восстанавливаем корректное значение/удаляем редкие и выбивающие значения      
# 
# [3. Посчитаю и добавлю в таблицу новые столбцы](#num3)
# 
# * рассчитаю и добавлю новые столбца, а именно:
#     - `'price_per_metr'` цена одного квадратного метра;
#     - `'first_day_exposition_of_week'`день недели публикации объявления (0 — понедельник, 1 — вторник и так далее);
#     - `'first_exposition_month'` месяц публикации объявления;
#     - `first_exposition_year` год публикации объявления;
#     - `type_of_floor` тип этажа квартиры (значения — «первый», «последний», «другой»);
#     - `distance_to_center` расстояние до центра города в километрах (переведите из м в км и округлите до целых значений).
# 
# [4. Исследовательский анализ данных](#num4)
# * изучу, построю гистограммы и опишу все мои наблюдения  для каждого из этих параметров, а именно:
#    * общая площадь;
#    * жилая площадь;
#    * площадь кухни;
#    * цена объекта;
#    * количество комнат;
#    * высота потолков;
#    * этаж квартиры;
#    * тип этажа квартиры («первый», «последний», «другой»);
#    * общее количество этажей в доме;
#    * расстояние до центра города в метрах;
#    * расстояние до ближайшего аэропорта;
#    * расстояние до ближайшего парка;
#    * день и месяц публикации объявления.
#  
# * проанализирую столбец days_exposition(срок продажи):
# * определю факторы влияния на общую(полную) стоимость объекта через корреляцию следующих параметров:   
# * проанализирую столбец locality_name   
# 
# [5. Вывод](#num5)

# # Выполнение проекта

# <a name="num1"></a>
# ## Изучение данных

# In[1]:


# Подключаем библиотеки 
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pylab
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px
import math
import seaborn as sns


# In[2]:


# Загружаем датасет

data = pd.read_csv('https://code.s3.yandex.net/datasets/real_estate_data.csv', sep='\t')


# In[3]:


# Изучаем таблицу
data.head(30)


# In[4]:


# Изучаем столбцы и их типы
data.info()


# In[5]:


# Просмотр сводной статистики
data.describe().T


# In[6]:


# Проверим наличие пропусков в каждом столбце(%)
pd.DataFrame(round(data.isna().mean()*100,)).style.background_gradient('BuPu') 


# In[7]:


# пропущенные значения бары

def pass_value_barh(df):
    try:
        (
            (df.isna().mean()*100)
            .to_frame()
            .rename(columns = {0:'space'})
            .query('space > 0')
            .sort_values(by = 'space', ascending = True)
            .plot(kind= 'barh', figsize=(19,6), rot = -5, legend = False, fontsize = 16)
            .set_title('Пример' + "\n", fontsize = 22, color = 'SteelBlue')    
        );    
    except:
        print('пропусков не осталось :) ')


# In[8]:


pass_value_barh(data)


# In[9]:


# Постоим гистограммы для каждой колонки

params = {'axes.titlesize':'18',
          'xtick.labelsize':'14',
          'ytick.labelsize':'14'}
#matplotlib.rcParams.update(params)


data.hist(figsize=(25, 20), color='orange')
plt.show()


# **`ВЫВОД`**: 
# <div style="border:solid orange 2px; padding: 20px"> 
# 
# В исходном датасете 23699 строк и 22 столбца. 
# После того, как изучили датасет, выявили следующие первичные отклонения:
# 1) `first_day_exposition`- не соответствует тип колонки object\
# 2) `ceiling_height`- <font color='red'>**39%**</font> пустых значений\
# 3) `living_area` - 8% пустых значений\
# 4) `is_apartment` - <font color='red'>**88%**</font> пустых значений, не соответствует тип колонки object\
# 5) `balcony`- <font color='red'>**49%**</font> пустых значений, не соответствует тип колонки float64\
# 6) `kitchen_area`- 10% пустых значений \
# 7) `airports_nearest| cityCenters_nearest | parks_around3000 | ponds_around3000` - по **23%** пустых значений \
# 8) `parks_nearest` - <font color='red'>**66%**</font> пустых значений\
# 9) `ponds_nearest` - <font color='red'>**62%**</font> пустых значений\
# 10)`days_exposition` - **13%** пустых значений\не соответствует тип колонки float64 \
# 11)`floors_total`- не соответствует тип колонки float64\
# 12)`locality_name` - неявные дубликаты
# </div>

# <a name="num2"></a>
# ## Предобработка данных

# В данном разделе нам предстоит сделать следующие шаги:
# * оставим в таблице необходимые для анализа столбцы;
# * проверяем и корректируем данные в каждом столбце на предмет:
#       > тип столбца => преобразуем в нужный тип
#       > пустые значения => просавляем "0"/находим median или mean/ удаляем
#       > уникальные значения => корректное написание значений/ явные/неявные дубликаты 
#       > аномалии => восстанавливаем корректное значение/удаляем редкие и выбивающие значения
#       
# Без проведения очистки данных будет сложно провести дополнительный анализ.
# 
# Чтобы преобразовать типы данных в pandas, используем способы:
# 
# * метод astype(), чтобы принудительно задать тип данных.
# * метод fillna(), заполняем пустые значения 
# * функцию pd.to_datetime(), преобразование отдельных столбцов месяца, дня и года 

# ### Обработка столцов 
# 

# ####  `first_day_exposition` 
# Тип колонки object меняем на datetime\, чтобы мы смогли определить день недели, месяц/год публикайии, срок продажи квартиры(добавим столбец day_exposition), убрали мин/сек, тк они не отражены.

# In[10]:


data['first_day_exposition'] = pd.to_datetime(data['first_day_exposition'])


# In[11]:


# Проверяем пустые значения
data['first_day_exposition'].isna().sum()


# #### `is_apartment` 
# Тип колонки object на bool- булевое значение, Nan изменили на False, тк обратное не указано в таблице.

# In[12]:


data['is_apartment'] = data['is_apartment'].fillna(False).astype('bool')


# #### `balcony` 
# Тип колонки float64 на int64 - целое число и запомняем пустое значение на 0, тк продавец не указал обратное.

# In[13]:


data['balcony'] = data['balcony'].fillna(0).astype('int')
data['balcony'].value_counts()


# ####   `floors_total` 
# Тип колонки float64 на int64 - целое число и пустые значения заполняем медианной.
# 
# Пустых значений- менее 1%(незначительно) или 86 значений.\
# Несколько вариантов:
# * оставить, как есть;
# * удалить пустые значения;
# * поставить медианное значение 
#       
# Вывод: Удаляем и меняем тип колонки float64 на int64.

# **Общее количество этажей в доме по имеющимся данным узнать нельзя. 
# Средним значением заполнять нет смысла, т.к. значение floor может оказаться больше floors_total. 
# Логичнее эти данные удалить.** 
#     

# In[14]:


# Удалим пропуски
total_floor_isna = data['floors_total'].isna() 
data[total_floor_isna]


# In[15]:


# Удалим экстремумы
data = data[(data['floors_total'] < 40)]
# согласно статистике, в Спб нет домов выше 40 этажей


# In[16]:


#  Заменим тип колонки float64 на int64.
data['floors_total'] = data['floors_total'].astype('int')


# In[17]:


# Проверим выбросы
data.floors_total.value_counts().to_frame()


# In[18]:


# Проверим нет ли этаже выше этажности дома
check_floor = data['floors_total'] < data['floor']
data.loc[check_floor]
# Таких этажей нет, значит уловие по пропускам оставим    


# In[19]:


# check
data.info()


# In[20]:


# check
data.shape


# In[21]:


# Прверим статистические показатели
data['floors_total'].describe()


# In[22]:


check_floor = data['floors_total'] < data['floor']
data.loc[check_floor]


# In[23]:


data['floors_total'].isna().sum()


# #### `days_exposition`
# 
# Пустых значений- 13%(значительно).\
# Несколько вариантов:
# * оставить, как есть;
# * удалить пустые значения;
# * поставить медианное значение;
# * поставить медианное значение и удалить экстремумы, чтобы они не влияли на показатели.
#       
# Вывод: меняем тип колонки float64 на int64 и пустые значения меняем на 0(означает, что квартира еще не продана). Кроме этого, оставляем выбросы, тк они могут быть подтверждением долгих продаж.

# In[24]:


# Меняем тип колонки float64 на int64 и исключаем 0
data['days_exposition'] = data['days_exposition'].fillna(0).astype('int')


# In[25]:


# Проверяем уникальные значения
data['days_exposition'].unique()


# In[26]:


# Проверим пустые значения
data['days_exposition'].isna().sum()


# In[27]:


#Удаляем выбросы, те 0, тк они показывают, что квартиры еще не проданы
#data = data[(data['days_exposition'] > 0)]


# In[28]:


# Используем метод describe() для получение статистических значений
data['days_exposition'].describe()


# In[29]:


# Проверим выбросы
data.days_exposition.value_counts().to_frame()


# #### `locality_name`
# 
# Пустых значений- менее 1%(незначительно). Есть неявные дубликаты.\
# Несколько вариантов:
# * оставить, как есть;
# * удалить пустые значения;
# * проверяем уникальные значения в столбце и утраняем неявные дубликаты, а именно:
#   - меняем "ё" на  "е"
#   - меняем'городской поселок' на 'поселок городского типа' 
# Вывод: проверяем уникальные значения в столбце и утраняем неявные дубликаты.

# In[30]:


# Выводим на экран все значения
# Корректируем правильное написание значений

data['locality_name'] = data['locality_name'].str.replace('ё', 'е')
data['locality_name'] = data['locality_name'].str.replace('городской поселок', 'поселок городского типа')

# pd.set_option('display.max_rows', None)
data.groupby(['locality_name'])['locality_name'].count()


# In[31]:


#Удаляем строки, в которых нет значений. Без этих данные крайне сложно анализировать.
data = data.dropna(subset = ['locality_name'])


# In[32]:


#Проверяем наличие пустых значений
data['locality_name'].isna().sum()


# In[33]:


# check
data['locality_name'].nunique()


# In[34]:


# check
data.info()


# ####  `living_area` 
# Пустых значений-  8%(незначительно).
# Можно предположить, что жилая площадь имеет зависимость от количества комнат в квартире. 

# In[35]:


#Проверим это, рассчитав коэффициент корреляции Пирсона.
data['rooms'].corr(data['living_area'])


# Для более точетного попадания медианного значения в пустые значения можно разбить на категории общие площади:
# * A: > 30 м2 (комнаты)
# * B: 31-50 м2 (студии, однокомнатные)
# * C: 51-80 м2 (2-3 комнатные)
# * D: 81-110 м2 (3-4 комнатные)
# * E: 111- 200 м2(5-6 комнатные)
# * F: < 201 м2 (более 6 комнат)

# In[36]:


def total_area_split(area):
    try:
        if 0 <= area <= 30:
            return 'A'
        elif 31 < area <= 50:
            return 'B'
        elif 51 < area <= 80:
            return 'C'
        elif 81 < area <= 110:
            return 'D'
        elif 111 < area <= 200:
            return 'E'
        elif area > 201:
            return 'F'
    except:
        pass
    


# In[37]:


data = data.reset_index(drop=True)
data['total_area_split'] = data['total_area'].apply(total_area_split)


# In[38]:


# Делаем замену пустых значений медианными по каждой категории
data.pivot_table(index='total_area_split', values = 'living_area', aggfunc = 'median').reset_index()


# In[39]:


# Заменим пропуски на среднюю площадь кухни в разрезе категорий
for i in data['total_area_split'].unique(): 
    data.loc[(data['total_area_split'] == i) & (data['living_area'].isna()), 'kitchen_area'] =     data.loc[(data['total_area_split'] == i), 'living_area'].median()


# In[40]:


# Проверим отклонения

data.query('total_area < living_area')


# In[41]:


# check
data.info()


# In[42]:


# В результате замены пропусков у нас получилось несколько строк, где жилая площадь больше общей, что в принципе невозможно. 
# Удалим эти аномалии

data = data.query('total_area > living_area | living_area.isna()')


# In[43]:


# check
data.shape


# In[44]:


#Удаляем выбросы
data = data[(data ['living_area'] <= 220) | (data ['living_area'].isna()) ]

data.info()


# In[45]:


# Проверим выбросы
data.living_area.value_counts().to_frame()


# In[46]:


data['living_area'].isna().sum()


# In[47]:


data['living_area'].describe()


# #### `kitchen_area` 
# Пустых значений-  10%(незначительно).
# 

# In[48]:


# Заменим на 0 если тип квартиры студио
data.loc[data['studio'] == True, 'kitchen_area'] = data.loc[data['studio'] == True, 'kitchen_area'].fillna(0)


# In[49]:


# Проверяем, есть ли у студий кухни. Нет. 
data.groupby('studio')['kitchen_area'].mean()


# In[50]:


# Заменим пропуски на среднюю площадь кухни в разрезе категорий
for i in data['total_area_split'].unique(): 
    data.loc[(data['total_area_split'] == i) & (data['kitchen_area'].isna()), 'kitchen_area'] =     data.loc[(data['total_area_split'] == i), 'kitchen_area'].median()


# In[51]:


#Удаляем выбросы
data = data[(data ['kitchen_area'] < 55) | (data ['kitchen_area'].isna()) ]

data.info()


# In[52]:


# Используем метод describe() для получение статистических значений
data['kitchen_area'].describe()


# In[53]:


# Проверим пустые значения
data['kitchen_area'].isna().sum()


# In[54]:


# НЕПРАВИЛЬНО Проверим 
check_living_area = data['total_area']*0.9  <= (data['living_area'] + data['kitchen_area'])
data.loc[check_living_area]


# In[55]:


data.shape


# #### `airports_nearest`
# Пустых значений- 23%(значительно), если решим изменить на '0, то повлияет на статистичекие показатели.\
# 
# Вывод: Оставляем, как есть, тк многие населенные пункты могут и не иметь аэропорт.

# In[56]:


# Проверим пустые значения
data['airports_nearest'].isna().sum()


# In[57]:


# Используем метод describe() для получение статистических значений
data['airports_nearest'].describe()


# #### `ceiling_height`
#  
# Пустых значений- 39%(значительно), если решим изменить на '0, то повлияет на статистичекие показатели.\
# Несколько вариантов:
# * оставить, как есть;
# * удалить пустые значения;
# * поставить медианное значение 2.65;
# * выполнить условие: 
#       если пустое значение в доме с такой же этажностью, заполняем медианным значением высоты потолка этой этажности, тк данные выглядят реалистично. 
#       
# Вывод: Выполняем условия и заполняем пропуски.

# In[58]:


# Проверим уникальные значения
data['ceiling_height'].unique()


# In[59]:


# За максимыльную высоту потолков возьмем 10, тк выше потолки встречаются крайне редко. 
# Задача все экстемумы выше 10 привести к реальным значениям.
for ceiling in data['ceiling_height']:
    if ceiling >=24:
        ceiling = ceiling/10


# In[60]:


# Фильтрация
data = data.loc[(data['ceiling_height'].isna()) | (data['ceiling_height']>= 2.4)                & (data['ceiling_height']<=7)]


# In[61]:


# Определим объекты, которые находятся в центре Спб и дальше. 
def distance_from_center(distance):
    try:
        if 0 <= distance <= 7000:
            return 'center_spb'
        elif 7 < distance:
            return 'no_center_spb'
    except:
        pass


# In[62]:


# Далее создадим новый столбец 'from_center'
data = data.reset_index(drop=True)
data['from_center'] = data['cityCenters_nearest'].apply(distance_from_center)


# In[63]:


# Заполняем пустые значение средним значением в разрезе удаленности от центра. Используем среднюю, тк выбросов нет.
data.pivot_table(index = 'from_center', values = 'ceiling_height', aggfunc = 'mean').reset_index()

for i in data['from_center'].unique():
    data.loc[(data['from_center'] == i) & (data['ceiling_height'].isna()), 'ceiling_height'] =     data.loc[(data['from_center'] == i), 'ceiling_height'].mean()   


# In[64]:


#Проверим пустые значения
data['ceiling_height'].isna().sum()


# In[65]:


# Проверим выбросы
data.ceiling_height.value_counts().to_frame()


# In[66]:


# check
data.info()


# In[67]:


# check
data.shape


# #### `cityCenters_nearest` 
# Пустых значений- 23%(значительно), если решим изменить на '0, то повлияет на статистичекие показатели.\
# Несколько вариантов:
# * оставить, как есть;
# * удалить пустые значения;
# * поставить "загрушки"- (например: -100), чтобы не искажали данные;
# * выполнить условие: 
#       если пустое значение в столбце cityCenters_nearest совпадает с 'locality_name' , заполняем медианным значением.
# 
# Вывод: После выполнения условия пустых значений осталось 20%, остальное ставляем, как есть и при расчетах их будем исключать.

# Проверим распределение пропусков по городам

# In[68]:


# Отфильтруем нужные ячейки с пустым расстоянием до центра города
cityCenters_nearest_nan = data[data.cityCenters_nearest.isna()]
cityCenters_nearest_nan.head()


# In[69]:


# Сгруппируем датафрейм с пропусками в расстояниях
locality_name_nan = cityCenters_nearest_nan.groupby('locality_name').count()
locality_name_nan


# In[70]:


# Пустых значений не много, ставлю загрушку
data['cityCenters_nearest'] = data['cityCenters_nearest'].fillna(-999)


# In[71]:


#Проверяем наличие пустых значений
data['cityCenters_nearest'].isna().sum()


# In[72]:


# Используем метод describe() для получение статистических значений
data['cityCenters_nearest'].describe()


# In[73]:


#check

x = (
        data
         .value_counts('locality_name')
         .head(25)
         .to_frame()
         .rename(columns = {0:'count'})
    )



y = (
        data[data['airports_nearest'].isna()]
                .value_counts('locality_name')).head(25).to_frame().rename(columns = {0:'count_gap'}
    )

z = x.join(y, how = 'outer').reset_index().sort_values(by = 'locality_name')
z.style.format("{:,.0f}", subset = ['count_gap', 'count'])


# #### `parks_around3000` 
# Пустых значений- 23%(значительно).
# Вывод: Не трогаем

# In[74]:


#Проверяем наличие пустых значений
data['parks_around3000'].isna().sum()


# In[75]:


# Используем метод describe() для получение статистических значений
data['parks_around3000'].describe()


# #### `floor`
# Пустых значений- 0%.
# Тип колонки float64 меняемна int64 - целое число\
# Анамалий нет.\
# Вывод: Замена типа колонки на int64

# In[76]:


#Проверяем наличие пустых значений
data['floor'].isna().sum()


# In[77]:


data['floor'].unique()


# In[78]:


# Замена типа колонки на int64
data['floor'].astype('int')


# In[79]:


# Проверим выбросы
data.floor.value_counts().to_frame()


# #### `total_area`

# In[80]:


#Проверяем наличие пустых значений
data['total_area'].isna().sum()


# In[81]:


#Удаляем выбросы
data = data[(data['total_area'] <= 200)]


# In[82]:


# Проверим выбросы
data.total_area.value_counts().to_frame()


# In[83]:


# Используем метод describe() для получение статистических значений
data['total_area'].describe()


# #### `rooms`
# Пустых значений- 0%.
# Анамалии удаляем.
# 
# Вывод: Оставляем, как есть.

# In[84]:


#Проверяем наличие пустых значений.
data['rooms'].isna().sum()


# In[85]:


#Удаляем выбросы
data = data[(data['rooms'] < 6)]


# In[86]:


# Проверим выбросы
data.rooms.value_counts().to_frame()


# In[87]:


data['rooms'].describe()


# #### `studio`
# Пустых значений- 0%.
# Анамалий нет.
# 
# Вывод: Оставляем, как есть.

# In[88]:


#Проверяем наличие пустых значений.
data['studio'].isna().sum()


# In[89]:


# Используем метод describe() для получение статистических значений
data['studio'].describe()


# In[90]:


# Проверяем уникальные значения
data['studio'].unique()


# In[91]:


# Проверим выбросы
data.studio.value_counts().to_frame()


# #### `open_plan`
# Пустых значений- 0%.
# 
# Анамалий нет.
# 
# Вывод: Оставляем, как есть.

# In[92]:


#Проверяем наличие пустых значений
data['open_plan'].isna().sum()


# In[93]:


# Проверяем уникальные значения
data['open_plan'].unique()


# #### `parks_nearest`
# Пустых значений- 66%(крайне значительно), если решим изменить на '0, то повлияет на статистичекие показатели.\
# Несколько вариантов:
# * оставить, как есть;
# * удалить пустые значения;
# * выполнить условие: 
#       если пустое значение в столбце parks_around3000 совпадает с 'locality_name' , заполняем медианным значением.  Остальное заполняем 0.
# 
# Вывод: Не трогаем. Замена типа колонки на int64.

# In[94]:


# Заполняем пустые значение медианным значением в разрезе места расположения. Медианну используем, тк есть экстремумы.
data['parks_nearest'] = data.groupby(['locality_name'])['parks_nearest'].apply(lambda x: x.fillna(x.median()))


# In[95]:


#Заменим пропуски значением 0, используя метод fillna(), предположив, что парков в радиусе 3 км нет.
data['parks_nearest'] = data['parks_nearest'].fillna(0)


# In[96]:


#Проверяем наличие пустых значений
data['parks_nearest'].isna().sum()


# #### `ponds_around3000`
# Пустых значений- 23%(значительно), если решим изменить на '0, то повлияет на статистичекие показатели.\
# Несколько вариантов:
# * оставить, как есть;
# * удалить пустые значения;
# * выполнить условие: 
#       если пустое значение в столбце ponds_around3000 совпадает с 'locality_name' , заполняем медианным значением, 
#  
# Вывод: Выполняем уловие и остальное заполняем 0, тк скорее всего водоемов в радиусе 3 км нет.

# In[97]:


# Заполняем пустые значение медианным значением в разрезе места расположения. Медианну используем, тк есть экстремумы.
data['ponds_around3000'] = data.groupby(['locality_name'])['ponds_around3000'].apply(lambda x: x.fillna(x.median()))


# In[98]:


#Заменим пропуски значением 0, используя метод fillna()
data['ponds_around3000'] = data['ponds_around3000'].fillna(0)


# In[99]:


#Проверяем наличие пустых значений
data['ponds_around3000'].isna().sum()


# In[100]:


# Используем метод describe() для получение статистических значений
data['ponds_around3000'].describe()


# #### `ponds_nearest`
# Пустых значений- 62%(крайне значитально).
# 
# Несколько вариантов:
# * оставить, как есть;
# * удалить пустые значения;
# * выполнить условие: 
#       если пустое значение в столбце 'ponds_nearest' совпадает с 'locality_name', то заполняем медианным значением.
# 
# Вывод: После выполнения условия пустых значений осталось 21%. Пока оставим их. 

# In[101]:


# Заполняем пропуски в столбце 'ponds_nearest' медианными значениями по каждому типу 'locality_name'.
for i in data['locality_name'].unique():
    data.loc[(data['locality_name'] == i) & (data['ponds_nearest'].isna()), 'ponds_nearest'] =     data.loc[(data['locality_name'] == i), 'ponds_nearest'].median()


# In[102]:


#Проверяем наличие пустых значений
data['ponds_nearest'].isna().sum()


# In[103]:


# Используем метод describe() для получение статистических значений
data['ponds_nearest'].describe()


# #### `last_price`
# Пустых значений- 0%.
# 
# Вывод: Оставляем, как есть.

# In[104]:


# #Проверяем наличие пустых значений
data['last_price'].isna().sum()


# In[105]:


# Меняем формат числа через pandas.options для читабельности
pd.options.display.float_format = '{: .2f}'.format


# In[106]:


#Удаляем выбросы
data = data[(data['last_price'] > 500000) & (data['last_price'] < 30000000)]


# In[107]:


# Используем метод describe() для получение статистических значений
data['last_price'].describe()


# #### `total_images`
# Оставляем без изменений.

# In[108]:


#Проверяем наличие пустых значений
data['total_images'].isna().sum()


# In[109]:


# Используем метод describe() для получение статистических значений
data['total_images'].describe()


# In[110]:


#Проверяем наличие пустых значений по всем столбцам
data.isna().sum()


# In[111]:


# check 
data.info()


# In[112]:


# check

# Показатели о кол-ве объявлений в датасете, минимальных и максимальных показателях 
# в выбранных параметрах о продаже квартир

(
    data[['rooms', 'total_area', 'ceiling_height', 'days_exposition', 'last_price', 'living_area',  'kitchen_area', 'floor',
       'floors_total']]
    .apply (['count', 'min', 'max'])   
    .style.format("{:,.2f}")
)


# In[113]:


# check
data.rooms.value_counts().to_frame()


# In[114]:


# check

# Показатели о кол-ве объявлений в датасете, минимальных и максимальных значениях 
# в выбранных параметрах о продаже квартир
# сырые данные

(
    data[['rooms', 'total_area', 'ceiling_height', 'days_exposition', 'last_price', 'living_area',  'kitchen_area',
          'floor', 'floors_total']]
    .apply (['count', 'min', 'max'])   
    .style.format("{:,.2f}")
)


# In[115]:


# check
data.rooms.value_counts().to_frame()


# In[116]:


# check
data.total_area.hist(bins = 150, figsize = (15,3));


# In[117]:


# check
data.total_area.hist(bins = 150, figsize = (15,3), range = (180,500));


# <a name="num3"></a>
# ### Посчитайте и добавьте в таблицу новые столбцы
# 
# План работ:
# * рассчитаю и добавлю новые столбца, а именно:
#     - `'price_per_metr'` цена одного квадратного метра;
#     - `'first_day_exposition_of_week'`день недели публикации объявления (0 — понедельник, 1 — вторник и так далее);
#     - `'first_exposition_month'` месяц публикации объявления;
#     - `first_exposition_year` год публикации объявления;
#     - `type_of_floor` тип этажа квартиры (значения — «первый», «последний», «другой»);
#     - `distance_to_center` расстояние до центра города в километрах (переведите из м в км и округлите до целых значений).
# * использую следующие методы:
#     - **.dt.dayofweek** (вытаскиваем день недели из даты);
#     - **.dt.month** (вытаскиваем номер месяца из даты);
#     - **.dt.year** (вытаскиваем год из даты);
#     -  пишим функцию для опеределия типа этажа;
#     -  **round()**- округление чисел.

# #### Цена одного квадратного метра

# In[118]:


# Рассчитаем цену м2 и добавим данные в новый столбец price_per_metr
data['price_per_metr'] = data['last_price']/data['total_area']
data.head(3)


# In[119]:


data['price_per_metr'].describe()


# In[120]:


#Удаляем выбросы
data = data[(data['price_per_metr'] < 320000)]


# In[121]:


# Построим гистограмму
plt.figure(figsize=(15,5))
data.price_per_metr.hist(color='rebeccapurple', bins = 1000, alpha=0.6)
plt.xlabel('Средняя цена за м2')
plt.title('Распределение средней цены объектов за м2 в объявлениях')
plt.ylabel('Кол-во объявлений')
plt.show()

# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(data['price_per_metr'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# #### День недели публикации объявления
# 0- понедельник
# 1- вторник
# 2- среда
# 3- четверг
# 4- пятница
# 5- суббота
# 6- воскресенье
# 

# In[122]:


# Добавим новый столбец first_day_exposition_of_week используя метод dayofweek
data['first_day_exposition_of_week'] = pd.to_datetime(data['first_day_exposition']).dt.dayofweek
data.head(3)


# #### Месяц публикации объявления

# In[123]:


# Добавим новый столбец first_exposition_month используя метод month
data['first_exposition_month'] = pd.to_datetime(data['first_day_exposition']).dt.month
data.head(3)


# #### Год публикации объявления

# In[124]:


# Добавим новый столбец first_exposition_year используя метод year
data['first_exposition_year'] = pd.to_datetime(data['first_day_exposition']).dt.year
data.head(3)


# #### Тип этажа 
# (значения- "первый", "последний", "другой")

# In[125]:


# Добавим новый столбец number_floor и оборачиваем в функцию
def type_of_floor(row):
    if row['floor'] == 1:
        return 'первый'
    elif row['floor'] == row['floors_total']:
        return 'последний'
    elif row['floor'] > 1 and row['floor'] < row['floors_total']:
        return 'другой'
    elif row['floor'] > 1 and math.isnan(row['floors_total']):
        return 'другой'


# In[126]:


data['type_of_floor'] = data.apply(type_of_floor, axis=1)


# In[127]:


data[['floor','floors_total', 'type_of_floor']].sample(3)


# #### Расстояние до центра города в километрах
# (переводим из м в км и округляем до целых значений)

# In[128]:


# Добавим новый столбец distance_to_center используя метод round() для округления

###Сначала убери пустые значения в cityCenters_nearest

data['distance_to_center'] = np.round(data['cityCenters_nearest']/1000).astype('int')
data[['cityCenters_nearest','distance_to_center',]].head(3)


# <a name="num4"></a>
# ### Проведите исследовательский анализ данных

# План работ:
# 
# 2.3.1. Изучу, построю гистограммы и опишу все мои наблюдения  для каждого из этих параметров, а именно:
#    * общая площадь;
#    * жилая площадь;
#    * площадь кухни;
#    * цена объекта;
#    * количество комнат;
#    * высота потолков;
#    * этаж квартиры;
#    * тип этажа квартиры («первый», «последний», «другой»);
#    * общее количество этажей в доме;
#    * расстояние до центра города в метрах;
#    * расстояние до ближайшего аэропорта;
#    * расстояние до ближайшего парка;
#    * день и месяц публикации объявления.
#  
# 2.3.2. Проанализирую столбец days_exposition(срок продажи):
#    * постою гистограмму;
#    * рассчитаю среднюю и медианную величину;
#    * разделю срок продажи на "быстрые" и "долгие".
#     
# 2.3.3. Определю факторы влияния на общую(полную) стоимость объекта через корреляцию следующих параметров:
#    * цена-общая площадь
#    * цена-общая площадь
#    * цена-жилая площадь
#    * цена-площадь кухни
#    * цена-количество комнат
#    * цена-этаж
#    * цена-даты размещения (день недели, месяц, год)
#    
# 2.3.4. Проанализирую столбец locality_name:
#    * посчитаю среднюю цену одного квадратного метра в 10 населённых пунктах с наибольшим числом объявлений;
#    * выделю населённые пункты с самой высокой и низкой стоимостью квадратного метра;
#    * определю среднюю цену каждого километра в Санкт-Петербурге и опишу, как стоимость объектов зависит от расстояния до центра города.
#     
# Использую следующие методы:
# - pivot_table(Сводные таблицы)
# - groupby(группировка данных)
# - hist(гистограмма)
# - sort_values(сортировка данных) 

# ####  Изучу, построю гистограммы и опишу все мои наблюдения для каждого из этих параметров

# In[129]:


# Оборачиваем график в функцию для дальнейшего использования
def building_hist(data, x_name,y_name, title):
    plt.figure(figsize=(10,5))
    data.hist(color='rebeccapurple', bins = 100, alpha=0.6 )
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(title)
    plt.ticklabel_format(style='plain')
   
    plt.show()


# **`'total_area'-общая площадь`**

# In[130]:


# Построим гистограмму
building_hist(data.total_area,'Общая площадь(м2)', 'Кол-во объявлений','Распределение общей площади в объявлениях')

# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(data['total_area'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на общую площадь квартир от 50 до 100 м2.  

# **`'living_area'-жилая площадь`**

# In[131]:


# Построим гистограмму
building_hist(data.living_area,'Жилая площадь(м2)', 'Кол-во объявлений','Распределение жилой площади в объявлениях')

# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(data['living_area'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на жилую площадь квартир от 30 до 50 м2. 

# **`'kitchen_area'-площадь кухни`**

# In[132]:


# Построим гистограмму
building_hist(data.kitchen_area,'Площадь кухни(м2)', 'Кол-во объявлений','Распределение площадей кухнь в объявлениях')

# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(data['kitchen_area'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на площадь кухонь от 7 до 12 м2. Есть незначительное количество объявлений, где площадь кухни от 30 до 55 м2.

# **`'last_price'- цена объекта`**

# In[133]:


# Построим гистограмму
plt.figure(figsize=(15,5))
data.last_price.hist(color='rebeccapurple', bins = 1000, alpha=0.5)
plt.xlabel('Цена объекта(0.5=5млн руб)')
plt.title('Распределение цен объектов в объявлениях')
plt.ylabel('Кол-во объявлений')
plt.show()

# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(data['last_price'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на диапозон цен объекта в районе 5 млн рублей. Большое количество выбросов до 500К и более 250 млн р.

# **`'rooms'- количество комнат`**

# In[134]:


# Построим гистограмму
building_hist(data.rooms,'Количество комнат', 'Кол-во объявлений', 'Распределение по количеству комнат в объявлениях')

# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(data['rooms'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на количество комнат до 2х комнат.

# **`'ceiling_height'-высота потолков`**

# In[135]:


# Построим гистограмму
building_hist(data.ceiling_height,'Высота потолков','Кол-во объявлений','Распределение по высоте потолков в объявлениях')


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на высоту потолков в районе 2,7 метров. 

# **`'floor'- этаж квартиры`**

# In[136]:


# Построим гистограмму
building_hist(data.floor,'Этаж квартиры', 'Кол-во объявлений', 'Распределение по этажам в объявлениях')


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на квартиры, расположенные на нижних этажаж( от 1 по 3).

# **`type_of_floor -тип этажа квартиры («первый», «последний», «другой»)`**

# In[137]:


# Построим гистограмму
plt.figure(figsize=(10,3))
data.type_of_floor.hist(color='rebeccapurple', bins = 5, alpha=0.6)
plt.xlabel('Тип этажа квартиры')
plt.ylabel('Кол-во объявлений')
plt.title('Распределение по типам этажей в объявлениях')
plt.show()


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на квартиры, расположенные между первым и последним этажами.

# **`'floors_total'- общее количество этажей в доме`**

# In[138]:


# Построим гистограмму
building_hist(data.floors_total,'Общее количество этажей в доме', 'Кол-во объявлений', 'Распределение по общему количеству этажей в доме в объявлениях')


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на 'этажность дома (5, 9).

# **`'cityCenters_nearest' - расстояние до центра города в метрах`**

# In[139]:


# Построим гистограмму
building_hist(data.cityCenters_nearest,'Расстояние до центра города в метрах', 'Кол-во объявлений', 'Распределение по расстоянию до центра города в метрах')


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на квартиры, расположенные в 10-20 км от центра города. Меньше 0- заглушки

# **`'airports_nearest'- расстояние до ближайшего аэропорта`**

# In[140]:


# Построим гистограмму
building_hist(data.airports_nearest,'Расстояние до ближайшего аэропорта','Кол-во объявлений', 'Распределение по расстоянию до ближайшего аэропорта')


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на квартиры, расположенные в районе 20 км от аэропорта.

# **`parks_nearest- расстояние до ближайшего парка`**

# In[141]:


# Построим гистограмму
plt.figure(figsize=(15,5))
data.last_price.hist(color='rebeccapurple', bins = 500, alpha=0.5)
plt.xlabel('Расстояние до ближайшего парка')
plt.ylabel('Кол-во объявлений')
plt.title('Распределение по расстоянию до ближайшего парка')
plt.show()

# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(data['parks_nearest'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на квартиры, расположенные в районе до 500 м от парка.

# **'first_day_exposition_of_week', 'first_exposition_month'`день и месяц публикации объявления`**

# In[142]:


# Построим гистограмму
building_hist(data.first_day_exposition_of_week,'День недели', 'Кол-во объявлений','Распределение по дням недели в объявлениях')


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на будни. Незначительные пики во вторник и четверг.

# In[143]:


# Построим гистограмму
building_hist(data.first_exposition_month,'Месяц', 'Кол-во объявлений', 'Распределение по месяцам в объявлениях')


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на пиковые месяца- январь и ноябрь.

# #### Проанализирую столбец days_exposition (длительность размещения объяления):
#    * постою гистограмму и диаграмму размаха("ящик с усами");
#    * проанализирую выбросы;
#    * рассчитаю среднюю и медианную величину;
#    * разделю срок продажи на "быстрые" и "долгие"

# In[144]:


# Рассчитаю медианную величину
data['days_exposition'].median()


# In[145]:


# Рассчитаю среднюю величину
data['days_exposition'].mean()


# In[146]:


# Построим гистограмму
plt.figure(figsize=(15,5))
data.days_exposition.hist(color='rebeccapurple', bins = 500, alpha=0.6)

plt.xlabel('Длительность размещения объяления')
plt.ylabel('Кол-во объявлений')
plt.title('Распределение объявлений по длительности размещения')

# Построим диаграмму размаха("ящик с усами")
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(2, 1,2)

ax.boxplot(data['days_exposition'], False, sym='rs', vert=False, whis=0.5, positions=[0], widths=[0.3])

plt.tight_layout()
plt.show()


# **Наблюдение:** На графике видно, что большая часть объявлений приходится на длительность размещения от 55 до 60 дней. Основные выбросы приходяться на длительность от 170 дней. Данные смещены в левую сторону, что говорит о быстрых продажах. 

#  Разделю срок продажи на "быстрые" и "долгие"

# In[147]:


# быстрой продажей будем считать что меньше 25% и долгой, то что больше 75%

data['days_exposition'].describe()  


# In[148]:


# Добавим новый столбец days_exposition_duration и оборачиваем в функцию
def days_exposition_duration(row):
    if row['days_exposition'] < 22:
        return 'быстрые'
    elif row['days_exposition'] > 201:
        return 'долгие'
    return 'стандартные'


# In[149]:


data['days_exposition_duration'] = data.apply(days_exposition_duration, axis=1)


# In[150]:


data[['days_exposition','days_exposition_duration']].sample(3)


# In[151]:


# Изменение средней скорости продаж по годам

data.groupby('first_exposition_year')['days_exposition'].mean()


# **Вывод:** Согласно таблице выше, видно, что с 2014 по 2018 год (2019 исключим из-за неполныл данных) скорость продаж увеличилась в 9 раз, что говорит о высоком спросе на рынке недвижимости. 

# #### Определю факторы влияния на общую(полную) стоимость объекта через корреляцию следующих параметров:
#  
#    * цена-общая площадь
#    * цена-жилая площадь
#    * цена-площадь кухни
#    * цена-количество комнат
#    * цена-этаж
#    * цена-даты размещения (день недели, месяц, год)
#    

# In[152]:


# Построим корреляционную матрицу

data_corr = data[['last_price', 'total_area', 'living_area', 'kitchen_area', 'rooms', 'airports_nearest',                  'balcony', 'ceiling_height', 'cityCenters_nearest', 'floor', 'floors_total', 'is_apartment',                  'locality_name', 'parks_around3000', 'parks_nearest', 'ponds_around3000',                 'ponds_nearest', 'total_images', 'price_per_metr','distance_to_center']].corr()
data_corr.style.background_gradient(cmap='BuPu').set_precision(2)


# In[153]:


fig = px.imshow(data_corr)
fig.show()


# **Изучим влияние средней стомости за м2 на стоимость квартиры**

# In[154]:


aver_price_year = data.groupby('first_exposition_year')['price_per_metr'].mean()
aver_price_year.plot(x = 'first_exposition_year', y = 'price_per_metr', kind = 'line', color='rebeccapurple',          alpha=0.6, figsize=(10,5), xlabel='Год размещения объявления', ylabel='Стоимость м2')

plt.title('Влияние средней стомости за м2 на стоимость квартиры по годам')
plt.show()


# **Наблюдение:** На графике четко прослеживается падение средней стоимости за м2 с 2014 по 2015 года, стагнация с 2016 по 2017 года и резкий подъем с 2019 года.

# **Изучим влияние месяца размещения на стоимость квартиры**

# In[155]:


aver_price_month = data.groupby('first_exposition_month')['price_per_metr'].mean()

aver_price_month.plot(x = 'first_exposition_month', y = 'price_per_metr', kind = 'line', color='rebeccapurple',          alpha=0.6, figsize=(10,5), xlabel='Месяц размещения объявления', ylabel='Стоимость за м2')
plt.title('Влияние средней стомости за м2 на стоимость квартиры по месяцам')
plt.show()


# **Наблюдение:** На графике видно, что основной пик роста средней стоимости за м2 приходит на апрель. 

# In[156]:


# check
data.pivot_table(index='last_price', values=['total_area', 'living_area', 'distance_to_center',                                                           'rooms','kitchen_area']).reset_index()


# **Изучим влияние общей/жилой площади/площади кухни/количества комнат и расстояния от центра на стоимость квартиры**\
# Напримере рассмотрим трехкомнатные квартиры и общее количество объектов

# In[157]:


# цена-общая площадь
data[data['rooms'] == 3].query('total_area < 201 and last_price < 25_000_000').plot(kind='scatter',
        y='last_price' , x='total_area', alpha=0.5, subplots=True, figsize=(15,8), c = 'b', s = 4)
plt.title('Диаграмма рассеяния — Общая площадь — цена трешки')

# цена-жилая площадь
data[data['rooms'] == 3].query('total_area < 201 and last_price < 25_000_000').plot(kind='scatter', 
        y='last_price' , x='living_area', alpha=0.5, figsize=(15,8), c = 'r', s = 4)
plt.title('Диаграмма рассеяния — Жилая площадь — цена трешки');

# цена-площадь кухни
data[data['rooms'] == 3].query('total_area < 201 and last_price < 25_000_000').plot(kind='scatter', 
        y='last_price' , x='kitchen_area', alpha=0.5, figsize=(15,8), c = 'g', s = 4)
plt.title('Диаграмма рассеяния — Площадь кухни — цена трешки');

# цена-этаж
data[data['rooms'] == 3].query('total_area < 201 and last_price < 25_000_000').plot(kind='scatter', 
        y='last_price' , x='floor', alpha=0.5, figsize=(15,8), c = 'c', s = 4)
plt.title('Диаграмма рассеяния — Этаж — цена трешки');


# **Наблюдение:** Проанализировав трехкомнахные квартиры, видна четкая зависимости цены от общей и жилой площади, а также площади кухни. 

# In[158]:


# Кроме этого, мы можем посмотреть зависимости цены и общей площади по всем объявлениям

data.plot(kind='scatter', x='last_price', y='total_area', figsize=(10,5), color='rebeccapurple', alpha= 0.1)
data[['last_price','total_area']].corr()


# **Наблюдение:** На графике видна высокая корреляция (0.78) между стоимостью квартиры и общей площадью, \
# чем больше площадь, тем выше цена. Кроме этого видны объекты с завышенами ценами. 
#     

# In[159]:


# мы можем посмотреть зависимости цены и жилой площади по всем объявлениям

data.plot(kind='scatter', x='last_price', y='living_area', figsize=(10,5), color='rebeccapurple', alpha= 0.1)
data[['last_price','living_area']].corr()


# **Наблюдение:** На графике видна заметная корреляция (0.67) между стоимостью квартиры и жилой площадью. 

# In[160]:


# Кроме этого,мы можем посмотреть зависимости цены и площади кухни по всем объявлениям

data.plot(kind='scatter', x='last_price', y='kitchen_area', figsize=(10,5), color='rebeccapurple', alpha= 0.1)
data[['last_price','kitchen_area']].corr()


# **Наблюдение:** На графике видна заметная корреляция (0.59) между стоимостью квартиры и  площадью кухнию. 

# In[161]:


# Мы можем посмотреть зависимости цены и количества комнат по всем объявлениям

data.plot(kind='scatter', x='last_price', y='rooms', figsize=(10,5), color='rebeccapurple', alpha= 0.1)
data[['last_price','rooms']].corr()


# **Наблюдение:** На графике видна умеренная корреляция (0.48) между стоимостью квартиры и  количеством комнат. 

# In[162]:



# Мы можем посмотреть зависимости цены и типа этажа по всем объявлениям

data.plot(kind='scatter', x='last_price', y='type_of_floor', figsize=(10,5), color='rebeccapurple', alpha= 0.1)


# **Наблюдение:** На графике видно, что квартиры на первом этаже значительно дешевле, чем квартиры расположенные между первым и последним этажами.  

# In[163]:


# Мы можем посмотреть зависимость цены и удаленности от центра по всем объявлениям

data.plot(kind='scatter', x='last_price', y='cityCenters_nearest', figsize=(10,5),          color='rebeccapurple', alpha= 0.1)


# **Наблюдение:** На графике видно, чем ближе к центру, тем дороже.

# #### Проанализирую столбец locality_name:

#    * посчитаю среднюю цену одного квадратного метра в 10 населённых пунктах с наибольшим числом объявлений;
#    * выделю населённые пункты с самой высокой стоимостью квадратного метра;

# In[164]:



cities_top10 = data.pivot_table(index='locality_name', values= 'price_per_metr', aggfunc=['mean', 'count'])

cities_top10.columns = ['price_per_metr_mean', 'total_flats']

price_for_cities_top10 = cities_top10.sort_values(by= 'total_flats', ascending = False).head(10)

price_for_cities_top10.sort_values(by= 'price_per_metr_mean', ascending = False)


# * выделю населённые пункты с самой низкой стоимостью квадратного метра
#  

# In[165]:


price_for_cities_low10 = cities_top10.sort_values(by= 'total_flats', ascending = True).head(10)

price_for_cities_low10.sort_values(by= 'price_per_metr_mean', ascending = True)


# * построю график распределения цены за м2 по населенным пунктам;

# In[166]:


fig, ax = plt.subplots(figsize=(15, 5)) 
# 10 населённых пунктов с наибольшим числом объявлений

data_top_places = data[data.locality_name.isin(data.locality_name.value_counts().index[:10])]
# Пишем функцию
for locality in data_top_places.locality_name.unique():
    sns.kdeplot(data_top_places[data_top_places.locality_name == locality].price_per_metr, label = locality)
    
plt.grid(True) # сетка
plt.legend(loc = 'upper left', bbox_to_anchor = (1,1)) # положение легенды
plt.title('Плотность распределения\цены за квадратный метр по населенным пунктам', loc = 'left') # название графика
plt.xlabel('Цена за квадратный метр') # подпись оси x
plt.xlim((0,250000)) # ограничение значений оси X
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: '{}'.format(int(x/1000)) + 'K')) # форматирование подписей на оси X
plt.annotate('Хвосты', size = 15, xy = (200000, 0.000003), xytext = (220000, 0.0000225), 
             arrowprops = dict(facecolor = 'gray', shrink = 0.1, width = 2)) # аннотация графика с заданной позицией
plt.show()


# **Наблюдение:** Выбрав топ 10 населенных пунктов со средней стоимостью за м2, мы видим, что цена находится в диапазоне 70К-120К в зависимости от места. Максимум в пунктах- Санкт-Петербург, Пушкин, Сестрорецк. Также есть выбросы от 200К.

# **`Определю среднюю цену каждого километра в Санкт-Петербурге и опишу, как стоимость объектов зависит от расстояния до центра города.`**

# In[167]:


# Сортируем по городу, расстоянию и цене
data_spb_mean = data.query('locality_name=="Санкт-Петербург"')                     .groupby('distance_to_center')['last_price'].mean().plot(grid=True, figsize=(12, 5), color='rebeccapurple')
plt.title('Средняя цена км в Санкт-Петербурге') # название графика
plt.xlabel('Расстояние от центра (км)') # подпись оси x
plt.ylabel('Средняя цена за км')
plt.show()


# **Наблюдение:** На графике четко видна корреляция между стоимостью квартиры и расстоянием до центра. Чем ближе к центру, тем дороже.

# ### Общий вывод

# <div style="border-radius: 15px; box-shadow: 4px 4px 4px; border: solid orange 2px; padding: 20px"> 
#     
# - Изучив данные сервиса Яндекс.Недвижимость — архив объявлений о продаже квартир в Санкт-Петербурге и соседних населённых пунктов за несколько лет было выявлено следующее:
# 
# * Основные аномалии были определены по причине некорректно введенных данных самими пользователями, а именно:
#     - высота потолков(проставлялись значения без ".") 
#     - стоимость квартиры (выбросы до 500К и более 250 млн руб)
# Кроме этого, значительная часть данных(более 20%) отсутствовала в значениях- высота поталков, тип квартира-апартаменты, наличие балкона.
# 
# - Если в данных наблюдались пропуски, они заменялись на среднию или медианную величину в разрезе каждого типа данных. Если данные не были найдены через уникальные значения, они обнулялись или удалялись, в зависимости от влияния на статистику. Часть данных, в основном, которая была получена картографическим путем не трогалась, если нельзя было их заменить через функции в разрезе названия населенного пункта. 
# 
# - Высокую корреляционную зависимость можно увидеть между last_price- rooms, rooms-total_area, total_area-living_area, kitchen_area-total_area и last_price-distance_to_center
# 
# - Выбрав топ 10 населенных пунктов со средней стоимостью за м2, мы видим, что цена находится в диапазоне 70К-120К в зависимости от места. Максимум в пунктах- Санкт-Петербург, Пушкин, Сестрорецк.
# 
# - Кроме этого, проанализировав динамику средней цены за м2 по годам, четко прослеживается падение средней стоимости за м2 с 2014 по 2015 года, стагнация с 2016 по 2017 года и резкий подъем с 2019 года.
#     
# </b>
