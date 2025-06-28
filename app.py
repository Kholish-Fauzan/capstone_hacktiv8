# app.py
import os
import streamlit as st
import google.generativeai as genai

# Load API key securely from Streamlit secrets
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google Gemini API key not found. Please set the environment variable GOOGLE_API_KEY.")
    st.stop()

# Configure Google Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
try:
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Gagal menginisialisasi model Gemini: {e}")
    st.stop()

# Streamlit UI setup
st.title("Jelajah Bondowoso: Kisah Budaya & Promosi Pariwisata Berbasis AI")
st.write("Aplikasi ini membantu Anda merangkai narasi budaya dan promosi pariwisata Bondowoso dengan bantuan Google Gemini AI. Masukkan detail, dan AI akan mengembangkannya menjadi cerita menarik serta memberikan wawasan promosi yang dioptimalkan.")

st.sidebar.header("Tentang Aplikasi Ini")
st.sidebar.write("Aplikasi ini menggunakan Google Gemini AI untuk menciptakan narasi tentang budaya dan promosi pariwisata di Bondowoso berdasarkan input yang diberikan oleh pengguna.")

# Input section
judul = st.text_input("Judul/Nama Objek")
deskripsi_kunci = st.text_area("Deskripsi Kunci/Fakta")
target_audiens = st.text_input("Target Audiens (opsional)", value="Umum")
gaya_bahasa = st.selectbox("Gaya Bahasa (opsional)", ["Formal", "Informal", "Neutral"])

# Button to trigger AI generation
if st.button("Generate Narrative & Analysis"):
    try:
        # First Gemini Call (Generation)
        prompt_gen = f"Buat sebuah narasi tentang {judul}. Deskripsi kunci: {deskripsi_kunci}. Target audiens: {target_audiens}. Gaya bahasa: {gaya_bahasa}."
        response_gen = genai.generate(prompt=prompt_gen, max_tokens=500, temperature=0.7)
        st.subheader("📝 Kisah & Narasi dari Gemini AI")
        st.write(response_gen.text)

        # Second Gemini Call (Analysis)
        prompt_analy = f"Analisis narasi di atas untuk mencari titik-titik penarik, sektor pelanggan ideal, ide monetisasi, pengembangan pesan promosi, dan potensi kerjasama lokal."
        response_analy = genai.analyze(text=response_gen.text, max_tokens=500, temperature=0.7)
        st.subheader("💡 Wawasan & Optimasi Promosi dari Gemini AI")
        st.write(f"**{response_analy.text}**")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Sidebar explanation
st.sidebar.write("""
### Apa Saja Fungsi Aplikasi Ini?
1. **Input Data**: Masukkan nama objek, deskripsi kunci, serta informasi tentang target audiens dan gaya bahasa yang diinginkan.
2. **Generate**: Tekan tombol 'Generate' untuk mencari narasi dan analisis berdasarkan input Anda.
3. **Output**: Hasil narasi yang dirancang oleh Gemini AI dan analisis promosi akan terlihat di bagian utama aplikasi.
""")