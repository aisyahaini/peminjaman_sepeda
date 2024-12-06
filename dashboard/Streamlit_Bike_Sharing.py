import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend tanpa GUI
import matplotlib.pyplot as plt


# Data dibaca dari file CSV
df = pd.read_csv("dashboard/dataset_cleaned.csv", delimiter=',')
df.columns = df.columns.str.strip()

# Pastikan tidak ada nilai kosong pada kolom 'weathersit' dan 'cnt'
#df = df.dropna(subset=['weathersit', 'cnt'])

# Judul aplikasi
st.title("Analisis Jumlah Peminjaman Sepeda")

# Dropdown dengan opsi "Semua Cuaca" dan "Semua Hari"
st.sidebar.title("Parameter Analisis")
cuaca = st.sidebar.selectbox(
    "Pilih kondisi cuaca:",
    ("Semua Cuaca", "Cerah/Mendung", "Berkabut/Gerimis", "Hujan Ringan/Snow"),
    key="cuaca"
)

hari = st.sidebar.selectbox(
    "Pilih jenis hari:",
    ("Semua Hari", "Hari Kerja", "Akhir Pekan"),
    key="hari"
)

# Slider untuk suhu dan kelembapan
temp = st.sidebar.slider("Suhu (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="temp")
hum = st.sidebar.slider("Kelembapan (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="hum")

# Logika filter cuaca
cuaca_mapping = {
    "Cerah/Mendung": 1,
    "Berkabut/Gerimis": 2,
    "Hujan Ringan/Snow": 3
}
# Filter cuaca
if cuaca == "Cerah/Mendung":
    cuaca_filter = df['weathersit'] == 1
elif cuaca == "Berkabut/Gerimis":
    cuaca_filter = df['weathersit'] == 2
elif cuaca == "Hujan Ringan/Snow":
    cuaca_filter = df['weathersit'] == 3
else:  # Jika pilih "Semua Cuaca"
    cuaca_filter = True  # Ini akan mencakup semua baris

# Filter hari
if hari == "Hari Kerja":
    hari_filter = df['workingday'] == 1
elif hari == "Akhir Pekan":
    hari_filter = df['workingday'] == 0
else:  # Jika pilih "Semua Hari"
    hari_filter = True  # Ini akan mencakup semua baris

# Filter suhu dan kelembapan
temp_filter = (df['temp'] >= temp - 0.05) & (df['temp'] <= temp + 0.05)
hum_filter = (df['hum'] >= hum - 0.05) & (df['hum'] <= hum + 0.05)

# Gabungkan semua filter
filtered_data = df[cuaca_filter & hari_filter & temp_filter & hum_filter]


# Menghitung prediksi jumlah peminjaman sepeda
if not filtered_data.empty:
    jumlah_peminjaman = int(filtered_data['cnt'].sum())  # Menghitung total peminjaman sepeda
else:
    jumlah_peminjaman = 0

# Menampilkan jumlah peminjaman sepeda
st.write("## Jumlah Peminjaman Sepeda")
st.markdown(f"<h1 style='text-align: center;'>{jumlah_peminjaman} sepeda</h1>", unsafe_allow_html=True)

# Dropdown untuk memilih jenis visualisasi
visualisasi_option = st.selectbox(
    "Pilih jenis visualisasi:",
    ["Visualisasi Cuaca", "Hubungan Suhu dan Peminjaman", "Hubungan Kelembapan dan Peminjaman"]
)

# Logika visualisasi sesuai pilihan
if visualisasi_option == "Visualisasi Cuaca":
    fig, ax = plt.subplots()
    if not filtered_data.empty:
        # Mengelompokkan data berdasarkan cuaca dan menghitung total
        grouped = filtered_data.groupby('weathersit')['cnt'].sum()

        # Menambahkan kategori yang tidak ada dalam data hasil filter
        for weather in [1, 2, 3]:
            if weather not in grouped.index:
                grouped.loc[weather] = 0

        # Mengganti indeks angka menjadi label deskriptif
        grouped.index = grouped.index.map({1: "Cerah/Mendung", 2: "Berkabut/Gerimis", 3: "Hujan Ringan/Snow"})

        grouped = grouped.sort_index()  # Memastikan urutan kategori tetap konsisten

        grouped.plot(kind='bar', ax=ax, color='skyblue')

        # Menambahkan angka di atas setiap batang
        for i, v in enumerate(grouped):
            ax.text(i, v + 5, f'{int(v)}', ha='center', va='bottom', fontsize=10)

        ax.set_title("Jumlah Peminjaman Berdasarkan Cuaca")
        ax.set_xlabel("Cuaca")
        ax.set_ylabel("Jumlah Peminjaman")
        ax.set_xticklabels(grouped.index, rotation=0)
    else:
        st.write("Data tidak ditemukan untuk filter yang dipilih")
    st.pyplot(fig)
elif visualisasi_option == "Hubungan Suhu dan Peminjaman":
    fig, ax = plt.subplots()
    ax.scatter(filtered_data['temp'], filtered_data['cnt'], alpha=0.5, color='green')
    ax.set_title("Hubungan Suhu dengan Jumlah Peminjaman")
    ax.set_xlabel("Suhu")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)
elif visualisasi_option == "Hubungan Kelembapan dan Peminjaman":
    fig, ax = plt.subplots()
    ax.scatter(filtered_data['hum'], filtered_data['cnt'], alpha=0.5, color='orange')
    ax.set_title("Hubungan Kelembapan dengan Jumlah Peminjaman")
    ax.set_xlabel("Kelembapan")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)
