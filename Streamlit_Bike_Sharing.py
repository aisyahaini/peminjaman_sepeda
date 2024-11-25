import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# Data dibaca dari file CSV
df = pd.read_csv("dataset_cleaned.csv")

# Pastikan tidak ada nilai kosong pada kolom 'weathersit' dan 'cnt'
df = df.dropna(subset=['weathersit', 'cnt'])

# Judul aplikasi
st.title("Analisis dan Prediksi Jumlah Peminjaman Sepeda")

# Memilih parameter analisis
st.sidebar.title("Parameter Analisis")
cuaca = st.sidebar.selectbox(
    "Pilih kondisi cuaca:",
    ("Cerah/Mendung", "Berkabut/Gerimis", "Hujan Ringan/Snow"),
    key="cuaca"
)

hari = st.sidebar.selectbox(
    "Pilih jenis hari:",
    ("Hari Kerja", "Akhir Pekan"),
    key="hari"
)

# Menggunakan slider tunggal untuk suhu dan kelembapan tanpa batas minimum dan maksimum
temp = st.sidebar.slider("Suhu (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="temp")
hum = st.sidebar.slider("Kelembapan (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="hum")

# Filter data berdasarkan parameter
if cuaca == "Cerah/Mendung":
    cuaca_filter = df['weathersit'] == 1
elif cuaca == "Berkabut/Gerimis":
    cuaca_filter = df['weathersit'] == 2
else:
    cuaca_filter = df['weathersit'] == 3

hari_filter = (df['workingday'] == (hari == "Hari Kerja"))
temp_filter = (df['temp'] >= temp - 0.05) & (df['temp'] <= temp + 0.05)  # Filter based on a narrow range around the selected temp
hum_filter = (df['hum'] >= hum - 0.05) & (df['hum'] <= hum + 0.05)  # Filter based on a narrow range around the selected hum

# Menggabungkan semua filter
filtered_data = df[cuaca_filter & hari_filter & temp_filter & hum_filter]

# Menghitung prediksi jumlah peminjaman sepeda (rata-rata 'cnt' berdasarkan data yang difilter)
if not filtered_data.empty:
    jumlah_peminjaman = int(filtered_data['cnt'].mean())  # Menghitung rata-rata peminjaman sepeda
else:
    jumlah_peminjaman = 0  # Jika tidak ada data yang cocok, set jumlah peminjaman ke 0

# Menampilkan jumlah peminjaman sepeda
st.write("## Jumlah Peminjaman Sepeda")
st.markdown(f"<h1 style='text-align: center;'>{jumlah_peminjaman} sepeda</h1>", unsafe_allow_html=True)

# Dropdown untuk memilih jenis visualisasi
visualisasi_option = st.selectbox(
    "Pilih jenis visualisasi:",
    ["Visualisasi Cuaca", "Hubungan Suhu dan Peminjaman", "Hubungan Kelembapan dan Peminjaman"]
)

# Visualisasi sesuai pilihan
if visualisasi_option == "Visualisasi Cuaca":
    fig, ax = plt.subplots()
    if not filtered_data.empty:
        grouped = filtered_data.groupby('weathersit')['cnt'].mean()
        grouped.plot(kind='bar', ax=ax, color='skyblue')

        # Menambahkan angka di atas setiap batang
        for i, v in enumerate(grouped):
            ax.text(i, v + 5, f'{int(v)}', ha='center', va='bottom', fontsize=10)  # Menampilkan angka di atas batang

        ax.set_title("Rata-rata Peminjaman Berdasarkan Cuaca")
        ax.set_xlabel("Cuaca")
        ax.set_ylabel("Rata-rata Peminjaman")
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
