import streamlit as st
import json
import pandas as pd
from datetime import datetime

# Import dari file konfigurasi
from config import GOOGLE_API_KEY, get_gemini_model

# Import fungsi-fungsi utilitas
from utils.pdf_utils import generate_pdf_from_text, generate_analysis_pdf
from utils.gemini_utils import generate_narrative, generate_analysis_data
from utils.sidebar_content import render_custom_sidebar_content, render_sidebar_expander_content

# --- Konfigurasi API dan Model ---
try:
    gemini_model = get_gemini_model()
except Exception as e:
    st.error(f"Maaf, kami mengalami masalah teknis. Silakan coba lagi nanti atau hubungi pengembang.")
    st.stop()

# --- Streamlit UI Setup (Hanya di app.py) ---
st.set_page_config(
    page_title="Beranda Utama",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Custom CSS (Hanya di app.py yang pertama kali memuatnya, tapi akan dimuat ulang di setiap halaman `pages/` juga) ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('assets/style.css')

# --- Inisialisasi Session State di Awal Skrip ---
# Ini sangat penting agar variabel tidak hilang saat rerun
if 'generated_narration' not in st.session_state:
    st.session_state.generated_narration = ""
if 'generated_analysis' not in st.session_state:
    st.session_state.generated_analysis = {} # Gunakan dictionary kosong jika hasilnya JSON
if 'narasi_pdf_bytes' not in st.session_state:
    st.session_state.narasi_pdf_bytes = None
if 'analisis_pdf_bytes' not in st.session_state:
    st.session_state.analisis_pdf_bytes = None
if 'narasi_file_name' not in st.session_state:
    st.session_state.narasi_file_name = ""
if 'analisis_file_name' not in st.session_state:
    st.session_state.analisis_file_name = ""


# --- Sidebar ---
with st.sidebar:
    st.header("Nusantara Story")
    render_custom_sidebar_content()
    render_sidebar_expander_content()

# --- Main Content for app.py (Homepage) ---
st.title("Nusantara Story: Menggali Kisah Budaya, Memicu Potensi Wisata 🗺️")
st.markdown("Jelajahi potensi tak terbatas budaya dan pariwisata lokal Anda. Aplikasi ini dirancang untuk membantu Anda merangkai **narasi yang memikat** dan **strategi promosi cerdas**, didukung oleh kecerdasan buatan **Gemini-2.5 Flash** dan **IBM Granite**.")
st.markdown("---")

# Menggunakan st.form untuk input agar tidak langsung rerun saat input berubah
with st.form("story_generation_form"):
    col_input1, col_input2 = st.columns(2)

    with col_input1:
        st.markdown('<p style="font-weight: 600; color: #555555; margin-bottom: 5px;">Nama Objek Budaya/Wisata <span style="color:red">*</span></p>', unsafe_allow_html=True)
        judul_objek = st.text_input("", placeholder="Contoh: Kopi Gayo, Tari Saman, Candi Prambanan", key="input_judul", label_visibility="collapsed")
        st.markdown('<p class="custom-help-text">Nama spesifik objek yang ingin Anda ceritakan atau promosikan.</p>', unsafe_allow_html=True)

        st.markdown('<p style="font-weight: 600; color: #555555; margin-bottom: 5px;">Lokasi Obyek (Kota/Kabupaten/Provinsi) <span style="color:red">*</span></p>', unsafe_allow_html=True)
        lokasi_objek = st.text_input("", placeholder="Contoh: Aceh Tengah, Sumatra Utara, Bondowoso", key="input_lokasi", label_visibility="collapsed")
        st.markdown('<p class="custom-help-text">Lokasi geografis di mana objek ini berada.</p>', unsafe_allow_html=True)


    with col_input2:
        st.markdown('<p style="font-weight: 600; color: #555555; margin-bottom: 5px;">Pilih Gaya Bahasa Narasi (Opsional)</p>', unsafe_allow_html=True)
        gaya_bahasa = st.selectbox("", ["Pilih Gaya", "Edukasi", "Promosi", "Cerita Rakyat", "Puitis", "Informatif", "Inspiratif"], key="select_gaya", label_visibility="collapsed")
        st.markdown('<p class="custom-help-text">Pilih nuansa dan gaya penulisan yang Anda inginkan untuk narasi.</p>', unsafe_allow_html=True)

        st.markdown('<p style="font-weight: 600; color: #555555; margin-bottom: 5px;">Target Audiens Utama (Opsional)</p>', unsafe_allow_html=True)
        target_audiens = st.text_input("", value="", placeholder="Contoh: Wisatawan Keluarga, Pecinta Sejarah, Penggemar Kopi", key="input_target", label_visibility="collapsed")
        st.markdown('<p class="custom-help-text">Siapa target utama pesan promosi ini? (Misal: anak muda, keluarga, turis asing).</p>', unsafe_allow_html=True)

    st.markdown('<p style="font-weight: 600; color: #555555; margin-bottom: 5px;">Deskripsi Singkat / Poin-poin Kunci / Fakta Sejarah <span style="color:red">*</span></p>', unsafe_allow_html=True)
    deskripsi_kunci = st.text_area("", height=150,
                                    placeholder="Sebutkan detail penting, fragmen cerita, lokasi, tradisi, keunikan, atau fakta sejarah obyek ini. Semakin detail dan spesifik, semakin baik hasil yang akan AI berikan!",
                                    key="input_deskripsi", label_visibility="collapsed")
    st.markdown('<p class="custom-help-text">Ini adalah informasi inti untuk Kami merangkai cerita. Beri detail sebanyak mungkin!</p>', unsafe_allow_html=True)


    # --- Tombol Generate di dalam form ---
    submit_button = st.form_submit_button("Mulai Rangkai Kisah & Optimalkan Promosi! ✨", type="primary")

# --- Logika Setelah Tombol Submit Ditekan (di luar form agar bisa mengakses st.session_state) ---
if submit_button:
    if not judul_objek or not deskripsi_kunci or not lokasi_objek:
        st.warning("Mohon lengkapi semua kolom yang bertanda '*' (Wajib diisi) sebelum melanjutkan! 🙏")
        # Kosongkan session state jika input tidak valid agar output sebelumnya tidak muncul
        st.session_state.generated_narration = ""
        st.session_state.generated_analysis = {}
        st.session_state.narasi_pdf_bytes = None
        st.session_state.analisis_pdf_bytes = None
        st.session_state.narasi_file_name = ""
        st.session_state.analisis_file_name = ""
    else:
        # Hapus hasil sebelumnya dari session state untuk memastikan hasil baru
        st.session_state.generated_narration = ""
        st.session_state.generated_analysis = {}
        st.session_state.narasi_pdf_bytes = None
        st.session_state.analisis_pdf_bytes = None
        st.session_state.narasi_file_name = ""
        st.session_state.analisis_file_name = ""

        # --- Tahap 1: Generasi Narasi oleh Gemini ---
        st.subheader("📝 Kisah & Narasi")
        narasi_placeholder = st.empty()

        with st.spinner("Kami sedang menyusun narasi memukau untuk Anda... Sabar ya! ⏳"):
            generated_narration = generate_narrative(
                gemini_model, judul_objek, lokasi_objek, deskripsi_kunci, target_audiens, gaya_bahasa
            )

            if generated_narration:
                narasi_placeholder.markdown(f"<div class='output-card'><p>{generated_narration}</p></div>", unsafe_allow_html=True)
                st.session_state.generated_narration = generated_naration # Simpan ke session state

                # Generate PDF bytes dan simpan juga ke session state
                pdf_bytes_narasi_temp = generate_pdf_from_text(generated_narration, f"Narasi_{judul_objek}")
                if pdf_bytes_narasi_temp:
                    st.session_state.narasi_pdf_bytes = pdf_bytes_narasi_temp
                    st.session_state.narasi_file_name = f"Kisah_{judul_objek}.pdf"
                else:
                    st.error("Gagal membuat PDF Narasi.")
                    st.session_state.narasi_pdf_bytes = None
                    st.session_state.narasi_file_name = ""

            else:
                narasi_placeholder.error("Maaf, Kami gagal merangkai narasi yang valid. Coba ulangi atau sesuaikan input Anda.")
                st.session_state.generated_narration = "" # Kosongkan jika gagal

        # --- Tahap 2: Analisis & Optimasi oleh Gemini ---
        if st.session_state.generated_narration: # Pastikan narasi sudah ada sebelum analisis (ambil dari session state)
            st.markdown("---")
            st.subheader("💡 Wawasan & Optimasi Promosi Wisata")
            
            with st.spinner("Kami sedang menganalisis potensi tak terbatas destinasi Anda... Mohon tunggu! 🚀"):
                analysis_data = generate_analysis_data(gemini_model, lokasi_objek, st.session_state.generated_narration)

                if analysis_data:
                    st.session_state.generated_analysis = analysis_data # Simpan ke session state

                    col_analysis1, col_analysis2 = st.columns(2)

                    # Definisi kunci untuk setiap kolom
                    col1_keys = [
                        "Poin Jual Utama",
                        "Segmen Wisatawan Ideal",
                        "Ide Monetisasi & Produk Pariwisata"
                    ]
                    col2_keys = [
                        "Saran Peningkatan Pesan Promosi",
                        "Potensi Kolaborasi Lokal"
                    ]

                    # Render kolom 1
                    with col_analysis1:
                        for key in col1_keys:
                            if key in analysis_data and analysis_data[key]:
                                st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
                                st.markdown(f"<h4>{key}</h4>", unsafe_allow_html=True)

                                for item in analysis_data[key]:
                                    if 'poin' in item:
                                        st.markdown(f"**👉 {item['poin']}**", unsafe_allow_html=True)
                                    if 'deskripsi' in item:
                                        st.write(item['deskripsi'])
                                st.markdown('</div>', unsafe_allow_html=True)

                    # Render kolom 2
                    with col_analysis2:
                        for key in col2_keys:
                            if key in analysis_data and analysis_data[key]:
                                st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
                                st.markdown(f"<h4>{key}</h4>", unsafe_allow_html=True)

                                for item in analysis_data[key]:
                                    if 'poin' in item:
                                        st.markdown(f"**👉 {item['poin']}**", unsafe_allow_html=True)
                                    if 'deskripsi' in item:
                                        st.write(item['deskripsi'])
                                st.markdown('</div>', unsafe_allow_html=True)

                    # Generate PDF bytes untuk analisis dan simpan juga ke session state
                    pdf_bytes_analysis_temp = generate_analysis_pdf(analysis_data, f"Analisis_{judul_objek}")
                    if pdf_bytes_analysis_temp:
                        st.session_state.analisis_pdf_bytes = pdf_bytes_analysis_temp
                        st.session_state.analisis_file_name = f"Analisis_Promosi_{judul_objek}.pdf"
                    else:
                        st.error("Gagal membuat PDF Analisis Promosi.")
                        st.session_state.analisis_pdf_bytes = None
                        st.session_state.analisis_file_name = ""

                else:
                    st.error("Maaf, Kami gagal mendapatkan analisis yang valid. Coba ulangi atau sesuaikan input Anda.")
                    st.session_state.generated_analysis = {} # Kosongkan jika gagal
        else:
            st.warning("Analisis tidak dapat dilakukan karena narasi belum berhasil dibuat.")

# --- Tampilkan Hasil dan Tombol Unduh (di luar blok `if submit_button`) ---
# Ini agar hasil dan tombol tetap terlihat setelah rerun (misalnya, setelah download)

# Tampilkan narasi hanya jika ada di session state
if st.session_state.generated_narration:
    st.subheader("📝 Kisah & Narasi") # Subheader ini akan muncul ulang
    st.markdown(f"<div class='output-card'><p>{st.session_state.generated_narration}</p></div>", unsafe_allow_html=True)

    # Tombol Unduh Narasi PDF
    if st.session_state.narasi_pdf_bytes:
        st.download_button(
            label="Unduh Naskah Cerita (PDF) ⬇️",
            data=st.session_state.narasi_pdf_bytes,
            file_name=st.session_state.narasi_file_name,
            mime="application/pdf",
            key="download_narasi_pdf_final", # Key unik
            help="Unduh naskah cerita sebagai file PDF. Siap untuk dibagikan!"
        )

# Tampilkan analisis hanya jika ada di session state
if st.session_state.generated_analysis:
    st.markdown("---") # Garis pemisah akan muncul ulang
    st.subheader("💡 Wawasan & Optimasi Promosi Wisata") # Subheader ini akan muncul ulang
    
    # Render ulang analisis di kolom
    col_analysis1_rerun, col_analysis2_rerun = st.columns(2)
    col1_keys_rerun = [
        "Poin Jual Utama",
        "Segmen Wisatawan Ideal",
        "Ide Monetisasi & Produk Pariwisata"
    ]
    col2_keys_rerun = [
        "Saran Peningkatan Pesan Promosi",
        "Potensi Kolaborasi Lokal"
    ]

    with col_analysis1_rerun:
        for key in col1_keys_rerun:
            if key in st.session_state.generated_analysis and st.session_state.generated_analysis[key]:
                st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
                st.markdown(f"<h4>{key}</h4>", unsafe_allow_html=True)
                for item in st.session_state.generated_analysis[key]:
                    if 'poin' in item:
                        st.markdown(f"**👉 {item['poin']}**", unsafe_allow_html=True)
                    if 'deskripsi' in item:
                        st.write(item['deskripsi'])
                st.markdown('</div>', unsafe_allow_html=True)
    
    with col_analysis2_rerun:
        for key in col2_keys_rerun:
            if key in st.session_state.generated_analysis and st.session_state.generated_analysis[key]:
                st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
                st.markdown(f"<h4>{key}</h4>", unsafe_allow_html=True)
                for item in st.session_state.generated_analysis[key]:
                    if 'poin' in item:
                        st.markdown(f"**👉 {item['poin']}**", unsafe_allow_html=True)
                    if 'deskripsi' in item:
                        st.write(item['deskripsi'])
                st.markdown('</div>', unsafe_allow_html=True)

    # Tombol Unduh Analisis Promosi PDF
    if st.session_state.analisis_pdf_bytes:
        st.download_button(
            label="Unduh Analisis Promosi (PDF) ⬇️",
            data=st.session_state.analisis_pdf_bytes,
            file_name=st.session_state.analisis_file_name,
            mime="application/pdf",
            key="download_analysis_pdf_final", # Key unik
            help="Dapatkan dokumen analisis lengkap untuk panduan promosi Anda!"
        )


# --- Footer Copyright ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #777;'>© {datetime.now().year} Nusantara Story. Dibuat dengan ✨ oleh Kholish Fauzan.</p>", unsafe_allow_html=True)