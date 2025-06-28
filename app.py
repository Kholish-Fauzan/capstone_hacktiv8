import streamlit as st
import google.generativeai as genai
import os

# --- Konfigurasi API ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    st.error("Google Gemini API key tidak ditemukan di Streamlit Secrets. Pastikan sudah diatur.")
    st.stop()

try:
    # Menggunakan Gemini-1.5 Flash sesuai permintaan
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Gagal menginisialisasi model Gemini-1.5 Flash: {e}")
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
            # === PERHATIAN: Prompt Narasi Ditingkatkan ===
            prompt_narasi = f"""
            Anda adalah seorang pencerita ulung dan promotor pariwisata yang sangat mengenal kekayaan budaya Bondowoso, Jawa Timur.
            Tugas Anda adalah menciptakan sebuah narasi atau skrip promosi yang sangat menarik, detail, dan komprehensif (minimal 300 kata) berdasarkan informasi berikut.
            Pastikan narasi ini cukup panjang dan kaya akan detail deskriptif yang memukau pembaca.

            Nama Objek Budaya/Pariwisata: {judul_objek}
            Poin-Poin Kunci / Fakta Sejarah / Detail Penting: {deskripsi_kunci}
            """
            if target_audiens.strip():
                prompt_narasi += f"Target Audiens Utama: {target_audiens}\n"
            if gaya_bahasa != "Pilih Gaya":
                prompt_narasi += f"Gaya Bahasa yang Diinginkan: {gaya_bahasa}\n"

            prompt_narasi += """
            Hasilkan narasi yang memukau. Kembangkan poin-poin menjadi paragraf yang koheren, tambahkan sentuhan emosional, dan gambarkan pengalaman yang dapat dirasakan pengunjung/pembaca. Pastikan narasi ini mencapai panjang yang substansial, tidak terpotong, dan terasa lengkap.
            """

            # === Perhatikan: max_output_tokens diatur lebih tinggi ===
            response_narasi = gemini_model.generate_content(
                prompt_narasi,
                generation_config={
                    "max_output_tokens": 1000, # Meningkatkan batas token output
                    "temperature": 0.8,        # Sedikit lebih tinggi untuk kreativitas
                    "top_p": 0.95,
                    "top_k": 60
                }
            )
            # Mengatasi potensi error jika response.text tidak langsung tersedia
            if response_narasi.parts:
                generated_narration = response_narasi.text
            else:
                st.warning("Gemini tidak dapat menghasilkan narasi. Mungkin ada batasan respons.")
                generated_narration = ""

            if generated_narration:
                st.subheader("📝 Kisah & Narasi dari Gemini AI")
                st.markdown(generated_narration)
            else:
                st.error("Gagal mendapatkan narasi yang valid dari Gemini.")
                generated_narration = "" # Pastikan kosong jika gagal


        except Exception as e:
            st.error(f"Terjadi kesalahan saat generasi narasi dengan Gemini: {e}")
            generated_narration = "" # Kosongkan jika ada error

    # --- Tahap 2: Analisis & Optimasi oleh Gemini ---
    if generated_narration: # Lanjutkan hanya jika narasi berhasil digenerate
        st.markdown("---") # Garis pemisah untuk keterbacaan
        with st.spinner("Gemini AI lagi menganalisis & mengoptimasi promosi..."):
            try:
                # === PERHATIAN: Prompt Analisis Ditingkatkan ===
                prompt_analisis = f"""
                Sebagai konsultan pemasaran pariwisata dan pengembang ekonomi lokal untuk wilayah seperti Bondowoso, analisis narasi budaya/pariwisata berikut secara mendalam untuk mengekstrak wawasan kunci dan menyarankan optimasi yang konkret dan terperinci untuk dampak ekonomi dan promosi pariwisata.

                Narasi yang Dihasilkan:
                ---
                {generated_narration}
                ---

                Berikan analisis Anda dalam format yang terstruktur dengan sub-judul yang jelas, dan poin-poin yang mudah dibaca:
                1.  **Poin Jual Utama (Key Selling Points):** Identifikasi 3-5 fitur atau daya tarik unik terkuat yang *sudah ada* atau *bisa ditekankan lebih lanjut* dari narasi ini.
                2.  **Segmen Wisatawan Ideal:** Jelaskan 2-3 segmen wisatawan spesifik yang paling mungkin tertarik berdasarkan isi narasi, berikan alasan singkat.
                3.  **Ide Monetisasi & Produk Pariwisata Konkret:** Sarankan 2-3 cara konkret objek ini dapat menghasilkan nilai ekonomi. Contoh: "Paket tur petualangan Blue Fire 3 hari 2 malam dengan akomodasi lokal", "Produk kopi Bondowoso premium yang diintegrasikan ke pengalaman wisata", "Festival budaya tahunan dengan tiket masuk".
                4.  **Saran Peningkatan Pesan Promosi:** Berikan 2-3 tips atau frasa yang direvisi untuk membuat pesan promosi lebih menarik dan persuasif di berbagai media (sosial media, brosur).
                5.  **Potensi Kolaborasi Lokal di Bondowoso:** Sarankan 2-3 jenis bisnis atau komunitas lokal di Bondowoso (misal: pengrajin batik, petani kopi, kelompok seni tari tradisional, pengelola homestay) yang dapat berkolaborasi dengan inisiatif ini untuk meningkatkan daya tarik dan jangkauan ekonomi.
                """
                # === Perhatikan: max_output_tokens diatur lebih tinggi untuk analisis ===
                response_analisis = gemini_model.generate_content(
                    prompt_analisis,
                    generation_config={
                        "max_output_tokens": 700, # Meningkatkan batas token output untuk analisis
                        "temperature": 0.6,        # Agak lebih tinggi dari sebelumnya untuk detail
                        "top_p": 0.9,
                        "top_k": 40
                    }
                )
                if response_analisis.parts:
                    gemini_analysis = response_analisis.text
                else:
                    st.warning("Gemini tidak dapat menghasilkan analisis. Mungkin ada batasan respons.")
                    gemini_analysis = ""

                if gemini_analysis:
                    st.subheader("💡 Wawasan & Optimasi Promosi dari Gemini AI")
                    st.markdown(gemini_analysis)
                else:
                    st.error("Gagal mendapatkan analisis yang valid dari Gemini.")

            except Exception as e:
                st.error(f"Terjadi kesalahan saat analisis promosi dengan Gemini: {e}")

# --- Sidebar Explanation (Moved to a separate section for better organization) ---
st.sidebar.markdown("""
### Bagaimana Aplikasi Ini Bekerja?
1.  **Input Data**: Masukkan nama objek, deskripsi kunci, serta informasi tentang target audiens dan gaya bahasa yang diinginkan di bagian utama.
2.  **Generate Kisah**: Tekan tombol 'Generate Kisah & Promosi dengan AI'. Aplikasi akan memanggil Google Gemini untuk menciptakan narasi awal.
3.  **Analisis & Optimasi**: Setelah narasi dihasilkan, Gemini akan dipanggil lagi untuk menganalisis narasi tersebut dan memberikan wawasan serta saran promosi yang berfokus pada potensi ekonomi lokal.
4.  **Output**: Hasil narasi dan analisis promosi akan terlihat di bagian utama aplikasi.
""")