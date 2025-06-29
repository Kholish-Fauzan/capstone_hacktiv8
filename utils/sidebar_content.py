import streamlit as st

def render_custom_sidebar_content():
    st.markdown("---")
    st.subheader("Jelajahi Halaman Lain")
    st.page_link("app.py", label="Beranda Utama", icon="🏠")
    st.page_link("pages/2_Panduan & Tips.py", label="Panduan & Tips", icon="💡")
    st.page_link("pages/3_Contoh & Inspirasi.py", label="Contoh & Inspirasi", icon="✨")
    st.page_link("pages/4_Tentang Saya.py", label="Tentang Saya", icon="👤")

    st.markdown("---")

    st.subheader("Bagaimana Kami Membantu Anda?")
    st.markdown("""
    Nusantara Story AI adalah teman setia Anda dalam **mengungkap dan membagikan pesona narasi Indonesia**. Kami memandu Anda melalui empat langkah mudah:

    * **1. Masukkan Detail Objek**: Mulai dengan memberikan informasi kunci tentang objek budaya atau destinasi wisata Anda. Semakin detail, semakin kaya hasilnya!
    * **2. Rangkai Kisah Otentik**: Biarkan AI kami menyusun narasi yang indah, memukau, dan relevan dengan esensi cerita Anda. ✨
    * **3. Analisis Potensi Promosi**: Dapatkan wawasan cerdas tentang strategi promosi yang efektif dan ide pengembangan ekonomi lokal yang inovatif. 📈
    * **4. Unduh & Bagikan**: Kisah dan analisis Anda siap untuk disebarluaskan, menginspirasi, dan menarik perhatian dunia! 📊
    """)

    st.info("💡 **Tips Cepat:** Semakin detail input Anda, semakin berkualitas hasil narasi dan analisis dari AI! Ayo berikan informasi selengkapnya.")

def render_sidebar_expander_content():
    with st.expander("Tentang Aplikasi Ini"):
        st.markdown("""
        **Nusantara Story AI** adalah proyek inovatif yang memanfaatkan teknologi AI Gemini untuk **menggali dan mempromosikan kekayaan budaya serta potensi pariwisata Indonesia**.

        Kami juga menggunakan **IBM Granite** untuk optimasi kode aplikasi ini. Dedikasi kami adalah menciptakan solusi yang intuitif dan efektif demi kemajuan narasi lokal.
        """)