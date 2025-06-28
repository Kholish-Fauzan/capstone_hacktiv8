# utils/gemini_utils.py
import json
import streamlit as st

def generate_narrative(model, judul_objek, lokasi_objek, deskripsi_kunci, target_audiens, gaya_bahasa):
    """
    Menghasilkan narasi cerita berdasarkan input pengguna menggunakan model Gemini.
    """
    prompt = f"""
    Anda adalah seorang ahli narasi budaya dan pariwisata Indonesia. Buatlah narasi yang memukau dan informatif tentang objek budaya/pariwisata berikut:

    Nama Objek: {judul_objek}
    Lokasi: {lokasi_objek}
    Deskripsi Kunci/Fakta Sejarah: {deskripsi_kunci}

    Target Audiens (jika ada): {target_audiens if target_audiens else 'Umum'}
    Gaya Bahasa (jika dipilih): {gaya_bahasa if gaya_bahasa != 'Pilih Gaya' else 'Informatif dan Menarik'}

    Fokuskan pada:
    1. Keunikan dan daya tarik utama objek tersebut.
    2. Sejarah atau latar belakang budaya yang relevan (jika ada dalam deskripsi kunci).
    3. Potensi pengalaman bagi pengunjung/pembaca.
    4. Gunakan bahasa yang kaya dan deskriptif.
    5. Panjang narasi sekitar 400-600 kata.

    Pastikan narasi tersebut otentik dan menggugah minat.
    """
    try:
        response = model.generate_content(prompt)
        # Mengakses teks dari bagian text response
        return response.text
    except Exception as e:
        st.error(f"Terjadi kesalahan saat menghasilkan narasi: {e}")
        return None

def generate_analysis_data(model, lokasi_objek, narrative_text):
    """
    Menganalisis narasi yang dihasilkan untuk memberikan wawasan promosi dan monetisasi.
    Mengembalikan data dalam format JSON.
    """
    prompt = f"""
    Berdasarkan narasi tentang objek budaya/pariwisata dari {lokasi_objek} ini, berikan analisis mendalam yang berfokus pada potensi promosi dan pengembangan ekonomi lokal.

    Narasi:
    {narrative_text}

    Berikan output dalam format JSON yang terstruktur dengan kunci-kunci berikut. Untuk setiap kunci, berikan minimal 3 poin (jika relevan).

    {{
      "Poin Jual Utama": [
        {{"poin": "Poin utama 1", "deskripsi": "Deskripsi poin 1"}},
        {{"poin": "Poin utama 2", "deskripsi": "Deskripsi poin 2"}}
      ],
      "Segmen Wisatawan Ideal": [
        {{"poin": "Segmen 1", "deskripsi": "Deskripsi segmen 1"}},
        {{"poin": "Segmen 2", "deskripsi": "Deskripsi segmen 2"}}
      ],
      "Ide Monetisasi & Produk Pariwisata": [
        {{"poin": "Ide 1", "deskripsi": "Deskripsi ide 1"}},
        {{"poin": "Ide 2", "deskripsi": "Deskripsi ide 2"}}
      ],
      "Saran Peningkatan Pesan Promosi": [
        {{"poin": "Saran 1", "deskripsi": "Deskripsi saran 1"}},
        {{"poin": "Saran 2", "deskripsi": "Deskripsi saran 2"}}
      ],
      "Potensi Kolaborasi Lokal": [
        {{"poin": "Kolaborasi 1", "deskripsi": "Deskripsi kolaborasi 1"}},
        {{"poin": "Kolaborasi 2", "deskripsi": "Deskripsi kolaborasi 2"}}
      ]
    }}

    Pastikan output adalah JSON yang valid dan dapat di-parse langsung.
    """
    try:
        response = model.generate_content(prompt)
        # Mencoba membersihkan respons jika ada markdown atau teks tambahan
        json_text = response.text.strip()
        if json_text.startswith("```json"):
            json_text = json_text[len("```json"):].strip()
        if json_text.endswith("```"):
            json_text = json_text[:-len("```")].strip()

        return json.loads(json_text)
    except json.JSONDecodeError as e:
        st.error(f"Gagal mengurai respons AI sebagai JSON. Mohon coba lagi. Error: {e}")
        st.write("Respons AI mentah (untuk debugging):", response.text)
        return None
    except Exception as e:
        st.error(f"Terjadi kesalahan saat menghasilkan analisis: {e}")
        return None