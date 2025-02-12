import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataHari = pd.read_csv("./data/day.csv")
dataJam = pd.read_csv("./data/hour.csv")

st.title("📊 Dashboard Penyewaan Sepeda")

# Sidebar
st.sidebar.title("🔍 Filter Data")
view_option = st.sidebar.radio(
    "Pilih data yang ingin ditampilkan:", 
    ["Statistik Deskriptif", "Visualisasi Penyewaan"]
)

# Statistik Deskriptif
if view_option == "Statistik Deskriptif":
    st.subheader("📊 Statistik Deskriptif Data Hari")
    st.write(dataHari.describe())

    st.subheader("📊 Statistik Deskriptif Data Jam")
    st.write(dataJam.describe())
    

# Visualisasi
elif view_option == "Visualisasi Penyewaan":

    # Penyewaan Sepeda per Bulan
    st.subheader("📅 Rata-rata Penyewaan Sepeda per Bulan")

    monthly_trend = dataHari.groupby("mnth")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(monthly_trend, marker="o", linestyle="-", color="b")
    plt.xticks(ticks=range(1, 13), labels=["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
    plt.title("Rata-rata Penyewaan Sepeda per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Penyewa")
    plt.grid(True)
    st.pyplot(fig)

    # Penyewaan Sepeda per Musim 
    st.subheader("🌤️ Rata-rata Penyewaan Sepeda per Musim")

    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    
    avg_users_hari = dataHari.groupby("season")["cnt"].mean()
    avg_users_jam = dataJam.groupby("season")["cnt"].mean()

    avg_users_hari.index = avg_users_hari.index.map(season_labels)
    avg_users_jam.index = avg_users_jam.index.map(season_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(avg_users_hari.index, avg_users_hari, color="skyblue", alpha=0.7, label="Harian")
    ax.bar(avg_users_jam.index, avg_users_jam, color="orange", alpha=0.7, label="Per Jam")
    ax.set_title("Rata-rata Penyewaan Sepeda per Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Pengguna Sepeda")
    ax.legend()
    st.pyplot(fig)

    # Pengaruh Hari Kerja terhadap Penyewaan
    st.subheader("📆 Perbandingan Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")

    workday_effect = dataHari.groupby("workingday")[["casual", "registered"]].mean()

    fig, ax = plt.subplots(figsize=(8, 5))
    workday_effect.plot(kind="bar", stacked=True, ax=ax, color=["orange", "blue"])
    ax.set_xticklabels(["Akhir Pekan / Libur", "Hari Kerja"], rotation=0)
    ax.set_title("Perbandingan Penggunaan Sepeda pada Hari Kerja dan Akhir Pekan")
    ax.set_ylabel("Rata-rata Penyewa")
    ax.legend(["Casual", "Registered"])
    st.pyplot(fig)

    # Penyewaan Berdasarkan Jam
    st.subheader("⏰ Tren Penyewaan Sepeda Berdasarkan Jam")

    hourly_trend = dataJam.groupby("hr")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(hourly_trend, marker="o", linestyle="-", color="g")
    plt.xticks(ticks=range(0, 24))
    plt.title("Tren Penyewaan Sepeda Berdasarkan Jam")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Penyewa")
    plt.grid(True)
    st.pyplot(fig)

    # Pengaruh Cuaca terhadap Penyewaan Sepeda
    st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")

    weather_effect = dataHari.groupby("weathersit")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(x=weather_effect.index, y=weather_effect.values, palette="coolwarm", ax=ax)
    ax.set_xticklabels(["Clear", "Mist", "Light Snow/Rain", "Heavy Rain/Snow"], rotation=0)
    ax.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
    ax.set_ylabel("Rata-rata Jumlah Penyewa")
    st.pyplot(fig)
