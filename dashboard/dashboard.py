import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('/day.csv')

# Streamlit UI
st.title('Bike Sharing Data Analysis Dashboard')
st.write('Created by: Haiqel Aziizul Hakeem')
st.write('Data Analysis Project - Laskar AI 2025')

# Menampilkan sebagian dataset
st.subheader('Dataset Preview')
st.dataframe(df.head())

# Penyewaan Sepeda per Musim
st.subheader('Penyewaan Sepeda per Musim')
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season'] = df['season'].map(season_mapping)
fig, ax = plt.subplots()
sns.barplot(x=df['season'], y=df['cnt'], hue=df['season'], estimator=sum, ax=ax, palette='viridis', errorbar=None, legend=False)
ax.set_ylabel('Total Rental')
st.pyplot(fig)

# Penyewaan Sepeda berdasarkan Kondisi Cuaca
st.subheader('Penyewaan Sepeda berdasarkan Kondisi Cuaca')
weather_mapping = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
df['weathersit'] = df['weathersit'].map(weather_mapping)
fig, ax = plt.subplots()
sns.barplot(x=df['weathersit'], y=df['cnt'], hue=df['weathersit'], estimator=sum, ax=ax, palette='coolwarm', errorbar=None, legend=False)
ax.set_ylabel('Total Rental')
st.pyplot(fig)

# Penyewaan Sepeda berdasarkan Hari
st.subheader('Penyewaan Sepeda berdasarkan Hari')
weekday_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
df['weekday'] = df['weekday'].map(weekday_mapping)
fig, ax = plt.subplots()
sns.barplot(x=df['weekday'], y=df['cnt'], hue=df['weekday'], estimator=sum, ax=ax, palette='Set2', errorbar=None, legend=False)
ax.set_ylabel('Total Rental')
plt.xticks(rotation=45)
st.pyplot(fig)

# Insights dan Kesimpulan
st.subheader('Insights dan Kesimpulan')
st.write("Puncak penyewaan sepeda paling banyak adalah pada musim gugur. Kemudian paling sedikit adalah pada musim semi. Pada musim gugur, kemungkinan cuaca dan suasana yang ditawarkan lebih menarik para pesepeda. Sedangkan pada musim semi konsumen kurang tertarik untuk menyewa sepeda. Untuk meningkatkan penyewaan ini dapat dilakukan dengan meningkatkan promosi dan marketing penyewaan, dikarenakan faktor lain seperti cuaca sudah mendukung untuk aktivitas bersepeda.")
st.write("Berdasarkan grafik yang diperoleh dapat disimpulkan bahwa cuaca yang cerah meningkatkan jumlah penyewa sepeda. Dapat dilihat bahwa penyewaan terbanyak adalah pada hari kamis. Meski begitu jumlah penyewa yang konstan dengan berbagai jenis cuaca adalah pada saat weekend. Sedangkan weekday, jumlah penyewa sangat bergantung cuaca.")
