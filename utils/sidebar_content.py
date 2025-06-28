# utils/sidebar_content.py
import streamlit as st

def render_custom_sidebar_content():
    st.sidebar.success("Pilih Satu Halaman di Atas")

    """
    Fungsi ini berisi semua elemen UI kustom yang Anda inginkan di sidebar,
    yang akan muncul di bawah navigasi otomatis Streamlit.
    """
    st.markdown("---") # Garis pemisah antara navigasi dan konten kustom Anda

    st.header("Bagaimana Kami Membantu Anda? 🚀")
    st.markdown("""
    Kami percaya setiap daerah punya kisah unik. Aplikasi ini hadir untuk memberdayakan Anda dalam merangkai dan membagikan kekayaan tersebut.
    1.  **Input Cerita Anda**: Masukkan detail penting tentang objek budaya atau destinasi wisata Anda.
    2.  **Rangkai Narasi Otentik**: AI Gemini akan menyusun cerita yang indah dan menarik. ✨
    3.  **Analisis Potensi Promosi**: Dapatkan wawasan tentang bagaimana mempromosikan dan mengembangkan potensi ekonomi lokal. 📈
    4.  **Unduh & Bagikan**: Hasil narasi dan analisis siap Anda gunakan! 📊
    """)
    st.markdown("---")
    st.write("Dibuat oleh Kholish Fauzan")
    st.markdown("---")
    st.info("Tips: Semakin detail informasi yang Anda berikan, semakin kaya dan relevan hasil dari AI! 💡")

# Contoh tambahan jika Anda ingin menambahkan expander di sidebar seperti ReFisher
def render_sidebar_expander_content():
    st.markdown("---")
    with st.expander("Tentang Aplikasi"):
        st.markdown("""
        Nusantara Story AI adalah proyek inovatif untuk menggali dan mempromosikan kekayaan budaya serta potensi pariwisata Indonesia menggunakan kecerdasan buatan Gemini.
        """)
        st.markdown("[Pelajari Lebih Lanjut](link_ke_halaman_tentang_saya)") # Anda bisa arahkan ke halaman about_me_page
    st.markdown("---")