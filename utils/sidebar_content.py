import streamlit as st

def render_custom_sidebar_content():
    st.markdown("---") # Garis pemisah sebelum navigasi kustom agar lebih terstruktur
    st.subheader("Jelajahi Halaman Lain") # Menggunakan st.subheader agar bisa diatur stylenya di CSS
    st.page_link("app.py", label="Beranda Utama", icon="🏠")
    st.page_link("pages/2_Panduan & Tips.py", label="Panduan & Tips", icon="💡")
    st.page_link("pages/3_Contoh & Inspirasi.py", label="Contoh & Inspirasi", icon="✨")
    st.page_link("pages/4_Tentang Saya.py", label="Tentang Saya", icon="👤")

    st.markdown("---") # Garis pemisah setelah navigasi kustom

    st.subheader("Bagaimana Kami Membantu Anda?") # UX Writing lebih langsung
    st.markdown("""
    Nusantara Story AI hadir untuk memberdayakan Anda dalam merangkai dan membagikan kekayaan narasi Indonesia.

    * **1. Masukkan Detail Objek**: Berikan informasi kunci tentang objek budaya atau destinasi wisata Anda.
    * **2. Rangkai Kisah Otentik**: AI kami akan menyusun cerita yang indah dan menarik. ✨
    * **3. Analisis Potensi Promosi**: Dapatkan wawasan tentang strategi promosi & pengembangan ekonomi lokal. 📈
    * **4. Unduh & Bagikan**: Hasil narasi dan analisis siap Anda gunakan! 📊
    """)

    st.info("💡 **Tips Cepat:** Semakin detail input Anda, semakin berkualitas hasil narasi dan analisis dari AI! Ayo berikan informasi selengkapnya.")

def render_sidebar_expander_content():
    with st.expander("Tentang Aplikasi Ini"): # Ganti judul expander agar lebih spesifik
        st.markdown("""
        **Nusantara Story AI** adalah proyek inovatif yang memanfaatkan teknologi AI Gemini untuk **menggali dan mempromosikan kekayaan budaya serta potensi pariwisata Indonesia**.

        Kami juga menggunakan **IBM Granite** untuk optimasi kode aplikasi ini. Dedikasi kami adalah menciptakan solusi yang intuitif dan efektif demi kemajuan narasi lokal.
        """)