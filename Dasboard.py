import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Dashboard Analisis Data Bike Sharing")
st.subheader("Proyek Analisis Data: Bike Sharing Dataset")
st.write("Nama: **Adedio Daniel Situmeang**")
st.write("Email: **adediodaniel9@gmail.com**")
st.write("ID Dicoding: **Adedio Daniel S**")

# Memuat data
data = pd.read_csv('day.csv')
data['dteday'] = pd.to_datetime(data['dteday'])
data['month'] = data['dteday'].dt.month
data['day_type'] = data['weekday'].apply(lambda x: 'Weekend' if x in [5, 6] else 'Weekday')

# Sidebar untuk memilih jenis analisis
st.sidebar.title("Pilih Analisis")
analysis_type = st.sidebar.selectbox("Pilih jenis analisis:", 
                                     ["Explore Pengaruh Cuaca dan Hari","Tren Penggunaan Sepeda", "Korelasi Cuaca dan Penyewaan", "Analisis Lanjutan"])

# Explore Pengaruh Cuaca dan hari terhadap Jumlah Penyewaan Sepeda
if analysis_type == "Explore Pengaruh Cuaca dan Hari":
    st.header(" Explore Pengaruh Cuaca dan hari terhadap Jumlah Penyewaan Sepeda")
    
    # Mengelompokkan dataset berdasarkan tahun dan bulan
    data_grouped = data.groupby(['yr', 'month'])[['casual', 'registered']].sum()
    
    # Membuat plot untuk melihat perbandingan pengguna
    fig, ax = plt.subplots(figsize=(15, 7))
    data_grouped.plot(kind='bar', ax=ax)
    plt.title('Penggunaan Sepeda Kasual dan Terdaftar Berdasarkan Bulan')
    plt.xlabel('Tahun, Bulan')
    plt.ylabel('Jumlah Pengguna')
    st.pyplot(fig)

# Pertanyaan 2: Faktor cuaca dan suhu mana yang berpengaruh terhadap jumlah total penyewa sepeda
elif analysis_type == "Korelasi Cuaca dan Penyewaan":
    st.header("Korelasi Antara Cuaca, Suhu, dan Jumlah Penyewaan Sepeda")
    
    # Melihat hubungan antara variabel cuaca, suhu, dan jumlah peminjaman
    correlation = data[['weathersit', 'temp', 'cnt']].corr()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
    plt.title('Korelasi antara Cuaca, Suhu, dan Jumlah Peminjaman')
    st.pyplot(fig)

    # Visualisasi Rata-rata Peminjaman Berdasarkan Kondisi Cuaca
    st.subheader("Rata-rata Jumlah Peminjaman Berdasarkan Kondisi Cuaca")
    weather_grouped = data.groupby(['weathersit'])[['cnt']].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    weather_grouped.plot(kind='bar', color='orange', ax=ax)
    plt.title('Rata-rata Jumlah Peminjaman Berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca (1: Clear, 2: Mist, 3: Light Rain)')
    plt.ylabel('Rata-rata Jumlah Peminjaman')
    st.pyplot(fig)

# Pertanyaan 1: Bagaimana tren penggunaan sepeda oleh penyewa terdaftar dan penyewa kasual selama periode waktu tertentu?
elif analysis_type == "Tren Penggunaan Sepeda":
    st.header("Rata-rata Penggunaan Sepeda Berdasarkan Tipe Hari")

    # Menambah kolom 'day_type' untuk membedakan antara hari kerja dan akhir pekan
    day_type_grouped = data.groupby('day_type')[['casual', 'registered']].mean().reset_index()

    # Plot visualisasi
    fig, ax = plt.subplots(figsize=(10, 5))
    day_type_grouped.plot(kind='bar', ax=ax)
    plt.title('Rata-rata Penggunaan Sepeda Berdasarkan Tipe Hari')
    plt.xlabel('Tipe Hari')
    plt.ylabel('Rata-rata Jumlah Pengguna')
    st.pyplot(fig)

    st.write("### Insight:")
    st.write(""" 
    - Pada akhir pekan, pengguna kasual cenderung lebih banyak dibandingkan hari kerja.
    - Pengguna terdaftar lebih dominan pada hari kerja dibandingkan akhir pekan.
    """)

# Analisis Lanjutan (Opsional)
elif analysis_type == "Analisis Lanjutan":
    st.subheader("Analisis Lanjutan: Clustering Data")

    # Binning untuk Jumlah Peminjaman (cnt)
    # Membuat kategori peminjaman: 'Low', 'Medium', 'High'
    bins = [0, 1000, 3000, data['cnt'].max()]
    labels = ['Low', 'Medium', 'High']
    data['cnt_category'] = pd.cut(data['cnt'], bins=bins, labels=labels)

    # Binning untuk Suhu (temp)
    # Membuat kategori suhu: 'Cold', 'Warm', 'Hot'
    temp_bins = [data['temp'].min(), 0.3, 0.6, data['temp'].max()]
    temp_labels = ['Cold', 'Warm', 'Hot']
    data['temp_category'] = pd.cut(data['temp'], bins=temp_bins, labels=temp_labels)

    # Binning untuk Kondisi Cuaca (weathersit)
    # Menyederhanakan kondisi cuaca: 1 = 'Clear', 2 = 'Mist', 3 = 'Light Rain'
    weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Rain'}
    data['weather_category'] = data['weathersit'].map(weather_mapping)

    # Menggabungkan Hasil Kategori
    # Membuat DataFrame baru dengan kategori-kategori yang telah dibentuk
    clustering_df = data[['dteday', 'cnt', 'temp', 'weathersit', 'cnt_category', 'temp_category', 'weather_category']]

    # Visualisasi Hasil Clustering berdasarkan Kategori Jumlah Peminjaman (cnt)
    st.subheader("Distribusi Jumlah Peminjaman Berdasarkan Kategori")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=clustering_df, x='cnt_category', palette='viridis')
    plt.title('Distribusi Jumlah Peminjaman Berdasarkan Kategori (Low, Medium, High)')
    plt.xlabel('Kategori Jumlah Peminjaman')
    plt.ylabel('Jumlah Observasi')
    st.pyplot(fig)

    # Visualisasi Berdasarkan Kategori Suhu (temp)
    st.subheader("Distribusi Pengguna Berdasarkan Kategori Suhu")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=clustering_df, x='temp_category', palette='coolwarm')
    plt.title('Distribusi Pengguna Berdasarkan Kategori Suhu (Cold, Warm, Hot)')
    plt.xlabel('Kategori Suhu')
    plt.ylabel('Jumlah Observasi')
    st.pyplot(fig)

    # Visualisasi Berdasarkan Kategori Cuaca
    st.subheader("Distribusi Pengguna Berdasarkan Kondisi Cuaca")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=clustering_df, x='weather_category', palette='magma')
    plt.title('Distribusi Pengguna Berdasarkan Kondisi Cuaca (Clear, Mist, Light Rain)')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Observasi')
    st.pyplot(fig)

    # Insight dari Clustering
    st.subheader("Insight dari Clustering")
    insight = clustering_df.groupby(['cnt_category', 'temp_category', 'weather_category'], observed=True).size()
    st.write(insight)
