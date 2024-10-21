import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df_hour = pd.read_csv("hour.csv")

df_hour.drop(['instant', 'temp', 'atemp', 'hum', 'windspeed'], axis=1, inplace=True)
df_hour.rename(columns={'dteday': 'date', 'hr': 'hour', 'yr': 'year', 'mnth': 'month', 'cnt': 'total'}, inplace=True)
df_hour['date'] = pd.to_datetime(df_hour['date'])

df_hour.season.replace((1, 2, 3, 4), ('Spring', 'Summer', 'Fall', 'Winter'), inplace=True)
df_hour.year.replace((0, 1), ('2011', '2012'), inplace=True)
df_hour.month.replace((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 
                      ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), 
                      inplace=True)
df_hour.holiday.replace((0, 1), ('No', 'Yes'), inplace=True)
df_hour.weekday.replace((0, 1, 2, 3, 4, 5, 6), 
                         ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), 
                         inplace=True)
df_hour.workingday.replace((0, 1), ('No', 'Yes'), inplace=True)
df_hour.weathersit.replace((1, 2, 3, 4), ('Clear', 'Misty', 'Light_rainsnow', 'Heavy_rainsnow'), inplace=True)

st.title("Proyek Analisa Bike Sharing")

st.sidebar.title("Navigasi Analisis")

analysis_option = st.sidebar.selectbox(
    'Pilih Analisis yang Ingin Dilihat',
    (
        'Trend Pengguna Sepeda Casual & Register (2011-2012)',
        'Dampak cuaca pada Jumlah Pengguna Sepeda',
        'Jam Penggunaan Sepeda Paling Banyak'
    )
)


if analysis_option == 'Trend Pengguna Sepeda Casual & Register (2011-2012)':
    st.write("Menampilkan trend pengguna sepeda casual & register dari tahun 2011 sampai 2012")

    df_grouped = df_hour.groupby(by='year').agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    df_melt = df_grouped.melt(id_vars='year', value_vars=['casual', 'registered'],
                              var_name='type', value_name='sum')
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='year', y='sum', hue='type', data=df_melt, palette='muted', ax=ax)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Jumlah Pengguna')
    ax.set_title('Jumlah Pengguna Casual dan Registered per Tahun')

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(format(height, ','),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 5), textcoords='offset points')
    plt.subplots_adjust(top=0.85, bottom=0.2, left=0.15, right=0.95, hspace=0.3, wspace=0.3)
    st.pyplot(fig)

elif analysis_option == 'Dampak cuaca pada Jumlah Pengguna Sepeda':
    st.write("Menampilkan dampak cuaca pada jumlah pengguna sepeda")
    df_grouped = df_hour.groupby(by='weathersit').agg({'total': 'sum'}).reset_index()
    weathersit = df_grouped['weathersit']
    total = df_grouped['total']
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(weathersit, total, color='orange')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.set_xlabel('Weather Situation')
    ax.set_ylabel('Total Users')
    ax.set_title('Total Users by Weather Situation')
    for i, value in enumerate(total):
        ax.text(i, value + 50000, format(value, ','), ha='center', va='bottom')
    plt.subplots_adjust(top=0.85, bottom=0.2, left=0.15, right=0.95, hspace=0.3, wspace=0.3)
    st.pyplot(fig)


elif analysis_option == 'Jam Penggunaan Sepeda Paling Banyak':
    st.write("Menampilkan jam penggunaan sepeda yang paling banyak digunakan")

    df_grouped = df_hour.groupby(by='hour').agg({
        'total': 'sum'
    }).reset_index()

    hours = df_grouped['hour']
    total = df_grouped['total']

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(hours, total, marker='o', color='b', linestyle='-', linewidth=2, markersize=6)

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Total Users')
    ax.set_title('Total Users by Hour of Day')

    for i, value in enumerate(total):
        ax.text(hours[i], value + 5000, format(value, ','), ha='center', va='bottom', fontsize=9)

    ax.set_xticks(range(0, 24)) 
    plt.tight_layout()
    plt.subplots_adjust(top=0.85, bottom=0.2, left=0.15, right=0.95, hspace=0.3, wspace=0.3)
    st.pyplot(fig)