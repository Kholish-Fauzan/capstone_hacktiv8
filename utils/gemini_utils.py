# utils/gemini_utils.py
import streamlit as st
import json

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
                "max_output_tokens": 3000,
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

def generate_analysis_data(model, lokasi_objek, generated_narration):
    """Menghasilkan data analisis menggunakan model Gemini."""
    try:
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

        Narasi yang Dihasilkan:
        ---
        {generated_narration}
        ---
        """

        response_analisis = model.generate_content(
            prompt_analisis,
            generation_config={
                "max_output_tokens": 5000,
                "temperature": 0.5,
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "Poin Jual Utama": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "poin": {"type": "STRING"},
                                    "deskripsi": {"type": "STRING"}
                                },
                                "required": ["poin", "deskripsi"]
                            }
                        },
                        "Segmen Wisatawan Ideal": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "poin": {"type": "STRING"},
                                    "deskripsi": {"type": "STRING"}
                                },
                                "required": ["poin", "deskripsi"]
                            }
                        },
                        "Ide Monetisasi & Produk Pariwisata": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "poin": {"type": "STRING"},
                                    "deskripsi": {"type": "STRING"}
                                },
                                "required": ["poin", "deskripsi"]
                            }
                        },
                        "Saran Peningkatan Pesan Promosi": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "poin": {"type": "STRING"},
                                    "deskripsi": {"type": "STRING"}
                                },
                                "required": ["poin", "deskripsi"]
                            }
                        },
                        "Potensi Kolaborasi Lokal": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "poin": {"type": "STRING"},
                                    "deskripsi": {"type": "STRING"}
                                },
                                "required": ["poin", "deskripsi"]
                            }
                        }
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

        if response_analisis.parts:
            return json.loads(response_analisis.text)
        elif response_analisis.candidates and response_analisis.candidates[0].finish_reason:
            st.warning(f"Gemini tidak dapat menghasilkan analisis. Finish reason: {response_analisis.candidates[0].finish_reason.name}. Coba sesuaikan prompt atau input.")
            return None
        else:
            st.warning("Gemini tidak dapat menghasilkan analisis. Respons kosong atau tidak terduga. Coba sesuaikan prompt atau input.")
            return None

    except json.JSONDecodeError as json_err:
        st.error(f"Gagal memparsing respons JSON dari Gemini: {json_err}. Coba periksa prompt dan input.")
        return None
    except Exception as e:
        st.error(f"Terjadi kesalahan saat analisis promosi dengan Gemini: {e}. Coba periksa prompt dan input.")
        return None