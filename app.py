import streamlit as st
import google.generativeai as genai
import os
import json # Untuk parsing JSON dari Gemini
import pandas as pd # Untuk menampilkan tabel
from reportlab.lib.pagesizes import letter # Untuk PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io # Untuk membuat file di memori

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

# --- Fungsi Pembantu untuk Generasi PDF ---

def generate_pdf_from_text(text_content, filename_prefix="document"):
    """Menghasilkan PDF dari teks biasa."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()

    # Style untuk paragraf normal
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.leading = 14 # Jarak antar baris

    # Style untuk judul
    title_style = styles['h1']
    title_style.fontSize = 18
    title_style.alignment = 1 # Center

    story = []
    # Tambahkan judul jika ada
    if "judul_objek" in st.session_state and st.session_state.judul_objek:
        story.append(Paragraph(st.session_state.judul_objek, title_style))
        story.append(Spacer(1, 0.2 * inch))

    # Pisahkan teks ke paragraf berdasarkan baris baru ganda
    paragraphs = text_content.split('\n\n')
    for para_text in paragraphs:
        if para_text.strip():
            story.append(Paragraph(para_text.replace('\n', '<br/>'), normal_style))
            story.append(Spacer(1, 0.1 * inch)) # Spasi antar paragraf

    try:
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Gagal membuat PDF narasi: {e}")
        return None

def generate_analysis_pdf(analysis_data, filename_prefix="analysis"):
    """Menghasilkan PDF dari data analisis dalam bentuk tabel."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()

    title_style = styles['h1']
    title_style.fontSize = 18
    title_style.alignment = 1 # Center

    # Style untuk tabel
    table_style_header = ParagraphStyle('TableHeader',
                                        parent=styles['Normal'],
                                        fontName='Helvetica-Bold',
                                        fontSize=10,
                                        alignment=1, # Center
                                        backColor=colors.HexColor('#F0F2F6')) # Warna latar belakang header Streamlit default

    table_style_cell = ParagraphStyle('TableCell',
                                       parent=styles['Normal'],
                                       fontSize=9)


    story = []
    story.append(Paragraph("Wawasan & Optimasi Promosi dari Gemini AI", title_style))
    story.append(Spacer(1, 0.2 * inch))

    if analysis_data:
        # Siapkan data untuk tabel
        table_headers = ["Fitur Analisis", "Wawasan/Saran"]
        table_data = [table_headers]

        # Mapping kunci ke nama yang lebih rapi untuk tampilan
        key_mapping = {
            "Poin Jual Utama": "Poin Jual Utama",
            "Segmen Wisatawan Ideal": "Segmen Wisatawan Ideal",
            "Ide Monetisasi & Produk": "Ide Monetisasi & Produk Pariwisata Konkret",
            "Saran Peningkatan Promosi": "Saran Peningkatan Pesan Promosi",
            "Potensi Kolaborasi Lokal": "Potensi Kolaborasi Lokal"
        }

        for key, display_name in key_mapping.items():
            value = analysis_data.get(key, "N/A")
            if isinstance(value, list):
                # Ubah list menjadi string berpoin untuk cell tabel
                formatted_value = "<br/>".join([f"• {item}" for item in value])
            else:
                formatted_value = str(value)
            table_data.append([Paragraph(display_name, table_style_header), Paragraph(formatted_value, table_style_cell)])

        table = Table(table_data, colWidths=[2*inch, 4.5*inch]) # Lebar kolom
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F0F2F6')), # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#31333F')), # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BOX', (0,0), (-1,-1), 1, colors.black),
        ]))
        story.append(table)
    else:
        story.append(Paragraph("Tidak ada data analisis yang valid untuk ditampilkan.", styles['Normal']))

    try:
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Gagal membuat PDF analisis: {e}")
        return None


# --- Streamlit UI Setup ---
st.set_page_config(layout="wide", page_title="Jelajah Kisah & Potensi Lokal Berbasis AI")

st.title("Jelajah Kisah: Pengenalan Budaya & Pariwisata Lokal Berbasis AI")
st.markdown("Aplikasi ini bantu Anda merangkai narasi budaya dan promosi pariwisata di lokasi Anda menggunakan **Gemini-2.5 Flash**.")
st.markdown("---") # Garis pemisah visual

# --- Sidebar ---
st.sidebar.header("Tentang Aplikasi Ini")
st.sidebar.info("Memanfaatkan Gemini-2.5 Flash untuk bikin cerita dan analisis promosi obyek wisata/budaya lokal.")
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

    # Simpan input ke session_state agar bisa diakses oleh tombol download
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
        try:
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
                    "max_output_tokens": 2000, # Batas token lebih tinggi
                    "temperature": 0.6,
                    "top_p": 0.9,
                    "top_k": 50
                }
            )

            if response_narasi.parts:
                generated_narration = response_narasi.text
                narasi_placeholder.markdown(generated_narration)
                st.session_state.generated_narration = generated_narration # Simpan ke session state

                pdf_bytes = generate_pdf_from_text(generated_narration, f"Narasi_{judul_objek}")
                if pdf_bytes:
                    download_narasi_placeholder.download_button(
                        label="Unduh Naskah Cerita (PDF)",
                        data=pdf_bytes,
                        file_name=f"Kisah_{judul_objek}.pdf",
                        mime="application/pdf",
                        help="Unduh naskah cerita yang dihasilkan AI sebagai file PDF."
                    )
            elif response_narasi.candidates and response_narasi.candidates[0].finish_reason:
                narasi_placeholder.warning(f"Gemini tidak dapat menghasilkan narasi. Finish reason: {response_narasi.candidates[0].finish_reason.name}. Coba sesuaikan prompt atau input.")
                st.session_state.generated_narration = ""
            else:
                narasi_placeholder.warning("Gemini tidak dapat menghasilkan narasi. Respons kosong atau tidak terduga. Coba sesuaikan prompt atau input.")
                st.session_state.generated_narration = ""

        except Exception as e:
            st.error(f"Terjadi kesalahan saat generasi narasi dengan Gemini: {e}. Coba periksa prompt dan input.")
            st.session_state.generated_narration = ""

    # --- Tahap 2: Analisis & Optimasi oleh Gemini ---
    if st.session_state.generated_narration: # Lanjutkan hanya jika narasi berhasil digenerate
        st.markdown("---")
        st.subheader("💡 Wawasan & Optimasi Promosi dari Gemini AI")
        analisis_placeholder = st.empty()
        download_analisis_placeholder = st.empty()

        with st.spinner("Saya sedang menganalisis & mengoptimasi promosi..."):
            try:
                # === Prompt Analisis dengan Permintaan JSON ===
                # Penting: Menginstruksikan format JSON dengan kunci spesifik
                prompt_analisis = f"""
                Anda adalah seorang konsultan pemasaran pariwisata dan pengembang ekonomi lokal untuk wilayah {lokasi_objek}.
                Analisis narasi budaya/pariwisata berikut secara mendalam untuk mengekstrak wawasan kunci dan menyarankan optimasi yang konkret dan terperinci untuk dampak ekonomi dan promosi pariwisata.

                Berikan respons Anda dalam format JSON. Objek JSON harus memiliki 5 kunci berikut, dengan nilai berupa array string atau string singkat dan padat:
                - "Poin Jual Utama" (3-5 poin unik)
                - "Segmen Wisatawan Ideal" (2-3 segmen dengan alasan singkat)
                - "Ide Monetisasi & Produk Pariwisata" (2-3 ide konkret, misal: "Paket Wisata A", "Produk Souvenir B")
                - "Saran Peningkatan Pesan Promosi" (2-3 saran singkat atau frasa kunci)
                - "Potensi Kolaborasi Lokal" (2-3 jenis bisnis/komunitas lokal yang relevan dengan {lokasi_objek})

                Narasi yang Dihasilkan:
                ---
                {st.session_state.generated_narration}
                ---
                """
                
                response_analisis = gemini_model.generate_content(
                    prompt_analisis,
                    generation_config={
                        "max_output_tokens": 1000, # Cukup 1000 untuk JSON singkat
                        "temperature": 0.5, # Lebih rendah untuk objektivitas
                        "response_mime_type": "application/json", # Minta respons dalam JSON
                        "response_schema": { # Definisi skema JSON yang diharapkan
                            "type": "OBJECT",
                            "properties": {
                                "Poin Jual Utama": { "type": "ARRAY", "items": { "type": "STRING" } },
                                "Segmen Wisatawan Ideal": { "type": "ARRAY", "items": { "type": "STRING" } },
                                "Ide Monetisasi & Produk Pariwisata": { "type": "ARRAY", "items": { "type": "STRING" } },
                                "Saran Peningkatan Pesan Promosi": { "type": "ARRAY", "items": { "type": "STRING" } },
                                "Potensi Kolaborasi Lokal": { "type": "ARRAY", "items": { "type": "STRING" } }
                            },
                            "required": [
                                "Poin Jual Utama",
                                "Segmen Wisatawan Ideal",
                                "Ide Monetisasi & Produk Pariwisata",
                                "Saran Peningkatan Pesan Promosi",
                                "Potensi Kolaborasi Lokal"
                            ]
                        }
                    }
                )

                gemini_analysis_raw_text = ""
                if response_analisis.parts:
                    gemini_analysis_raw_text = response_analisis.text
                elif response_analisis.candidates and response_analisis.candidates[0].finish_reason:
                    analisis_placeholder.warning(f"Gemini tidak dapat menghasilkan analisis. Finish reason: {response_analisis.candidates[0].finish_reason.name}. Coba sesuaikan prompt atau input.")
                else:
                    analisis_placeholder.warning("Gemini tidak dapat menghasilkan analisis. Respons kosong atau tidak terduga. Coba sesuaikan prompt atau input.")


                if gemini_analysis_raw_text:
                    try:
                        # Parsing JSON dari respons
                        analysis_data = json.loads(gemini_analysis_raw_text)
                        
                        # Mengubah data analisis menjadi DataFrame untuk tampilan tabel
                        # Mengubah format untuk st.dataframe
                        table_data = []
                        for key, value in analysis_data.items():
                            if isinstance(value, list):
                                table_data.append({"Fitur Analisis": key, "Wawasan/Saran": "\n- " + "\n- ".join(value)})
                            else:
                                table_data.append({"Fitur Analisis": key, "Wawasan/Saran": value})
                        
                        df_analysis = pd.DataFrame(table_data)
                        analisis_placeholder.dataframe(df_analysis, use_container_width=True, hide_index=True) # Tampilkan tabel

                        st.session_state.analysis_data = analysis_data # Simpan ke session state

                        # Tombol Unduh PDF Analisis
                        pdf_bytes_analysis = generate_analysis_pdf(analysis_data, f"Analisis_{judul_objek}")
                        if pdf_bytes_analysis:
                            download_analisis_placeholder.download_button(
                                label="Unduh Analisis Promosi (PDF)",
                                data=pdf_bytes_analysis,
                                file_name=f"Analisis_Promosi_{judul_objek}.pdf",
                                mime="application/pdf",
                                help="Unduh analisis promosi yang dihasilkan AI sebagai file PDF."
                            )

                    except json.JSONDecodeError as json_err:
                        analisis_placeholder.error(f"Gagal memparsing respons JSON dari Gemini: {json_err}. Respons mentah:\n```json\n{gemini_analysis_raw_text}\n```")
                    except Exception as parse_err:
                        analisis_placeholder.error(f"Terjadi kesalahan saat memproses analisis: {parse_err}. Respons mentah:\n{gemini_analysis_raw_text}")
                else:
                    st.error("Gagal mendapatkan analisis yang valid dari Gemini.")

            except Exception as e:
                st.error(f"Terjadi kesalahan saat analisis promosi dengan Gemini: {e}. Coba periksa prompt dan input.")

# --- Sidebar Explanation (Moved to a separate section for better organization) ---
st.sidebar.markdown("""
### Bagaimana Aplikasi Ini Bekerja?
1.  **Input Data**: Masukkan nama objek, **lokasi objek**, deskripsi kunci, serta informasi tentang target audiens dan gaya bahasa yang diinginkan di bagian utama.
2.  **Generate Kisah**: Tekan tombol 'Generate Kisah & Promosi Wisata'. Aplikasi akan memanggil Google Gemini untuk menciptakan narasi awal.
3.  **Analisis & Optimasi**: Setelah narasi dihasilkan, Gemini akan dipanggil lagi untuk menganalisis narasi tersebut dan memberikan wawasan serta saran promosi yang berfokus pada potensi ekonomi lokal.
4.  **Output**: Hasil narasi dan analisis promosi akan terlihat di bagian utama aplikasi.
""")