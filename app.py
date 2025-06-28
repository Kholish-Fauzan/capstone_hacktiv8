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

# --- Konfigurasi API dan Model ---
try:
    gemini_model = get_gemini_model()
except Exception as e:
    st.error(f"Gagal menginisialisasi model Gemini: {e}")
    st.stop()

# --- Streamlit UI Setup ---
st.set_page_config(layout="wide", page_title="Nusantara Story AI - Eksplorasi Budaya & Wisata Lokal")

# --- Load Custom CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('assets/style.css')

st.title("Nusantara Story AI: Kisah Budaya & Potensi Wisata Lokal")
st.markdown("Aplikasi ini bantu Anda merangkai narasi budaya dan promosi pariwisata di lokasi Anda menggunakan **Gemini-2.5 Flash**.")
st.markdown("---")

# --- Sidebar ---
st.sidebar.header("Tentang Aplikasi Ini")
st.sidebar.markdown("""
### Bagaimana Aplikasi Ini Bekerja? 🚀
1.  **Input Data**: Isi detail objek budaya/wisata Anda (nama, lokasi, deskripsi kunci, target audiens, gaya bahasa).
2.  **Generate Kisah**: Klik tombol 'Generate Kisah & Promosi Wisata' untuk merangkai narasi awal oleh **Gemini AI**. ✨
3.  **Analisis & Optimasi**: Gemini akan menganalisis narasi Anda dan memberikan wawasan promosi serta potensi ekonomi lokal. 📈
4.  **Output**: Lihat hasil narasi dan analisis promosi langsung di aplikasi! 📊
""")
st.sidebar.markdown("---")
st.sidebar.write("Dibuat oleh Kholish Fauzan")
st.sidebar.markdown("---")
st.sidebar.info("Tips: Isi deskripsi dengan detail sebanyak mungkin untuk hasil AI yang lebih baik!")


# --- Input Section ---
st.header("Ceritakan Kekayaan Budaya/Wisata Lokal Anda")

col_input1, col_input2 = st.columns(2)

with col_input1:
    judul_objek = st.text_input("Judul/Nama Objek Budaya/Wisata",
                                 placeholder="Contoh: Kopi Gayo, Tari Saman", help="Nama spesifik obyek.")
    lokasi_objek = st.text_input("Lokasi Obyek (Kota/Kabupaten/Provinsi)",
                                 placeholder="Contoh: Aceh Tengah, Sumatra Utara, Bondowoso", help="Lokasi geografis obyek.")


with col_input2:
    gaya_bahasa = st.selectbox("Gaya Bahasa (opsional)",
                                 ["Pilih Gaya", "Edukasi", "Promosi", "Cerita Rakyat", "Puitis", "Informatif", "Inspiratif"],
                                 help="Pilih nuansa narasi.")

    target_audiens = st.text_input("Target Audiens Utama (opsional)",
                                    value="",
                                    placeholder="Contoh: Wisatawan Keluarga, Pecinta Sejarah, Penggemar Kopi, dll.")

deskripsi_kunci = st.text_area("Deskripsi Singkat / Poin-poin Kunci / Fakta Sejarah",
                               height=150,
                               placeholder="Sebutkan detail penting, fragmen cerita, lokasi, tradisi, atau keunikan obyek ini. Semakin detail, semakin baik.")


# --- Tombol Generate ---
if st.button("Generate Kisah & Promosi Wisata", type="primary"):
    if not judul_objek or not deskripsi_kunci or not lokasi_objek:
        st.warning("Judul Objek, Lokasi Obyek, dan Deskripsi Kunci wajib diisi ya!")
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

    with st.spinner("Saya sedang merangkai kisahnya..."):
        generated_narration = generate_narrative(
            gemini_model, judul_objek, lokasi_objek, deskripsi_kunci, target_audiens, gaya_bahasa
        )

        if generated_narration:
            narasi_placeholder.markdown(generated_narration)
            st.session_state.generated_narration = generated_narration

            pdf_bytes = generate_pdf_from_text(generated_narration, f"Narasi_{judul_objek}")
            if pdf_bytes:
                download_narasi_placeholder.download_button(
                    label="Unduh Naskah Cerita (PDF)",
                    data=pdf_bytes,
                    file_name=f"Kisah_{judul_objek}.pdf",
                    mime="application/pdf",
                    help="Unduh naskah cerita yang dihasilkan AI sebagai file PDF."
                )
        else:
            narasi_placeholder.error("Gagal mendapatkan narasi yang valid dari Gemini.")
            st.session_state.generated_narration = ""

    # --- Tahap 2: Analisis & Optimasi oleh Gemini ---
    if st.session_state.generated_narration:
        st.markdown("---")
        st.subheader("💡 Wawasan & Optimasi Promosi dari Gemini AI")
        analisis_output_container = st.container()
        download_analisis_placeholder = st.empty()

        with st.spinner("Saya sedang menganalisis & mengoptimasi promosi..."):
            analysis_data = generate_analysis_data(gemini_model, lokasi_objek, st.session_state.generated_narration)

            if analysis_data:
                st.session_state.analysis_data = analysis_data

                with analisis_output_container:
                    col_analysis1, col_analysis2 = st.columns(2)

                    col1_keys = [
                        "Poin Jual Utama",
                        "Segmen Wisatawan Ideal",
                        "Ide Monetisasi & Produk Pariwisata"
                    ]

                    col2_keys = [
                        "Saran Peningkatan Pesan Promosi",
                        "Potensi Kolaborasi Lokal"
                    ]

                    # Apply glass-card styling to each analysis section
                    for key in col1_keys:
                        if key in analysis_data:
                            with col_analysis1:
                                # Wrap content in a div with the custom class
                                st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
                                st.subheader(key)
                                for item in analysis_data[key]:
                                    st.markdown(f"**{item['poin']}**")
                                    st.write(item['deskripsi'])
                                st.markdown('</div>', unsafe_allow_html=True)
                                # st.markdown("---") # Removed this here, glass card has its own padding/margin

                    for key in col2_keys:
                        if key in analysis_data:
                            with col_analysis2:
                                # Wrap content in a div with the custom class
                                st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
                                st.subheader(key)
                                for item in analysis_data[key]:
                                    st.markdown(f"**{item['poin']}**")
                                    st.write(item['deskripsi'])
                                st.markdown('</div>', unsafe_allow_html=True)
                                # st.markdown("---") # Removed this here

                pdf_bytes_analysis = generate_analysis_pdf(analysis_data, f"Analisis_{judul_objek}")
                if pdf_bytes_analysis:
                    download_analisis_placeholder.download_button(
                        label="Unduh Analisis Promosi (PDF)",
                        data=pdf_bytes_analysis,
                        file_name=f"Analisis_Promosi_{judul_objek}.pdf",
                        mime="application/pdf",
                        help="Unduh analisis promosi yang dihasilkan AI sebagai file PDF."
                    )

            else:
                st.error("Gagal mendapatkan analisis yang valid dari Gemini.")

# --- Footer Copyright ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: grey;'>© {datetime.now().year} Nusantara Story AI. All rights reserved.</p>", unsafe_allow_html=True)