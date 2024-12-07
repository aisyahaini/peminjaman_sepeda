# Analisis Jumlah Peminjaman Sepeda
## Dashboard
Dalam analisis ini, membuat aplikasi berbasis website menggunakan Streamlit.
Berikut untuk link deploy: https://jumlah-peminjaman-sepeda.streamlit.app/

## Project Bike Sharing
Project ini dibuat sebagai tugas akhir dari modul yang berjudul "Belajar Analisis Data dengan Python" dari Dicoding. Disini saya berfokus pada analisis data persebaran jumlah cuaca, temperature, dan kelembapan pada peminjaman sepeda ini. Tujuan dari tugas akhir ini untuk menganalisis lebih lanjut dari dataset peminjaman sepeda.

## Dataset
Pada project ini, saya menggunakan dataset yang berjudul "Bike Sharing Dataset (Day) yang bersumber dari: https://raw.githubusercontent.com/aisyahaini/dicoding_project/refs/heads/main/data%20science/Proyek%20akhir%20dicoding%20bike%20sharing%20dataset/day.csv

## Cara Membuat Dashboard
Berikut ini cara untuk membuat dashboard:
### Setup Environment
#### 1. Membuat Environment Baru
Dapat menginstall syntax berikut untuk menciptakan lingkungan terisolasi yang terpisah dari instalasi Python utama
  `conda create --name bikesharing-ds python=3.9`

#### 2. Mengaktifkan Environment
Dapat mengaktifkan lingkungan `bikesharing-ds` dengan syntax berikut:
  `conda activate bikesharing-ds`

#### 3. Menginstall Library dengan `pip`
Menginstall library yang dibutuhkan dengan syntax berikut:
`pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel`

atau dapat menggunakan syntax berikut:
`pip install -r requirements.txt` 
File requirements.txt berisi banyak library yang langsung dapat diinstall



### Running Streamlit Application
#### 1. Memastikan file yang berisi dashboard Streamlit disimpan dimana dengan mencari directory path, misalnya seperti ini 
`dashboard/Streamlit_Bike_Sharing.py`
#### 2. Running Streamlit App dengan syntax berikut:
`streamlit run dashboard/Streamlit_Bike_Sharing.py`


## Author
**Proyek Analisis Data: Bike Sharing Dataset - Day**
- **Nama:** Aisyah Nuraini
- **Email:** aisyahnuraini047@gmail.com
- **ID Dicoding:** aisyahaini