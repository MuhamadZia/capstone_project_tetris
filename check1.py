from tabnanny import check
import streamlit as st
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import re
import numpy as np
from scipy.interpolate import interp1d
from scipy.misc import derivative
from scipy.spatial.distance import cdist

st.title('Dampak Elektrifikasi')
st.write('Masa pandemi mempunyai banyak kisah yang tidak terduga dan era new normal.'+ 
' Trend saat itu pasti seputar Covid 19.'+
' Namun, ada trend lain yang menarik dan tidak berkaitan dengan pandemi yaitu kendaraan listrik.')

trend_electric_vehicle = pd.read_csv('multiTimeline electric vehicle trending.csv', header=1)
trend_electric_vehicle['Minggu'] = pd.to_datetime(trend_electric_vehicle['Minggu'], format='%Y-%m-%d')
data = trend_electric_vehicle
data.rename(columns={"Minggu":"Waktu"}, inplace=True)

# fig = plt.figure(figsize=(1,1))
# sns.lineplot(data=data, x=data.columns[0], y=data.columns[1])
# plt.xlabel('waktu',fontsize=10)
# plt.ylabel('trend',fontsize=10)
# st.pyplot(fig)
st.line_chart(data, x=data.columns[0], y=data.columns[1])

st.write('Kendaraan listrik dicetuskan karena cost kendaraan yang lebih rendah dan strategi mengurangi pemanasan global. Trend ini diikuti beberapa produk yang dielektrifikasi seperti kompor. Namun, apakah strategi itu mulai berdampak saat ini dan bagaimana kita mempersiapkan selanjutnya ?')

st.header('Asal Sumber Energi Elektrifikasi')
st.write('Sumber energi yang kita gunakan berasal dari berbagai macam. Bagian ini kita akan melihat sumber energi secara umum dan low-carbon')

def sumber_energi(elec_source,list_energy,key):
    # elec_source = pd.read_csv('share-elec-by-source.csv')
    # elec_source['Year'] = pd.to_datetime(elec_source['Year'], format='%Y').dt.to_period('Y').to_timestamp()
    # print(elec_source['Year'])

    elec_source['Year'] = elec_source['Year'].astype(str)
    # list_energy = []
    # for text in elec_source.columns[3:]:
    #     x = re.search("[^\s]+",text)
    #     list_energy.append(x[0])

    col_filter, col_graph = st.columns(2)
    with col_filter:
        option = st.selectbox('Pilih negara :', set(elec_source.Entity), key=key+"1")
        fitur = st.radio('Perbandingan :', ['Tidak', 'World'], key=key+"2")
        if (fitur == 'World'):
            option_energy = st.selectbox('Jenis energi :', list_energy, key=key+"3")
    with col_graph:

        if (fitur =='Tidak'):
            # chart_data = elec_source[(elec_source.Entity == option)][elec_source.columns[2:]]
            # chart_data = chart_data.rename(columns={'Year':'index'}).set_index('index')
            # st.line_chart(chart_data)

            data = elec_source[elec_source.Entity == option]
            data.rename(columns=dict(zip(elec_source.columns[3:], list_energy)),inplace=True)
            # st.write(dict(zip(elec_source.columns[3:], list_energy)))

            fig = px.line(data.sort_values(by='Year'), x='Year', y=data.columns[3:], template='none', markers=True)
            fig.update_layout(
                title = f"Sumber Energi {option}",
                yaxis_title= "% electricity"
            )
            st.plotly_chart(fig)

        elif (fitur == 'World'):

            data = elec_source[(elec_source.Entity == option)|(elec_source.Entity == 'World')]
            data.rename(columns=dict(zip(elec_source.columns[3:], list_energy)),inplace=True)
            # st.write(dict(zip(elec_source.columns[3:], list_energy)))

            fig = px.line(data.sort_values(by='Year'), x='Year', y=option_energy, template='none', markers=True, color='Entity')
            fig.update_layout(
                title = f"Perbandingan Energi {option}",
                yaxis_title= "% electricity"
            )
            st.plotly_chart(fig)

st.subheader('Sumber energi menyeluruh (kelompok)')

per_capita_energyGroup = pd.read_csv('per-capita-electricity-fossil-nuclear-renewables.csv')

list_energy_group = []
for text in per_capita_energyGroup.columns[3:]:
    x = text.split()[0]
    list_energy_group.append(x)

sumber_energi(per_capita_energyGroup,list_energy_group, key='group_energy')

st.subheader('Sumber energi menyeluruh (Spesifik)')
elec_source = pd.read_csv('share-elec-by-source.csv')
# elec_source['Year'] = pd.to_datetime(elec_source['Year'], format='%Y').dt.to_period('Y').to_timestamp()
# print(elec_source['Year'])

elec_source['Year'] = elec_source['Year'].astype(str)
list_energy = []
for text in elec_source.columns[3:]:
    x = re.search("[^\s]+",text)
    list_energy.append(x[0])

sumber_energi(elec_source,list_energy,key="spesific energy")

st.header('Trend Sumber Energi yang Digunakan')
st.write('Setiap negara maupun benua mempunyai sumber energi yang beragam sesuai keadaan. Berikut trend sumber daya beserta intensitas CO2')

# col_even, col_odd = st.columns(2)
def plot_trend(data, column, spacing, y_title, option, delta_color = 'normal'):
    
    x=data[data.Entity == option]['Year']
    y=data[data.Entity == option][column]

    # print(x.info())

    f = interp1d(x=x, y=y)
    x_fake = np.arange(x.min()+spacing, x.max()-spacing,spacing)
    df_dx = derivative(f, x_fake, dx=1e-6)
    
    average = np.around(np.average(df_dx),4)

    # print(f'trend of {column}')
    if average > 0 :
        trend = "Uptrend"
    elif average < 0:
        trend = "Downtrend"
    elif average == 0:
        trend = "No trend!"
        
    st.metric(label=col, value=trend, delta=f"{average} (average)", delta_color=delta_color)

    # Plot
    tab1, tab2 = st.tabs(["📈 Chart Energy-Time", "🗃 Chart Trend"])
    with tab1:
        fig = px.line(x=x, y=y, template='none', markers=True)
        fig.update_layout(
            title = f"{column} of {option}",
            yaxis_title= y_title
        )
        st.plotly_chart(fig)
    with tab2:
        fig = px.line(x=x_fake, y=df_dx, template='none', markers=True)
        fig.update_layout(
            title = f"Trend {column} of {option}",
            yaxis_title= "Trend (df/dt)"
        )
        st.plotly_chart(fig)

        st.write('Average trend measure is:')
        st.write(average)
        st.write("Max trend measure is:")
        st.write(np.around(np.max(df_dx),4))
        st.write("min trend measure is:")
        st.write(np.around(np.min(df_dx),4))


    return x_fake, df_dx, average

list_fossil = ['Coal', 'Gas', 'Oil']
list_renewable = [source for source in list_energy if source not in list_fossil]

list_fossil_fullname = []
list_renewable_fullname = []
for fossil in list_fossil:
    for col in elec_source.columns[3:]:
        if fossil in col:
            list_fossil_fullname.append(col)
            break

for renewable in list_renewable:
    for col in elec_source.columns[3:]:
        if renewable in col:
            list_renewable_fullname.append(col)
            break

elec_source['Fossil (% electricity)'] = elec_source[list_fossil_fullname].sum(axis=1)
elec_source['Renewable (% electricity)'] = elec_source[list_renewable_fullname].sum(axis=1)

new_cols = ['Fossil (% electricity)', 'Renewable (% electricity)']
first_cols = list(elec_source.columns[:3])
first_cols.extend(new_cols)

elec_source['Year'] = elec_source['Year'].astype('str')
elec_source['Year'] = elec_source['Year'].astype('int64')

cols = first_cols[-2:]
data = elec_source
list_source = []
list_average = []

option = st.selectbox('Pilih negara :', set(elec_source.Entity), key="check"+"1")
tab1, tab2, tab3 = st.tabs(['Fossil (% electricity)', 'Renewable (% electricity)', 'Carbon intensity of electricity (gCO2/kWh)'])
list_tabfirst = [tab1,tab2]
for col, tab in zip(cols, list_tabfirst):
    with tab:
        x_fake, df_dx, average = plot_trend(data, column=col, spacing=0.5, y_title='% electricity', option=option)

    list_source.append(col)
    list_average.append(average)

carbon = pd.read_csv('carbon-intensity-electricity.csv')

carbon['Year'] = carbon['Year'].astype('str')
carbon['Year'] = carbon['Year'].astype('int64')

col = carbon.columns[-1]
data = carbon

with tab3:
    x_fake, df_dx, average = plot_trend(data, column=col, spacing=0.5, y_title='% electricity', option=option, delta_color='inverse')
list_source.append(col)
list_average.append(average)

col0, col1, col2 = st.columns(3)

def metrics_trend(list_source, list_average, idx, col_st, delta_color = 'normal'):
    average = list_average[idx]
    if average > 0 :
        trend = "Uptrend"
    elif average < 0:
        trend = "Downtrend"
    elif average == 0:
        trend = "No trend!"

    if col_st == '':
        st.metric(label=list_source[idx], value=trend, delta=f"{list_average[idx]} (average)", delta_color=delta_color)
    else:
        with col_st:
            st.metric(label=list_source[idx], value=trend, delta=f"{list_average[idx]} (average)", delta_color=delta_color)

metrics_trend(list_source, list_average, idx=0, col_st=col0)
metrics_trend(list_source, list_average, idx=1, col_st=col1)
metrics_trend(list_source, list_average, idx=2, col_st=col2, delta_color='inverse')

data = pd.merge(left=elec_source[first_cols], right=carbon, on=['Entity','Code','Year'], how='right')
cols_entity = list(data.Entity.unique())
columns = data.columns[-3:]

dict_trend = {'Entity':cols_entity}
for col in columns:
    cols_trend_value = []
    for option in cols_entity:
        x=data[data.Entity == option]['Year']
        y=data[data.Entity == option][col]

        try:
            f = interp1d(x=x, y=y)
        except Exception:
            cols_trend_value.append(np.nan)
        else:
            spacing = 0.5
            x_fake = np.arange(x.min()+spacing, x.max()-spacing,spacing)
            df_dx = derivative(f, x_fake, dx=1e-6)

            average = np.around(np.average(df_dx),4)

            cols_trend_value.append(average)
    
    dict_trend['Trend '+col] = cols_trend_value

df_ = pd.DataFrame(dict_trend)
df_.to_csv('trend_energy.csv', index=False)

tab1, tab2, tab3 = st.tabs(["5 Trend Tertinggi Fossil Energy", "5 Trend Tertinggi Renewable Energy", "5 Trend Menurun Intensitas CO2"])
with tab1:
    df_five_fossil = df_.sort_values(by=df_.columns[1], ascending=False).head()
    df_five_fossil.reset_index(drop=True,inplace=True)
    st.dataframe(df_five_fossil)
with tab2:
    df_five_renewable = df_.sort_values(by=df_.columns[2], ascending=False).head()
    df_five_renewable.reset_index(drop=True,inplace=True)
    st.dataframe(df_five_renewable)

    col_five_renewable =  list(df_five_renewable.Entity)
with tab3:
    df_five_CO2 = df_.sort_values(by=df_.columns[3], ascending=True).head()
    df_five_CO2.reset_index(drop=True,inplace=True)
    st.dataframe(df_five_CO2)

st.header('Trend Sumber Energi Spesifik (Renewable)')
st.write('Setiap negara maupun benua mempunyai sumber energi yang beragam sesuai keadaan. \
    Berikut trend sumber daya beserta intensitas CO2')

option = st.selectbox('Pilih negara :', set(elec_source.Entity), key="check"+"2")

cols = elec_source.columns[3:-2]
data = elec_source
list_source = []
list_average = []

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(list(cols))
tabs_energy = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8]
for col, tab in zip(cols, tabs_energy):
    
    with tab:
        x_fake, df_dx, average = plot_trend(data, column=col, spacing=0.5, y_title='% electricity', option=option)

    list_source.append(col)
    list_average.append(average)

data_trend = pd.DataFrame({'Source': list_source, 'Average(% elecricity)': list_average})
col_check = data_trend.columns[1]
max = data_trend[col_check].max()
min = data_trend[col_check].min()
source_max = data_trend[data_trend[col_check] == max].Source.iloc[0]
source_min = data_trend[data_trend[col_check] == min].Source.iloc[0]


col1, col2 = st.columns(2)

for check, col in zip([max,min],[col1,col2]):
    if check > 0 :
        trend = "Uptrend"
    elif check < 0:
        trend = "Downtrend"
    elif check == 0:
        trend = "No trend!"
    if col == col1:
        with col1:
            st.caption('Trend Paling Tinggi Sumber Energi')
            st.metric(label=source_max,value=trend,delta=max)
    else:
        with col2:
            st.caption('Trend Paling Rendah Sumber Energi')
            st.metric(label=source_min,value=trend,delta=min)


data = elec_source[elec_source.columns[:-2]]
cols_entity = list(data.Entity.unique())
columns = data.columns[3:] #cols_energy

dict_trend = {'Entity':cols_entity}
for col in columns:
    cols_trend_value = []
    for option in cols_entity:
        x=data[data.Entity == option]['Year']
        y=data[data.Entity == option][col]

        try:
            f = interp1d(x=x, y=y)
        except Exception:
            cols_trend_value.append(np.nan)
        else:
            spacing = 0.5
            x_fake = np.arange(x.min()+spacing, x.max()-spacing,spacing)
            df_dx = derivative(f, x_fake, dx=1e-6)

            average = np.around(np.average(df_dx),4)

            cols_trend_value.append(average)
    
    dict_trend['Trend '+col] = cols_trend_value

df_ = pd.DataFrame(dict_trend)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(list(df_.columns[1:]))
tabs_energy = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8]

for col, tab in zip(df_.columns[1:], tabs_energy):
    with tab:
        df_sorted = df_.sort_values(by=col, ascending=False).head(10)
        fig = px.bar(df_sorted, x=df_sorted.Entity, y=col, template='none')
        fig.update_layout(
            title = f"{col}",
            # yaxis_title= "% electricity"
        )
        st.plotly_chart(fig)

df_five_rn_spesific = df_[df_.Entity.isin(col_five_renewable)].T
df_five_rn_spesific.columns = df_five_rn_spesific.iloc[0]
df_five_rn_spesific.drop(df_five_rn_spesific.index[0], inplace=True)
df_five_rn_spesific.reset_index(inplace=True)
df_five_rn_spesific.rename(columns={'index':'Energy'}, inplace=True)

data = df_five_rn_spesific

tab1, tab2, tab3, tab4, tab5 = st.tabs(list(data.columns[1:]))
col_tabs = [tab1, tab2, tab3, tab4, tab5]

for col, tab in zip(data.columns[1:],col_tabs):
    with tab:
        fig = px.bar(data.sort_values(by=col, ascending=False), x=data.columns[0], y=col, template='none')
        fig.update_layout(
            title = f"Perbandingan Energi {col}",
            yaxis_title= "Trend energy"
        )
        st.plotly_chart(fig)

st.header('Penggunaan Renewable Energy')
st.write('asd')

st.header('Kecocokan dengan Negara')
st.write('Setelah memahami keadaan setiap negara, sekarang dapat mencari negara dengan trend CO2 yang baik dan sesuai dengan keadaannya')

data_prossed_worldbank = pd.read_csv('data_prossed_worldbank.csv')

trend_energy = pd.read_csv('trend_energy.csv')
cols = trend_energy.columns
boundary = trend_energy[trend_energy.Entity == 'World'][cols[-1]].iloc[0]
def class_trend_energy(x, boundary):
    if x <= boundary:
        return 'good_trend'
    else:
        return 'bad_trend'
trend_energy['flag'] = trend_energy[cols[-1]].apply(lambda x: class_trend_energy(x, 0))

dataset_for_suitable = pd.merge(left=trend_energy, right=data_prossed_worldbank, on='Entity', how='left')

cols_country = dataset_for_suitable.Entity.unique()

option = st.selectbox('Pilih negara :', set(cols_country), key="check"+"3")

dict_ = {}
col_entity = []
col_dist = []
for country in cols_country:
        
    entity_1 = dataset_for_suitable[dataset_for_suitable.Entity == option]
    entity_2 = dataset_for_suitable[dataset_for_suitable.Entity == country]

    if country == option:
        continue

    cols_nan_e1 = entity_1.columns[entity_1.isna().any()].tolist()
    cols_nan_e2 = entity_2.columns[entity_2.isna().any()].tolist()
    cols_nan = cols_nan_e1
    cols_nan.extend(cols_nan_e2)
    cols_remove = cols_nan
    cols_remove.extend(['Entity','flag', 'Code'])

    entity_1_cal = entity_1.drop(columns=cols_nan)
    entity_2_cal = entity_2.drop(columns=cols_nan)


    
    dist = cdist(entity_1_cal, entity_2_cal, metric='cosine')
    
    col_entity.append(country)
    col_dist.append(dist[0][0])

dict_['Entity'] = col_entity
dict_['Distance'] = col_dist

data_dist = pd.DataFrame(dict_)
data_dist = pd.merge(left=data_dist, right=dataset_for_suitable[['Entity','flag' ,'Trend Carbon intensity of electricity (gCO2/kWh)']], on='Entity', how='left')
data_best_dist = data_dist[data_dist.flag == 'good_trend'].sort_values(by=['Distance']).reset_index(drop=True).head(5)
st.dataframe(data_best_dist)