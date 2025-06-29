import streamlit as st

def render_custom_sidebar_content():
    # Tambahkan navigasi kustom di sini
    st.markdown("---") # Garis pemisah sebelum navigasi kustom

    st.markdown("#### Jelajahi Halaman Lain:") # Judul untuk bagian navigasi kustom
    st.page_link("app.py", label="Beranda Utama", icon="🏠")
    st.page_link("pages/2_Panduan & Tips.py", label="Panduan & Tips", icon="💡")
    st.page_link("pages/3_Contoh & Inspirasi.py", label="Contoh & Inspirasi", icon="✨")
    st.page_link("pages/4_Tentang Saya.py", label="Tentang Saya", icon="👤")

    st.markdown("---") # Garis pemisah setelah navigasi kustom

    """
    Fungsi ini berisi semua elemen UI kustom yang Anda inginkan di sidebar,
    yang akan muncul di bawah navigasi otomatis Streamlit.
    """
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

def render_sidebar_expander_content():
    st.markdown("---")
    with st.expander("Tentang Aplikasi"):
        st.markdown("""
        Nusantara Story AI adalah proyek inovatif untuk menggali dan mempromosikan kekayaan budaya serta potensi pariwisata Indonesia menggunakan kecerdasan buatan Gemini.
        """)
        st.markdown("[Pelajari Lebih Lanjut](Tentang%20Saya)")
    st.markdown("---")