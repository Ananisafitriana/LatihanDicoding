import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataHari = pd.read_csv("./data/day.csv")
dataJam = pd.read_csv("./data/hour.csv")
dataHari['dteday'] = pd.to_datetime(dataHari['dteday'])

st.title("📊 Dashboard Penyewaan Sepeda")
st.sidebar.title("🔍 Filter Data")

# Filter tanggal
start_date = st.sidebar.date_input("Mulai Tanggal", dataHari['dteday'].min())
end_date = st.sidebar.date_input("Sampai Tanggal", dataHari['dteday'].max())

# Filter musim 
season_options = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
selected_season = st.sidebar.multiselect("Pilih Musim", options=season_options.keys(), format_func=lambda x: season_options[x])

# Filter cuaca
weather_options = {1: "Clear", 2: "Mist", 3: "Light Snow/Rain", 4: "Heavy Rain/Snow"}
selected_weather = st.sidebar.multiselect("Pilih Cuaca", options=weather_options.keys(), format_func=lambda x: weather_options[x])

data_filtered = dataHari[(dataHari['dteday'] >= pd.Timestamp(start_date)) & (dataHari['dteday'] <= pd.Timestamp(end_date))]
if selected_season:
    data_filtered = data_filtered[data_filtered['season'].isin(selected_season)]
if selected_weather:
    data_filtered = data_filtered[data_filtered['weathersit'].isin(selected_weather)]

view_option = st.sidebar.radio("Pilih data yang ingin ditampilkan:", ["Statistik Deskriptif", "Visualisasi Penyewaan"])

# Statistik Deskriptif
if view_option == "Statistik Deskriptif":
    st.subheader("📊 Statistik Deskriptif Data Hari")
    st.write(data_filtered.describe())
    
    # EDA Bivariate
    st.subheader("🔄 EDA Bivariate: Korelasi Antar Variabel")
    numeric_data = data_filtered.select_dtypes(include=["number"])
    correlation_matrix = numeric_data.corr()
    st.write(correlation_matrix)
    
    # EDA Numerikal
    st.subheader("📉 EDA Numerikal: Ringkasan Data Numerik")
    st.write(data_filtered[["temp", "hum", "windspeed", "casual", "registered", "cnt"]].describe())

    # Agregasi penyewa per bulan
    st.subheader("📉 Penyewa Per Bulan")
    monthly_avg = dataHari.groupby("mnth")["cnt"].mean().reset_index()
    monthly_avg = monthly_avg.sort_values(by="cnt", ascending=False) 
    st.write(monthly_avg)

    # Agregasi Penyewa per musim
    st.subheader("📉 Penyewa Per Musim")
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    avg_users_hari = dataHari.groupby("season")["cnt"].mean()
    avg_users_jam = dataJam.groupby("season")["cnt"].mean()
    avg_users_hari.index = avg_users_hari.index.map(season_labels)
    avg_users_jam.index = avg_users_jam.index.map(season_labels)

    df_summary = pd.DataFrame({
        "Rata-rata Harian": avg_users_hari,
        "Rata-rata Per Jam": avg_users_jam
    })
    st.write(df_summary)

    # Agregasi Pengaruh Hari Kerja
    st.subheader("📉 Penyewa Pengaruh Hari Kerja")
    workday_effect = dataHari.groupby("workingday")[["casual", "registered"]].mean()
    st.write(workday_effect)

    # Agregasi Binning Suhu
    st.subheader("📊 Rata-rata Penyewaan Berdasarkan Kategori Suhu")

    bins = [0, 0.3, 0.6, 1.0]  
    labels = ["Dingin", "Sedang", "Hangat"]

    dataHari["temp_category"] = pd.cut(dataHari["temp"], bins=bins, labels=labels, include_lowest=True)

    temp_summary = dataHari.groupby("temp_category", observed=False)["cnt"].mean().reset_index()
    temp_summary["temp_category"] = temp_summary["temp_category"].astype(str)

    st.write(temp_summary)



    
# Visualisasi Penyewaan
elif view_option == "Visualisasi Penyewaan":

    # Penyewaan Sepeda per Bulan
    st.subheader("📅 Rata-rata Penyewaan Sepeda per Bulan")
    monthly_trend = data_filtered.groupby("mnth")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(monthly_trend, marker="o", linestyle="-", color="b")
    plt.xticks(range(1, 13), ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Penyewa")
    plt.grid(True)
    st.pyplot(fig)
    
    # Penyewaan Sepeda per Musim 
    st.subheader("🌤️ Rata-rata Penyewaan Sepeda per Musim")
    avg_users = data_filtered.groupby("season")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=avg_users.index, y=avg_users.values, palette="coolwarm")
    ax.set_xticklabels([season_options[i] for i in avg_users.index], rotation=0)
    st.pyplot(fig)
    
    # Pengaruh Hari Kerja terhadap Penyewaan
    st.subheader("📆 Perbandingan Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")
    workday_effect = data_filtered.groupby("workingday")[['casual', 'registered']].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    workday_effect.plot(kind="bar", stacked=True, ax=ax, color=["orange", "blue"])
    ax.set_xticklabels(["Akhir Pekan / Libur", "Hari Kerja"], rotation=0)
    st.pyplot(fig)
    
    # Penyewaan Berdasarkan Jam
    st.subheader("⏰ Tren Penyewaan Sepeda Berdasarkan Jam")
    hourly_trend = dataJam.groupby("hr")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(hourly_trend, marker="o", linestyle="-", color="g")
    plt.xticks(range(0, 24))
    plt.grid(True)
    st.pyplot(fig)
    
    # Pengaruh Cuaca terhadap Penyewaan Sepeda
    st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")
    weather_effect = data_filtered.groupby("weathersit")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(x=weather_effect.index, y=weather_effect.values, palette="coolwarm")
    ax.set_xticklabels([weather_options[i] for i in weather_effect.index], rotation=0)
    st.pyplot(fig)
