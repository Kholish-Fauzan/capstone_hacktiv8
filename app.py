# app.py
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
    st.error(f"Maaf, kami mengalami masalah teknis. Gagal menghubungkan ke kecerdasan AI. Silakan coba lagi nanti atau hubungi pengembang.")
    st.stop()

# --- Streamlit UI Setup ---
st.set_page_config(
    page_title="Beranda Utama",
    layout="wide", # Pastikan ini tetap "wide"
    initial_sidebar_state="expanded"
)

# --- Load Custom CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('assets/style.css')

# --- Sidebar ---
with st.sidebar:
    st.header("Nusantara Story AI 🇮🇩")
    render_custom_sidebar_content()
    # render_sidebar_expander_content() # Aktifkan jika ingin menambahkan expander

# --- Main Content for app.py (Homepage) ---
st.title("Nusantara Story AI: Menggali Kisah Budaya, Memicu Potensi Wisata 🗺️")
st.markdown("Jelajahi potensi tak terbatas budaya dan pariwisata lokal Anda. Aplikasi ini dirancang untuk membantu Anda merangkai **narasi yang memikat** dan **strategi promosi cerdas**, didukung oleh kecerdasan buatan **Gemini-2.5 Flash**.")
st.markdown("---")

# --- Input Section ---
st.header("Ceritakan Kekayaan Budaya/Wisata Lokal Anda ✍️")

# Custom HTML/CSS for input fields to control spacing and help text
st.markdown("""
<style>
    .stTextInput, .stSelectbox, .stTextArea {
        margin-bottom: 20px;
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextArea"] label {
        margin-bottom: 5px;
    }
    .stHelpInline {
        display: none;
    }
    .custom-help-text {
        font-size: 0.85rem;
        color: #777777;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    .st-emotion-cache-10q20q p {
        font-weight: 600;
        color: #555555;
    }
</style>
""", unsafe_allow_html=True)

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
st.markdown('<p class="custom-help-text">Ini adalah informasi inti untuk AI merangkai cerita. Beri detail sebanyak mungkin!</p>', unsafe_allow_html=True)


# --- Tombol Generate ---
if st.button("Mulai Rangkai Kisah & Optimalkan Promosi! ✨", type="primary"):
    if not judul_objek or not deskripsi_kunci or not lokasi_objek:
        st.warning("Mohon lengkapi semua kolom yang bertanda '*' (Wajib diisi) sebelum melanjutkan! 🙏")
        st.stop()

    st.session_state.judul_objek = judul_objek
    st.session_state.lokasi_objek = lokasi_objek
    st.session_state.deskripsi_kunci = deskripsi_kunci
    st.session_state.target_audiens = target_audiens
    st.session_state.gaya_bahasa = gaya_bahasa


    # --- Tahap 1: Generasi Narasi oleh Gemini ---
    st.subheader("📝 Kisah & Narasi dari Gemini AI")
    narasi_placeholder = st.empty()
    download_narasi_placeholder = st.empty()

    with st.spinner("AI sedang menyusun narasi memukau untuk Anda... Sabar ya! ⏳"):
        generated_narration = generate_narrative(
            gemini_model, judul_objek, lokasi_objek, deskripsi_kunci, target_audiens, gaya_bahasa
        )

        if generated_narration:
            narasi_placeholder.markdown(f"<div class='output-card'><p>{generated_narration}</p></div>", unsafe_allow_html=True)
            st.session_state.generated_narration = generated_narration

            pdf_bytes = generate_pdf_from_text(generated_narration, f"Narasi_{judul_objek}")
            if pdf_bytes:
                download_narasi_placeholder.download_button(
                    label="Unduh Naskah Cerita (PDF) ⬇️",
                    data=pdf_bytes,
                    file_name=f"Kisah_{judul_objek}.pdf",
                    mime="application/pdf",
                    help="Unduh naskah cerita yang dihasilkan AI sebagai file PDF. Siap untuk dibagikan!"
                )
        else:
            narasi_placeholder.error("Maaf, AI gagal merangkai narasi yang valid. Coba ulangi atau sesuaikan input Anda.")
            st.session_state.generated_narration = ""

    # --- Tahap 2: Analisis & Optimasi oleh Gemini ---
    if generated_narration: # Pastikan narasi sudah ada sebelum analisis
        st.markdown("---")
        st.subheader("💡 Wawasan & Optimasi Promosi dari Gemini AI")
        # --- PERUBAHAN DI SINI UNTUK MENEMPATKAN JUDUL ANALISIS DENGAN BENAR ---
        download_analisis_placeholder = st.empty()

        with st.spinner("AI sedang menganalisis potensi tak terbatas destinasi Anda... Mohon tunggu! 🚀"):
            analysis_data = generate_analysis_data(gemini_model, lokasi_objek, st.session_state.generated_narration)

            if analysis_data:
                st.session_state.analysis_data = analysis_data

                col_analysis1, col_analysis2 = st.columns(2)

                with col_analysis1:
                    st.markdown("<h3>Poin Jual Utama</h3>", unsafe_allow_html=True) # Judul untuk kolom ini
                    col1_keys = [
                        "Poin Jual Utama",
                        "Segmen Wisatawan Ideal",
                        "Ide Monetisasi & Produk Pariwisata"
                    ]
                    for key in col1_keys:
                        if key in analysis_data and analysis_data[key]:
                            st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
                            st.markdown(f"<h4>{key}</h4>", unsafe_allow_html=True)
                            for item in analysis_data[key]:
                                st.markdown(f"**👉 {item['poin']}**")
                                st.write(item['deskripsi'])
                            st.markdown('</div>', unsafe_allow_html=True)

                with col_analysis2:
                    st.markdown("<h3>Saran Peningkatan Pesan Promosi</h3>", unsafe_allow_html=True) # Judul untuk kolom ini
                    col2_keys = [
                        "Saran Peningkatan Pesan Promosi",
                        "Potensi Kolaborasi Lokal"
                    ]
                    for key in col2_keys:
                        if key in analysis_data and analysis_data[key]:
                            st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
                            st.markdown(f"<h4>{key}</h4>", unsafe_allow_html=True)
                            for item in analysis_data[key]:
                                st.markdown(f"**👉 {item['poin']}**")
                                st.write(item['deskripsi'])
                            st.markdown('</div>', unsafe_allow_html=True)

                pdf_bytes_analysis = generate_analysis_pdf(analysis_data, f"Analisis_{judul_objek}")
                if pdf_bytes_analysis:
                    download_analisis_placeholder.download_button(
                        label="Unduh Analisis Promosi (PDF) ⬇️",
                        data=pdf_bytes_analysis,
                        file_name=f"Analisis_Promosi_{judul_objek}.pdf",
                        mime="application/pdf",
                        help="Dapatkan dokumen analisis lengkap untuk panduan promosi Anda!"
                    )

            else:
                st.error("Maaf, AI gagal mendapatkan analisis yang valid. Coba ulangi atau sesuaikan input Anda.")
    else:
        st.warning("Analisis tidak dapat dilakukan karena narasi belum berhasil dibuat.")

# --- Footer Copyright ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #777;'>© {datetime.now().year} Nusantara Story AI. Dibuat dengan ✨ oleh Kholish Fauzan.</p>", unsafe_allow_html=True)