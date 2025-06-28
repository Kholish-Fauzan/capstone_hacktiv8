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
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Gagal menginisialisasi model Gemini-2.5 Flash: {e}")
    st.stop()

# --- Streamlit UI Setup ---
st.set_page_config(layout="wide", page_title="Jelajah Kisah & Potensi Lokal Berbasis AI")

st.title("Jelajah Kisah: Pengenalan Budaya & Pariwisata Lokal Berbasis AI")
st.write("Aplikasi ini bantu Anda merangkai narasi budaya dan promosi pariwisata di lokasi Anda menggunakan **Gemini-2.5 Flash**.")

# --- Sidebar ---
st.sidebar.header("Tentang Aplikasi Ini")
st.sidebar.write("Memanfaatkan Gemini-2.5 Flash untuk bikin cerita dan analisis promosi obyek wisata/budaya lokal.")
st.sidebar.write("---")
st.sidebar.write("Dibuat oleh Kholish Fauzan")

# --- Input Section ---
st.header("Ceritakan Kekayaan Budaya/Wisata Lokal Anda")

col1, col2 = st.columns(2)

with col1:
    judul_objek = st.text_input("Judul/Nama Objek Budaya/Wisata",
                                 placeholder="Contoh: Kopi Gayo, Tari Saman", help="Nama spesifik obyek.")
    # --- BARU: Input Lokasi ---
    lokasi_objek = st.text_input("Lokasi Obyek (Kota/Kabupaten/Provinsi)",
                                 placeholder="Contoh: Aceh Tengah, Sumatra Utara, Bondowoso", help="Lokasi geografis obyek.")


with col2:
    gaya_bahasa = st.selectbox("Gaya Bahasa (opsional)",
                                 ["Pilih Gaya", "Edukasi", "Promosi", "Cerita Rakyat", "Puitis", "Informatif", "Inspiratif"],
                                 help="Pilih nuansa narasi.")

target_audiens = st.text_input("Target Audiens Utama (opsional)",
                                value="",
                                placeholder="Contoh: Wisatawan Keluarga, Pecinta Sejarah, Penggemar Kopi, dll.")

deskripsi_kunci = st.text_area("Deskripsi Singkat / Poin-poin Kunci / Fakta Sejarah",
                               height=150,
                               placeholder="Sebutkan detail penting, fragmen cerita, lokasi, tradisi, atau keunikan obyek ini.")


# --- Tombol Generate ---
if st.button("Generate Kisah & Promosi Wisata", type="primary"):
    if not judul_objek or not deskripsi_kunci or not lokasi_objek: # Validasi Lokasi
        st.warning("Judul Objek, Lokasi Obyek, dan Deskripsi Kunci wajib diisi ya!")
        st.stop()

    # --- Tahap 1: Generasi Narasi oleh Gemini ---
    with st.spinner("Saya sedang merangkai kisahnya..."):
        try:
            # === Prompt Narasi Disesuaikan untuk Lokasi ===
            prompt_narasi = f"""
            Anda adalah seorang pencerita ulung dan promotor pariwisata yang sangat mengenal kekayaan budaya dan pariwisata di {lokasi_objek}, Indonesia.
            Buatlah narasi atau skrip promosi yang sangat menarik dan detail (setidaknya beberapa paragraf, sekitar 300-500 kata) berdasarkan informasi berikut:

            Nama Objek Budaya/Pariwisata: {judul_objek}
            Poin-Poin Kunci / Fakta Sejarah / Detail Penting: {deskripsi_kunci}
            """
            if target_audiens.strip():
                prompt_narasi += f"Target Audiens Utama: {target_audiens}\n"
            if gaya_bahasa != "Pilih Gaya":
                prompt_narasi += f"Gaya Bahasa yang Diinginkan: {gaya_bahasa}\n"

            prompt_narasi += """
            Kembangkan poin-poin ini menjadi narasi yang koheren dan deskriptif. Tambahkan sentuhan emosional dan gambarkan pengalaman yang dapat dirasakan pengunjung/pembaca. Pastikan narasi ini mengalir dengan baik dan terasa lengkap.
            """

            response_narasi = gemini_model.generate_content(
                prompt_narasi,
                generation_config={
                    "max_output_tokens": 1200,
                    "temperature": 0.6,
                    "top_p": 0.9,
                    "top_k": 50
                }
            )

            if response_narasi.parts:
                generated_narration = response_narasi.text
            elif response_narasi.candidates and response_narasi.candidates[0].finish_reason:
                st.warning(f"Gemini tidak dapat menghasilkan narasi. Finish reason: {response_narasi.candidates[0].finish_reason.name}. Coba sesuaikan prompt atau input.")
                generated_narration = ""
            else:
                st.warning("Gemini tidak dapat menghasilkan narasi. Respons kosong atau tidak terduga. Coba sesuaikan prompt atau input.")
                generated_narration = ""

            if generated_narration:
                st.subheader("📝 Kisah & Narasi dari Gemini AI")
                st.markdown(generated_narration)
            else:
                st.error("Gagal mendapatkan narasi yang valid dari Gemini.")


        except Exception as e:
            st.error(f"Terjadi kesalahan saat generasi narasi dengan Gemini: {e}. Coba periksa prompt dan input.")
            generated_narration = ""

    # --- Tahap 2: Analisis & Optimasi oleh Gemini ---
    if generated_narration:
        st.markdown("---")
        with st.spinner("Saya sedang menganalisis & mengoptimasi promosi..."):
            try:
                # === Prompt Analisis Disesuaikan dengan Lokasi Baru ===
                prompt_analisis = f"""
                Sebagai konsultan pemasaran pariwisata dan pengembang ekonomi lokal untuk wilayah {lokasi_objek}, analisis narasi budaya/pariwisata berikut secara mendalam untuk mengekstrak wawasan kunci dan menyarankan optimasi yang konkret dan terperinci untuk dampak ekonomi dan promosi pariwisata.

                Narasi yang Dihasilkan:
                ---
                {generated_narration}
                ---

                Berikan analisis Anda dalam format yang terstruktur dengan sub-judul yang jelas, dan poin-poin yang mudah dibaca:
                1.  **Poin Jual Utama (Key Selling Points):** Identifikasi 3-5 fitur atau daya tarik unik terkuat yang *sudah ada* atau *bisa ditekankan lebih lanjut* dari narasi ini.
                2.  **Segmen Wisatawan Ideal:** Jelaskan 2-3 segmen wisatawan spesifik yang paling mungkin tertarik berdasarkan isi narasi, berikan alasan singkat.
                3.  **Ide Monetisasi & Produk Pariwisata Konkret:** Sarankan 2-3 cara konkret objek ini dapat menghasilkan nilai ekonomi. Contoh: "Paket tur petualangan Blue Fire 3 hari 2 malam dengan akomodasi lokal", "Produk kopi premium yang diintegrasikan ke pengalaman wisata", "Festival budaya tahunan dengan tiket masuk".
                4.  **Saran Peningkatan Pesan Promosi:** Berikan 2-3 tips atau frasa yang direvisi untuk membuat pesan promosi lebih menarik dan persuasif di berbagai media (sosial media, brosur).
                5.  **Potensi Kolaborasi Lokal di {lokasi_objek}:** Sarankan 2-3 jenis bisnis atau komunitas lokal (misal: pengrajin batik, petani kopi, kelompok seni tari tradisional, pengelola homestay) di {lokasi_objek} yang dapat berkolaborasi dengan inisiatif ini untuk meningkatkan daya tarik dan jangkauan ekonomi.
                """
                response_analisis = gemini_model.generate_content(
                    prompt_analisis,
                    generation_config={
                        "max_output_tokens": 1000,
                        "temperature": 0.6,
                        "top_p": 0.9,
                        "top_k": 40
                    }
                )
                if response_analisis.parts:
                    gemini_analysis = response_analisis.text
                elif response_analisis.candidates and response_analisis.candidates[0].finish_reason:
                    st.warning(f"Gemini tidak dapat menghasilkan analisis. Finish reason: {response_analisis.candidates[0].finish_reason.name}. Coba sesuaikan prompt atau input.")
                    gemini_analysis = ""
                else:
                    st.warning("Gemini tidak dapat menghasilkan analisis. Respons kosong atau tidak terduga. Coba sesuaikan prompt atau input.")
                    gemini_analysis = ""


                if gemini_analysis:
                    st.subheader("💡 Wawasan & Optimasi Promosi dari Gemini AI")
                    st.markdown(gemini_analysis)
                else:
                    st.error("Gagal mendapatkan analisis yang valid dari Gemini.")

            except Exception as e:
                st.error(f"Terjadi kesalahan saat analisis promosi dengan Gemini: {e}. Coba periksa prompt dan input.")

# --- Sidebar Explanation ---
st.sidebar.markdown("""
### Bagaimana Aplikasi Ini Bekerja?
1.  **Input Data**: Masukkan nama objek, **lokasi objek**, deskripsi kunci, serta informasi tentang target audiens dan gaya bahasa yang diinginkan di bagian utama.
2.  **Generate Kisah**: Tekan tombol 'Generate Kisah & Promosi Wisata'. Aplikasi akan memanggil Google Gemini untuk menciptakan narasi awal.
3.  **Analisis & Optimasi**: Setelah narasi dihasilkan, Gemini akan dipanggil lagi untuk menganalisis narasi tersebut dan memberikan wawasan serta saran promosi yang berfokus pada potensi ekonomi lokal.
4.  **Output**: Hasil narasi dan analisis promosi akan terlihat di bagian utama aplikasi.
""")