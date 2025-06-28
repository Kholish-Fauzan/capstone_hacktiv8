# pages/about_me_page.py
import streamlit as st
from datetime import datetime
from utils.sidebar_content import render_custom_sidebar_content, render_sidebar_expander_content # Import fungsi baru

# --- Load Custom CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('assets/style.css')

# --- Streamlit UI Setup for this specific page ---
st.set_page_config(
    page_title="Tentang Saya",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar (Revisi): Hanya header dan panggil fungsi konten kustom ---
with st.sidebar:
    st.header("Nusantara Story AI")
    render_custom_sidebar_content()
    render_sidebar_expander_content() # Jika ingin menambahkan expander seperti ReFisher


# Konten utama halaman ini (TETAP SAMA)
st.title("Tentang Saya & Kontak 👋")
st.markdown("Salam kenal! Saya adalah Kholish Fauzan, pengembang di balik Nusantara Story AI.")
st.markdown("---")

st.subheader("Perjalanan di Balik Aplikasi Ini 💡")
st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
st.write("""
Saya Kholish Fauzan, seorang individu yang memiliki semangat besar untuk teknologi dan kekayaan budaya Indonesia. Aplikasi Nusantara Story AI ini lahir dari keinginan saya untuk menjembatani kemajuan teknologi kecerdasan buatan dengan potensi luar biasa dari warisan budaya dan pariwisata lokal kita.

Saya percaya bahwa setiap daerah memiliki kisah unik yang layak diceritakan dan potensi ekonomi yang menunggu untuk digali. Dengan AI Gemini, saya berharap aplikasi ini dapat menjadi alat yang memberdayakan masyarakat, penggiat budaya, dan pelaku pariwisata untuk merangkai narasi yang memukau dan strategi promosi yang efektif.

Semoga aplikasi sederhana ini dapat memberikan manfaat nyata bagi pelestarian budaya dan pengembangan pariwisata di seluruh Nusantara.
""")
st.markdown('</div>', unsafe_allow_html=True)

st.subheader("Mari Terhubung! 📧")
st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
st.write("Saya sangat antusias untuk mendengar *feedback*, ide, atau pertanyaan dari Anda. Jangan ragu untuk terhubung!")
st.markdown("""
-   **Email:** [kholishfauzan.personal@gmail.com](mailto:kholishfauzan.personal@gmail.com) 📧
-   **LinkedIn:** [linkedin.com/in/kholish-fauzan](https://www.linkedin.com/in/kholish-fauzan) 🔗
-   **GitHub:** [github.com/KholishFauzan](https://github.com/KholishFauzan) 💻
""")
st.markdown('</div>', unsafe_allow_html=True)


st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #777;'>© {datetime.now().year} Nusantara Story AI. Dibuat dengan ✨ oleh Kholish Fauzan.</p>", unsafe_allow_html=True)