# utils/gemini_utils.py

import streamlit as st
import json
import time
import re # Import the regular expression module

def generate_narrative(model, judul_objek, lokasi_objek, deskripsi_kunci, target_audiens, gaya_bahasa):
    """Menghasilkan narasi menggunakan model Gemini."""
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

        response_narasi = model.generate_content(
            prompt_narasi,
            generation_config={
                "max_output_tokens": 4000,
                "temperature": 0.6,
                "top_p": 0.9,
                "top_k": 50
            }
        )

        if response_narasi.parts:
            return response_narasi.text
        elif response_narasi.candidates and response_narasi.candidates[0].finish_reason:
            st.warning(f"Gemini tidak dapat menghasilkan narasi. Finish reason: {response_narasi.candidates[0].finish_reason.name}. Coba sesuaikan prompt atau input.")
            return ""
        else:
            st.warning("Gemini tidak dapat menghasilkan narasi. Respons kosong atau tidak terduga. Coba sesuaikan prompt atau input.")
            return ""

    except Exception as e:
        st.error(f"Terjadi kesalahan saat generasi narasi dengan Gemini: {e}. Coba periksa prompt dan input.")
        return ""

def generate_analysis_data(model, lokasi_objek, generated_narration, max_retries=3):
    """Menghasilkan data analisis menggunakan model Gemini dengan mekanisme retry dan ekstraksi JSON yang lebih robust."""

    prompt_analisis = f"""
    Anda adalah seorang konsultan pemasaran pariwisata dan pengembang ekonomi lokal untuk wilayah {lokasi_objek}.
    Analisis narasi budaya/pariwisata berikut secara mendalam untuk mengekstrak wawasan kunci dan menyarankan optimasi yang konkret dan terperinci untuk dampak ekonomi dan promosi pariwisata.

    Berikan respons Anda dalam format JSON. Objek JSON harus memiliki 5 kunci utama berikut, di mana setiap kunci memiliki nilai berupa ARRAY OBJEK. Setiap objek dalam array tersebut harus memiliki dua properti: "poin" (nama singkat dari strategi/ide) dan "deskripsi" (penjelasan singkat namun padat tentang strategi tersebut).

    Contoh struktur untuk satu poin:
    {{
      "Poin Jual Utama": [
        {{ "poin": "Pemandangan Kawah Ijen", "deskripsi": "Keunikan kawah dengan api biru dan danau asam belerang, menarik wisatawan petualangan dan fotografi." }}
      ],
      "Segmen Wisatawan Ideal": [
        {{ "poin": "Wisatawan Minat Khusus (Kopi)", "deskripsi": "Mereka mencari pengalaman otentik dan edukatif tentang proses dan cita rasa kopi lokal." }}
      ]
    }}

    Pastikan setiap "deskripsi" cukup informatif sehingga pengguna memahami strategi atau potensi di baliknya, tidak hanya daftar poin.
    Sangat penting: Berikan HANYA objek JSON yang valid. Bungkus seluruh objek JSON Anda di dalam blok kode Markdown seperti ini:
    ```json
    {{
      "key": "value"
    }}
    ```
    Jangan tambahkan teks lain di luar blok kode JSON tersebut.

    Narasi yang Dihasilkan:
    ---
    {generated_narration}
    ---
    """

    for attempt in range(max_retries):
        try:
            response_analisis = model.generate_content(
                prompt_analisis,
                generation_config={
                    "max_output_tokens": 4000,
                    "temperature": 0.4,
                    # response_mime_type dan response_schema DIHAPUS di sini
                }
            )

            gemini_analysis_raw_text = ""
            if response_analisis.parts:
                gemini_analysis_raw_text = response_analisis.text
            elif response_analisis.candidates and response_analisis.candidates[0].finish_reason:
                st.warning(f"Percobaan {attempt + 1}/{max_retries}: Gemini tidak dapat menghasilkan analisis. Finish reason: {response_analisis.candidates[0].finish_reason.name}. Mencoba lagi...")
                time.sleep(1)
                continue
            else:
                st.warning(f"Percobaan {attempt + 1}/{max_retries}: Gemini tidak dapat menghasilkan analisis. Respons kosong atau tidak terduga. Mencoba lagi...")
                time.sleep(1)
                continue

            # --- Ekstraksi JSON dari teks mentah ---
            # Cari blok kode JSON yang dibungkus dengan ```json ... ```
            json_match = re.search(r"```json\s*(\{.*\})\s*```", gemini_analysis_raw_text, re.DOTALL)

            if json_match:
                json_string = json_match.group(1) # Ambil konten di dalam blok json
                return json.loads(json_string) # Coba parse JSON yang sudah diekstrak
            else:
                st.warning(f"Percobaan {attempt + 1}/{max_retries}: Tidak dapat menemukan blok JSON yang valid dalam respons Gemini. Respons mentah:\n```\n{gemini_analysis_raw_text}\n```\nMencoba lagi...")
                time.sleep(1)
                continue

        except json.JSONDecodeError as json_err:
            st.warning(f"Percobaan {attempt + 1}/{max_retries}: Gagal memparsing respons JSON dari Gemini: {json_err}. Respons mentah:\n```json\n{json_string if 'json_string' in locals() else gemini_analysis_raw_text}\n```\nMencoba lagi...")
            time.sleep(1)
            continue
        except Exception as e:
            st.warning(f"Percobaan {attempt + 1}/{max_retries}: Terjadi kesalahan umum saat analisis promosi dengan Gemini: {e}. Mencoba lagi...")
            time.sleep(1)
            continue

    # Jika semua percobaan gagal
    st.error(f"Semua {max_retries} percobaan untuk mendapatkan analisis valid gagal.")
    return None