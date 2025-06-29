import streamlit as st
from datetime import datetime
from utils.sidebar_content import render_custom_sidebar_content, render_sidebar_expander_content

# --- Load Custom CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css('assets/style.css')

# --- Sidebar ---
with st.sidebar:
    st.header("Nusantara Story")
    render_custom_sidebar_content()
    render_sidebar_expander_content()

# Konten utama halaman ini
st.title("Contoh & Inspirasi ✨")
st.markdown("Temukan ide dan lihat bagaimana Nusantara Story bisa membantu Anda merangkai kisah dan strategi promosi yang powerful!")
st.markdown("---")

st.subheader("Narasi & Analisis Promosi - Gunung Bromo, Jawa Timur 🌋")
st.markdown("#### Kisah Bromo: Pesona Magis Sang Penjaga Timur")
st.write("""
**Judul Objek:** Gunung Bromo
**Lokasi:** Taman Nasional Bromo Tengger Semeru, Jawa Timur
**Deskripsi Kunci:** Gunung berapi aktif dengan kawah berasap, pemandangan matahari terbit yang ikonik, pasir berbisik, suku Tengger, upacara Yadnya Kasada.

Tersembunyi di jantung Taman Nasional Bromo Tengger Semeru, Jawa Timur, terhampar permadani perkebunan kopi yang menghasilkan salah satu harta karun terbaik Indonesia: Kopi Gayo. Bukan sekadar minuman, Kopi Gayo adalah warisan berharga yang tumbuh subur di ketinggian 1.200 meter di atas permukaan laut, diberkahi dengan tanah vulkanis subur dan iklim mikro yang ideal. Cita rasanya yang unik dan kompleks – perpaduan antara *fruity*, *spicy*, dengan sedikit sentuhan cokelat dan *earthy* – telah memikat lidah para pecinta kopi di seluruh dunia.

Keistimewaan Kopi Gayo tak hanya terletak pada rasanya, namun juga pada proses pasca-panennya yang khas, yaitu "Giling Basah". Metode ini memberikan karakteristik bodi yang tebal dan aroma yang kuat, membedakannya dari kopi lain. Lebih dari itu, Kopi Gayo adalah cerminan ketekunan dan kearifan komunitas petani lokal yang telah mengolah kopi secara turun-temurun. Setiap biji kopi adalah hasil kerja keras, cinta, dan dedikasi, menjadikan Kopi Gayo sebagai simbol kebanggaan dan identitas bagi masyarakat Gayo. Menikmati Kopi Gayo berarti menikmati secangkir cerita tentang alam, budaya, dan semangat pantang menyerah.
""")

st.subheader("Analisis Promosi untuk Gunung Bromo")
st.markdown("**👉 Poin Jual Utama**")
st.write("""
- **Matahari Terbit Ikonik:** Pemandangan matahari terbit dengan lautan awan dan siluet gunung berapi yang ikonik.
- **Lanskap Unik:** Kombinasi kawah berasap, lautan pasir, dan perbukitan Teletubbies menciptakan lanskap *surreal* dan fotogenik.
- **Budaya Tengger:** Keunikan budaya dan tradisi lokal suku Tengger, terutama upacara Yadnya Kasada.
""")

st.markdown("**👉 Segmen Wisatawan Ideal**")
st.write("""
- **Petualang & Fotografer:** Mencari pengalaman alam ekstrem dan pemandangan luar biasa.
- **Pencinta Budaya:** Tertarik pada tradisi lokal yang otentik dan interaksi dengan masyarakat adat.
- **Wisatawan Internasional:** Bromo sudah dikenal luas di dunia.
""")

st.markdown("---")

st.subheader("Narasi & Analisis Promosi - Kopi Gayo, Aceh ☕")
st.markdown("#### Kisah Kopi Gayo: Aroma Warisan Dataran Tinggi")
st.write("""
**Judul Objek:** Kopi Gayo
**Lokasi:** Dataran Tinggi Gayo, Aceh Tengah
**Deskripsi Kunci:** Kopi Arabika, cita rasa unik (fruity, spicy), ditanam di ketinggian, proses pasca-panen basah (Giling Basah), sejarah panjang, komunitas petani.

Di perbukitan hijau Dataran Tinggi Gayo, Aceh Tengah, terhampar permadani perkebunan kopi yang menghasilkan salah satu harta karun terbaik Indonesia: Kopi Gayo. Bukan sekadar minuman, Kopi Gayo adalah warisan berharga yang tumbuh subur di ketinggian 1.200 meter di atas permukaan laut, diberkahi dengan tanah vulkanis subur dan iklim mikro yang ideal. Cita rasanya yang unik dan kompleks – perpaduan antara *fruity*, *spicy*, dengan sedikit sentuhan cokelat dan *earthy* – telah memikat lidah para pecinta kopi di seluruh dunia.

Keistimewaan Kopi Gayo tak hanya terletak pada rasanya, namun juga pada proses pasca-panennya yang khas, yaitu "Giling Basah". Metode ini memberikan karakteristik bodi yang tebal dan aroma yang kuat, membedakannya dari kopi lain. Lebih dari itu, Kopi Gayo adalah cerminan ketekunan dan kearifan komunitas petani lokal yang telah mengolah kopi secara turun-temurun. Setiap biji kopi adalah hasil kerja keras, cinta, dan dedikasi, menjadikan Kopi Gayo sebagai simbol kebanggaan dan identitas bagi masyarakat Gayo. Menikmati Kopi Gayo berarti menikmati secangkir cerita tentang alam, budaya, dan semangat pantang menyerah.
""")

st.subheader("Analisis Promosi untuk Kopi Gayo")
st.markdown("**👉 Poin Jual Utama**")
st.write("""
- **Cita Rasa Khas:** Profil rasa yang unik dan kompleks, diminati oleh penikmat kopi spesialti.
- **Proses Giling Basah:** Metode pengolahan yang khas memberikan karakteristik rasa dan aroma tersendiri.
- **Kualitas Arabika Premium:** Kopi yang ditanam di ketinggian ideal, menjamin kualitas biji.
""")

st.markdown("**👉 Segmen Wisatawan Ideal**")
st.write("""
- **Pecinta Kopi & Barista:** Tertarik pada asal-usul, proses, dan pengalaman mencicipi kopi langsung.
- **Wisatawan Edukatif:** Ingin belajar tentang pertanian kopi dan budaya lokal.
- **Eksportir & Distributor Kopi:** Mencari produk kopi berkualitas tinggi.
""")

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #777;'>© {datetime.now().year} Nusantara Story. Dibuat dengan ✨ oleh Kholish Fauzan.</p>", unsafe_allow_html=True)