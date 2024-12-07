import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend tanpa GUI
import matplotlib.pyplot as plt
import numpy as np

# Membaca data dari file CSV
df = pd.read_csv("dashboard/dataset_cleaned.csv", delimiter=',')
df.columns = df.columns.str.strip()

# Judul aplikasi
st.title("Analisis Jumlah Peminjaman Sepeda")

# Sidebar untuk parameter analisis
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

if cuaca == "Semua Cuaca":
    cuaca_filter = True  # Tidak memfilter
else:
    cuaca_filter = df['weathersit'] == cuaca_mapping[cuaca]

# Logika filter hari
if hari == "Hari Kerja":
    hari_filter = df['workingday'] == 1
elif hari == "Akhir Pekan":
    hari_filter = df['workingday'] == 0
else:
    hari_filter = True  # Tidak memfilter

# Filter suhu dan kelembapan dengan toleransi lebih luas
temp_filter = (df['temp'] >= temp - 0.1) & (df['temp'] <= temp + 0.1)
hum_filter = (df['hum'] >= hum - 0.1) & (df['hum'] <= hum + 0.1)

# Gabungkan semua filter
filtered_data = df[cuaca_filter & hari_filter & temp_filter & hum_filter]

# Menampilkan jumlah peminjaman sepeda
jumlah_peminjaman = int(filtered_data['cnt'].sum()) if not filtered_data.empty else 0

st.write("## Jumlah Peminjaman Sepeda")
st.markdown(f"<h1 style='text-align: center;'>{jumlah_peminjaman} sepeda</h1>", unsafe_allow_html=True)

# Dropdown untuk memilih jenis visualisasi
visualisasi_option = st.selectbox(
    "Pilih jenis visualisasi:",
    ["Visualisasi Hari dan Cuaca", "Hubungan Suhu dan Peminjaman", "Hubungan Kelembapan dan Peminjaman"]
)

if visualisasi_option == "Visualisasi Hari dan Cuaca":
    if not filtered_data.empty:
        fig, ax = plt.subplots()

        # Kelompokkan data berdasarkan hari kerja dan cuaca
        grouped = filtered_data.groupby(['workingday', 'weathersit'])['cnt'].sum().reset_index()
        grouped['workingday'] = grouped['workingday'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})
        grouped['weathersit'] = grouped['weathersit'].map({1: "Cerah/Mendung", 2: "Berkabut/Gerimis", 3: "Hujan Ringan/Snow"})

        # Filter berdasarkan pilihan hari
        if hari == "Hari Kerja":
            grouped = grouped[grouped['workingday'] == "Hari Kerja"]
        elif hari == "Akhir Pekan":
            grouped = grouped[grouped['workingday'] == "Akhir Pekan"]

        # Pivot data untuk visualisasi
        pivoted = grouped.pivot(index='workingday', columns='weathersit', values='cnt').fillna(0)

        # Bar positions
        bar_width = 0.2
        x_labels = pivoted.index.tolist()
        x = np.arange(len(x_labels))

        # Plot setiap kategori cuaca sebagai bar terpisah
        colors = ['skyblue', 'orange', 'palegreen']  # Warna untuk setiap kategori cuaca
        for i, cuaca_type in enumerate(["Cerah/Mendung", "Berkabut/Gerimis", "Hujan Ringan/Snow"]):
            bar_values = pivoted[cuaca_type] if cuaca_type in pivoted.columns else [0] * len(x)
            bars = ax.bar(
                x + i * bar_width,
                bar_values,
                width=bar_width,
                label=cuaca_type,
                color=colors[i]
            )

            # Tambahkan angka di atas setiap bar
            for bar in bars:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 5,
                    f'{int(bar.get_height())}',
                    ha='center',
                    va='bottom',
                    fontsize=10
                )

        # Kustomisasi plot
        ax.set_title("Jumlah Peminjaman Berdasarkan Hari dan Cuaca")
        ax.set_xlabel("Jenis Hari")
        ax.set_ylabel("Jumlah Peminjaman")
        ax.set_xticks(x + bar_width)
        ax.set_xticklabels(x_labels)
        ax.legend(title="Kondisi Cuaca")

        st.pyplot(fig)
    else:
        # Menampilkan pesan saat data tidak ditemukan
        st.write("### Data tidak ditemukan dari parameter yang diinputkan")

elif visualisasi_option == "Hubungan Suhu dan Peminjaman":
    if not filtered_data.empty:
        fig, ax = plt.subplots()
        ax.scatter(filtered_data['temp'], filtered_data['cnt'], alpha=0.5, color='green')
        ax.set_title("Hubungan Suhu dengan Jumlah Peminjaman")
        ax.set_xlabel("Suhu")
        ax.set_ylabel("Jumlah Peminjaman")
        st.pyplot(fig)
    else:
        st.write("### Data tidak ditemukan dari parameter yang diinputkan. ")

elif visualisasi_option == "Hubungan Kelembapan dan Peminjaman":
    if not filtered_data.empty:
        fig, ax = plt.subplots()
        ax.scatter(filtered_data['hum'], filtered_data['cnt'], alpha=0.5, color='orange')
        ax.set_title("Hubungan Kelembapan dengan Jumlah Peminjaman")
        ax.set_xlabel("Kelembapan")
        ax.set_ylabel("Jumlah Peminjaman")
        st.pyplot(fig)
    else:
        st.write("### Data tidak ditemukan dari parameter yang diinputkan. ")
