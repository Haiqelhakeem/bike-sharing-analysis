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

# Apply mapping
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
selected_seasons = st.sidebar.multiselect('Pilih Musim (kosongkan untuk semua)', options=season_options)

# Jika tidak ada yang dipilih, pilih semua
if not selected_seasons:
    selected_seasons = season_options

# Filter berdasarkan cuaca
weather_options = list(weather_mapping.values())
selected_weather = st.sidebar.multiselect('Pilih Kondisi Cuaca (kosongkan untuk semua)', options=weather_options)

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

# Tombol untuk reset semua filter
if st.sidebar.button("Reset Semua Filter"):
    # Tidak perlu melakukan apa-apa karena filter akan direset otomatis
    # pada refresh halaman
    st.experimental_rerun()

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
        
        # Tambahkan label pada bars
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
        
        # Tambahkan label pada bars
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
    # Urutkan hari sesuai urutan kalender
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_data['weekday_name'] = pd.Categorical(weekday_data['weekday_name'], categories=weekday_order, ordered=True)
    weekday_data = weekday_data.sort_values('weekday_name')

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = sns.barplot(x='weekday_name', y='cnt', data=weekday_data, palette='Set2', errorbar=None, ax=ax)

    # Tambahkan label pada bars
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
    plt.plot(time_trend['dteday'], time_trend['cnt'], marker='o', linestyle='-', color='#1f77b4')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penyewaan')
    plt.title('Tren Penyewaan Sepeda Harian')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.write("Tidak ada data untuk ditampilkan")

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