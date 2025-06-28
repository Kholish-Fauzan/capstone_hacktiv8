import streamlit as st
import google.generativeai as genai
import os

# --- Konfigurasi API ---
try:
    # Mengakses API Key langsung dari Streamlit Secrets yang sudah Anda set
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    st.error("Google Gemini API key tidak ditemukan di Streamlit Secrets. Pastikan sudah diatur.")
    st.stop()

# Inisialisasi model Gemini-1.5 Flash
try:
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Gagal menginisialisasi model Gemini-2.5 Flash: {e}")
    st.stop()

# --- Streamlit UI Setup ---
st.set_page_config(layout="wide", page_title="Jelajah Bondowoso AI")

st.title("Jelajah Bondowoso: Kisah Budaya & Promosi Pariwisata Berbasis AI")
st.write("Aplikasi ini bantu Anda merangkai narasi budaya dan promosi pariwisata Bondowoso pakai **Gemini-1.5 Flash AI**.")

# --- Sidebar ---
st.sidebar.header("Tentang Aplikasi Ini")
st.sidebar.write("Manfaatkan Gemini-1.5 Flash untuk bikin cerita dan analisis promosi obyek wisata/budaya Bondowoso.")
st.sidebar.write("---")
st.sidebar.write("Dibuat dengan ❤️")

# --- Input Section ---
st.header("Ceritakan Kekayaan Budaya/Wisata Bondowoso Anda")

col1, col2 = st.columns(2)

with col1:
    judul_objek = st.text_input("Judul/Nama Objek Budaya/Wisata",
                                 placeholder="Contoh: Kopi Bondowoso, Kawah Ijen", help="Nama spesifik obyek.")

with col2:
    gaya_bahasa = st.selectbox("Gaya Bahasa (opsional)",
                                 ["Pilih Gaya", "Edukasi", "Promosi", "Cerita Rakyat", "Puitis", "Informatif", "Inspiratif"],
                                 help="Pilih nuansa narasi.")

deskripsi_kunci = st.text_area("Deskripsi Singkat / Poin-poin Kunci / Fakta Sejarah",
                               height=150,
                               placeholder="Sebutkan detail penting, fragmen cerita, lokasi, tradisi, atau keunikan obyek ini.")

target_audiens = st.text_input("Target Audiens Utama (opsional)",
                                value="", # Kosongkan default agar bisa dikontrol di prompt
                                placeholder="Contoh: Wisatawan Keluarga, Pecinta Sejarah, Penggemar Kopi.")


# --- Tombol Generate ---
if st.button("Generate Kisah & Promosi dengan AI", type="primary"):
    if not judul_objek or not deskripsi_kunci:
        st.warning("Judul Objek dan Deskripsi Kunci wajib diisi ya!")
        st.stop()

    # --- Tahap 1: Generasi Narasi oleh Gemini ---
    with st.spinner("Gemini AI lagi merangkai kisah..."):
        try:
            prompt_narasi = f"""
            Sebagai pencerita ulung dan promotor pariwisata Bondowoso, Jawa Timur, buatlah narasi atau skrip promosi yang menarik berdasarkan detail berikut:

            Nama Objek: {judul_objek}
            Detail Kunci/Fakta: {deskripsi_kunci}
            """
            if target_audiens.strip(): # Hanya tambahkan jika tidak kosong
                prompt_narasi += f"Target Audiens: {target_audiens}\n"
            if gaya_bahasa != "Pilih Gaya": # Hanya tambahkan jika dipilih
                prompt_narasi += f"Gaya Bahasa: {gaya_bahasa}\n"

            prompt_narasi += """
            Hasilkan narasi yang memukau (minimal 250 kata, maksimal 500 kata) yang menyoroti keunikan dan daya tariknya. Fokus pada nuansa Bondowoso.
            """

            response_narasi = gemini_model.generate_content(
                prompt_narasi,
                generation_config={"max_output_tokens": 500, "temperature": 0.7, "top_p": 0.95}
            )
            generated_narration = response_narasi.text
            st.subheader("📝 Kisah & Narasi dari Gemini AI")
            st.markdown(generated_narration)

        except Exception as e:
            st.error(f"Gagal generate narasi: {e}")
            generated_narration = "" # Kosongkan jika ada error

    # --- Tahap 2: Analisis & Optimasi oleh Gemini ---
    if generated_narration: # Lanjutkan hanya jika narasi berhasil digenerate
        st.markdown("---") # Garis pemisah untuk keterbacaan
        with st.spinner("Gemini AI lagi menganalisis & mengoptimasi promosi..."):
            try:
                prompt_analisis = f"""
                Sebagai konsultan pemasaran pariwisata dan pengembang ekonomi lokal Bondowoso, analisis narasi ini untuk wawasan kunci dan saran optimasi:

                Nama Objek: {judul_objek}
                Narasi yang Dihasilkan:
                ---
                {generated_narration}
                ---

                Berikan informasi berikut dengan format daftar (bullet points) atau paragraf terstruktur:
                1.  **Poin Jual Utama:** 3-5 fitur unik terkuat dari narasi.
                2.  **Segmen Wisatawan Ideal:** 2-3 segmen wisatawan spesifik yang tertarik.
                3.  **Ide Monetisasi & Produk:** 2-3 cara konkret menghasilkan nilai ekonomi (misal: tur, produk lokal, event).
                4.  **Saran Peningkatan Promosi:** 2-3 tips/frasa revisi untuk pesan promosi lebih menarik.
                5.  **Potensi Kolaborasi Lokal:** 2-3 jenis bisnis/komunitas lokal Bondowoso yang bisa berkolaborasi.
                """
                response_analisis = gemini_model.generate_content(
                    prompt_analisis,
                    generation_config={"max_output_tokens": 500, "temperature": 0.5, "top_p": 0.9}
                )
                gemini_analysis = response_analisis.text
                st.subheader("💡 Wawasan & Optimasi Promosi dari Gemini AI")
                st.markdown(gemini_analysis)

            except Exception as e:
                st.error(f"Gagal menganalisis promosi: {e}")