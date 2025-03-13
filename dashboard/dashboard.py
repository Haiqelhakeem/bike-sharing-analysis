import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Set page config
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load dataset
df = pd.read_csv('data/day.csv')

# Konversi kolom date menjadi datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Mapping untuk kategori
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_mapping = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain/Snow'}
weekday_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

# Menambahkan kolom mapping
df['season_name'] = df['season'].map(season_mapping)
df['weathersit_name'] = df['weathersit'].map(weather_mapping)
df['weekday_name'] = df['weekday'].map(weekday_mapping)

# Streamlit UI
st.title('Bike Sharing Data Analysis Dashboard')
st.write('Created by: Haiqel Aziizul Hakeem')
st.write('Data Analysis Project - Laskar AI 2025')

# Sidebar untuk filter
st.sidebar.header('Filter Data')
st.sidebar.write("Pilih filter di bawah atau biarkan kosong untuk menampilkan semua data")

# Filter berdasarkan tanggal
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

# Menambahkan opsi untuk memilih rentang tanggal atau semua data
use_date_filter = st.sidebar.checkbox("Filter berdasarkan tanggal", value=False)

if use_date_filter:
    start_date, end_date = st.sidebar.date_input(
        "Rentang Tanggal",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
else:
    start_date, end_date = min_date, max_date

# Filter berdasarkan musim
season_options = list(season_mapping.values())
selected_seasons = st.sidebar.multiselect('Pilih Musim', options=season_options)

# Jika tidak ada yang dipilih, pilih semua
if not selected_seasons:
    selected_seasons = season_options

# Filter berdasarkan cuaca
weather_options = list(weather_mapping.values())
selected_weather = st.sidebar.multiselect('Pilih Kondisi Cuaca', options=weather_options)

# Jika tidak ada yang dipilih, pilih semua
if not selected_weather:
    selected_weather = weather_options

# Apply filters
filtered_df = df[
    (df['dteday'].dt.date >= start_date) & 
    (df['dteday'].dt.date <= end_date) & 
    (df['season_name'].isin(selected_seasons)) &
    (df['weathersit_name'].isin(selected_weather))
]

# Fungsi untuk memformat angka rental
def format_number(number):
    return f"{number:,}".replace(",", ".")

# Metrics Cards
st.subheader('Ringkasan Data')
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric("Total Penyewaan", format_number(total_rentals))

with col2:
    avg_rentals = filtered_df['cnt'].mean()
    st.metric("Rata-rata Penyewaan per Hari", f"{avg_rentals:.2f}")

with col3:
    if not filtered_df.empty:
        max_rental_day = filtered_df.loc[filtered_df['cnt'].idxmax()]
        st.metric("Hari dengan Penyewaan Tertinggi", 
                f"{max_rental_day['dteday'].strftime('%d %b %Y')} ({format_number(max_rental_day['cnt'])})")
    else:
        st.metric("Hari dengan Penyewaan Tertinggi", "Tidak ada data")

# Status filter aktif
if use_date_filter or selected_seasons != season_options or selected_weather != weather_options:
    st.info(f"Data difilter: {filtered_df.shape[0]} dari {df.shape[0]} baris ditampilkan")
else:
    st.success("Menampilkan semua data")

# Menampilkan sebagian dataset
st.subheader('Dataset Preview')
st.dataframe(filtered_df.head())

# Visualisasi dalam 2 kolom
col1, col2 = st.columns(2)

# Penyewaan Sepeda per Musim
with col1:
    st.subheader('Penyewaan Sepeda per Musim')
    if not filtered_df.empty:
        season_data = filtered_df.groupby('season_name')['cnt'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = sns.barplot(x='season_name', y='cnt', data=season_data, palette='viridis', errorbar=None, ax=ax)
        # Anotasi
        for i, p in enumerate(bars.patches):
            bars.annotate(format_number(p.get_height()), 
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha = 'center', va = 'bottom',
                       xytext = (0, 5), textcoords = 'offset points')
        ax.set_ylabel('Total Rental')
        ax.set_title('Total Penyewaan Berdasarkan Musim')
        st.pyplot(fig)
    else:
        st.write("Tidak ada data untuk ditampilkan")

# Penyewaan Sepeda berdasarkan Kondisi Cuaca
with col2:
    st.subheader('Penyewaan Sepeda berdasarkan Kondisi Cuaca')
    if not filtered_df.empty:
        weather_data = filtered_df.groupby('weathersit_name')['cnt'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = sns.barplot(x='weathersit_name', y='cnt', data=weather_data, palette='coolwarm', errorbar=None, ax=ax)
        # Anotasi
        for i, p in enumerate(bars.patches):
            bars.annotate(format_number(p.get_height()), 
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha = 'center', va = 'bottom',
                       xytext = (0, 5), textcoords = 'offset points')
        ax.set_ylabel('Total Rental')
        ax.set_title('Total Penyewaan Berdasarkan Kondisi Cuaca')
        st.pyplot(fig)
    else:
        st.write("Tidak ada data untuk ditampilkan")

# Penyewaan Sepeda berdasarkan Hari
st.subheader('Penyewaan Sepeda berdasarkan Hari')
if not filtered_df.empty:
    weekday_data = filtered_df.groupby('weekday_name')['cnt'].sum().reset_index()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_data['weekday_name'] = pd.Categorical(weekday_data['weekday_name'], categories=weekday_order, ordered=True)
    weekday_data = weekday_data.sort_values('weekday_name')
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = sns.barplot(x='weekday_name', y='cnt', data=weekday_data, palette='Set2', errorbar=None, ax=ax)
    # Anotasi
    for i, p in enumerate(bars.patches):
        bars.annotate(format_number(p.get_height()), 
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center', va = 'bottom',
                   xytext = (0, 5), textcoords = 'offset points')
    ax.set_ylabel('Total Rental')
    plt.xticks(rotation=30)
    st.pyplot(fig)
else:
    st.write("Tidak ada data untuk ditampilkan")

# Visualisasi tren waktu
st.subheader('Tren Penyewaan Sepeda Berdasarkan Waktu')
if not filtered_df.empty:
    time_trend = filtered_df.groupby('dteday')['cnt'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.plot(time_trend['dteday'], time_trend['cnt'], color='#1f77b4')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penyewaan')
    plt.title('Tren Penyewaan Sepeda Harian')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.write("Tidak ada data untuk ditampilkan")

### Visualisasi Utama ###
st.title('Visualisasi Utama')

# Mapping musim
season_mapping = {
    1: 'Spring', 
    2: 'Summer', 
    3: 'Fall', 
    4: 'Winter'
}
df['season'] = df['season'].map(season_mapping)

# Mapping cuaca
weather_map = {
    1: 'Clear',
    2: 'Mist/Cloudy',
    3: 'Light Rain/Snow',
}
df['weather_label'] = df['weathersit'].map(weather_map)

# Mapping Hari
weekday_map = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}
df['weekday_label'] = df['weekday'].map(weekday_map)

# Urutkan hari sesuai urutan kalender
df['weekday_label'] = pd.Categorical(
    df['weekday_label'],
    categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    ordered=True
)

# Rata-rata Penyewaan Sepeda per Musim
st.subheader('Rata-rata Penyewaan Sepeda per Musim')
seasonal_trends = df.groupby('season').agg({
    'cnt': 'mean'
}).sort_values(by='cnt', ascending=False).reset_index()
plt.figure(figsize=(8, 5))
season_barplot = sns.barplot(
    x='season',
    y='cnt',
    hue='season',
    data=seasonal_trends,
    palette='plasma',
    legend=False
)
# Anotasi
for p in season_barplot.patches:
    season_barplot.annotate(
        f"{p.get_height():.0f}",  
        (p.get_x() + p.get_width() / 2, p.get_height()),  
        ha='center', va='bottom', fontsize=10, color='black'
    )
plt.ylabel('Rata-rata Rental')
plt.xlabel('Musim')
st.pyplot(plt.gcf())

# Rata-rata Penyewaan Sepeda per Musim Semi
spring_data = df[df['season'] == 'Spring']
weather_in_spring = spring_data['weather_label'].value_counts().reset_index()
weather_in_spring.columns = ['Weather Condition', 'Count']
st.subheader('Kondisi Cuaca di Musim Semi')
plt.figure(figsize=(10, 6))
spring_barplot = sns.barplot(
    x='Weather Condition',
    y='Count',
    hue='Weather Condition',
    data=weather_in_spring,
    palette='plasma',
    legend=False
)
# Anotasi
for p in spring_barplot.patches:
    spring_barplot.annotate(
        f"{p.get_height():.0f}",
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha='center', va='bottom', fontsize=10, color='black'
    )
plt.title('Kondisi Cuaca di Musim Semi')
plt.xlabel('Cuaca')
plt.ylabel('Jumlah Sewa')
st.pyplot(plt.gcf())

# Pengaruh dari Cuaca dan Hari
weather_day_impact = df.groupby(by=['weather_label', 'weekday_label']).agg({
    'casual': 'mean',
    'registered': 'mean',
    'cnt': 'mean'
}).sort_values(by='weekday_label', ascending=False).reset_index()

# Plot Pengaruh dari Cuaca dan Hari
st.subheader('Plot Pengaruh dari Cuaca dan Hari terhadap Total Rental')
plt.figure(figsize=(14, 8))
sns.lineplot(
    x='weekday_label',
    y='cnt',
    hue='weather_label',
    data=weather_day_impact,
    marker='o',
    palette='plasma'
)

plt.title('Pengaruh dari Cuaca dan Hari terhadap Total Rental')
plt.xlabel('Hari')
plt.ylabel('Rata-rata Rental')
plt.legend(title='Cuaca')
plt.grid(True)

# Display the plot in Streamlit
st.pyplot(plt.gcf()) 

# Insights dan Kesimpulan
st.subheader('Insights dan Kesimpulan')

# Insights berdasarkan data yang difilter
if not filtered_df.empty:
    popular_season = filtered_df.groupby('season_name')['cnt'].sum().idxmax()
    popular_weather = filtered_df.groupby('weathersit_name')['cnt'].sum().idxmax()
    popular_day = filtered_df.groupby('weekday_name')['cnt'].sum().idxmax()

    st.write(f"""
    ### Berdasarkan data yang difilter:

    1. **Musim Terpopuler**: {popular_season} merupakan musim dengan jumlah penyewaan sepeda terbanyak. Pada musim ini, cuaca dan kondisi lingkungan kemungkinan lebih mendukung aktivitas bersepeda.

    2. **Kondisi Cuaca Ideal**: Kondisi cuaca {popular_weather} menunjukkan jumlah penyewaan tertinggi, membuktikan bahwa faktor cuaca sangat mempengaruhi keputusan konsumen untuk menyewa sepeda.

    3. **Hari Terpopuler**: {popular_day} adalah hari dengan jumlah penyewaan tertinggi. Hal ini dapat menjadi pertimbangan untuk strategi alokasi dan promosi.

    4. **Rekomendasi**:
       - Tingkatkan persediaan sepeda pada musim {popular_season} dan saat cuaca {popular_weather}
       - Kembangkan promosi khusus untuk meningkatkan penyewaan pada musim dengan aktivitas bersepeda yang rendah
       - Pertimbangkan strategi harga yang berbeda berdasarkan musim dan kondisi cuaca
    """)

    st.write("Untuk meningkatkan penyewaan di periode dengan permintaan rendah, dapat dilakukan peningkatan promosi dan program marketing khusus. Sedangkan pada periode puncak, pastikan ketersediaan dan pemeliharaan sepeda yang cukup untuk memenuhi permintaan.")
else:
    st.write("Tidak ada data yang tersedia untuk analisis.")

st.title("Analisis Utama Penyewaan Sepeda")

st.write("1. Pada musim apa penyewaan sepeda paling banyak dan kapan penyewaan paling sedikit? Apa yang dapat dilakukan untuk meningkatkan penyewaan?")
st.markdown(
    """ 
    * Puncak penyewaan sepeda paling banyak adalah pada **musim gugur**. Kemudian paling sedikit adalah pada **musim semi**. 
    * Pada musim gugur, kemungkinan cuaca dan suasana yang ditawarkan lebih menarik para pesepeda. 
    * Sedangkan pada musim semi konsumen kurang tertarik untuk menyewa sepeda. 
    * Untuk meningkatkan penyewaan ini dapat dilakukan dengan meningkatkan **promosi dan marketing penyewaan**, dikarenakan faktor lain seperti cuaca sudah mendukung untuk aktivitas bersepeda.
    """
)

st.write("2. Apa pengaruh cuaca dan hari terhadap tingkat penyewaan sepeda?")
st.markdown(
    """ 
    * Berdasarkan grafik yang diperoleh dapat disimpulkan bahwa **cuaca yang cerah meningkatkan jumlah penyewa sepeda**.
    * Dapat dilihat bahwa **penyewaan terbanyak adalah pada hari Kamis**.
    * Meski begitu, jumlah penyewa yang konstan dengan berbagai jenis cuaca adalah pada saat **weekend**.
    * Sedangkan **weekday, jumlah penyewa sangat bergantung pada cuaca**.
    """
)