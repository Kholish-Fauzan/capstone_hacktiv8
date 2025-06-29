import streamlit as st
from datetime import datetime
from utils.sidebar_content import render_custom_sidebar_content, render_sidebar_expander_content

# --- Sidebar (Ditambahkan Kembali): Pastikan ini ada di setiap halaman ---
with st.sidebar:
    st.header("Nusantara Story AI")
    render_custom_sidebar_content()
    render_sidebar_expander_content()


# Konten utama halaman ini (TETAP SAMA)
st.title("Tips & Panduan: Maksimalkan AI Anda! 🚀")
st.markdown("Dapatkan hasil terbaik dari Nusantara Story AI dengan panduan singkat ini. Semakin baik input Anda, semakin berkualitas output yang dihasilkan!")
st.markdown("---")

st.subheader("1. Tips Mengisi Deskripsi Kunci 📝")
st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
st.write("""
* **Detail adalah Kunci!** Semakin banyak detail spesifik yang Anda berikan (nama tokoh sejarah, tanggal penting, keunikan tradisi, ciri khas arsitektur, jenis kuliner, dll.), semakin kaya dan akurat narasi yang AI hasilkan.
* **Gunakan Poin-Poin atau Paragraf Singkat:** Anda bisa menggunakan daftar poin atau paragraf singkat yang padat informasi. AI akan merangkainya menjadi cerita yang mengalir.
* **Sertakan Keunikan:** Apa yang membuat objek ini istimewa? Sebutkan elemen unik yang membedakannya dari yang lain.
* **Libatkan Indera:** Coba deskripsikan apa yang bisa dilihat, didengar, dicium, dirasakan, atau dicicipi di tempat/objek tersebut.
""")
st.markdown('</div>', unsafe_allow_html=True)

st.subheader("2. Memilih Gaya Bahasa yang Tepat 🎭")
st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
st.write("""
Pilihan gaya bahasa akan memengaruhi nuansa dan tujuan narasi Anda:
* **Edukasi:** Cocok untuk materi pembelajaran, fokus pada fakta, sejarah, dan penjelasan yang mudah dimengerti.
* **Promosi:** Ditujukan untuk menarik wisatawan, menggunakan bahasa yang persuasif dan membangkitkan minat.
* **Cerita Rakyat:** Akan menghasilkan narasi dengan nuansa dongeng atau legenda, ideal untuk objek dengan mitos atau cerita lokal.
* **Puitis:** Menggunakan bahasa yang indah, metafora, dan gaya sastra untuk kesan artistik.
* **Informatif:** Ringkas, padat informasi, fokus pada data dan fakta tanpa banyak embel-embel.
* **Inspiratif:** Membangkitkan semangat, motivasi, dan mengajak pembaca untuk merasakan pengalaman.
""")
st.markdown('</div>', unsafe_allow_html=True)

st.subheader("3. Memahami Hasil Analisis Promosi 📈")
st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
st.write("""
Bagian analisis akan memberikan wawasan mendalam untuk strategi promosi Anda:
* **Poin Jual Utama:** Kekuatan inti dari objek budaya/wisata Anda yang bisa ditonjolkan dalam promosi.
* **Segmen Wisatawan Ideal:** Target audiens yang paling mungkin tertarik dengan penawaran Anda.
* **Ide Monetisasi & Produk Pariwisata:** Cara-cara untuk mengembangkan objek menjadi sumber pendapatan atau pengalaman yang lebih kaya.
* **Saran Peningkatan Pesan Promosi:** Rekomendasi untuk membuat materi promosi Anda lebih efektif dan menarik.
* **Potensi Kolaborasi Lokal:** Ide untuk bekerja sama dengan pihak lain di daerah untuk menciptakan nilai tambah.
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #777;'>© {datetime.now().year} Nusantara Story AI. Dibuat dengan ✨ oleh Kholish Fauzan.</p>", unsafe_allow_html=True)