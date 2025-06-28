# config.py
import streamlit as st
import google.generativeai as genai
import os

# Google Gemini API Key
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Google Gemini API key tidak ditemukan di Streamlit Secrets. Pastikan sudah diatur.")
    st.stop()

# Fungsi untuk mendapatkan model Gemini yang dikonfigurasi
def get_gemini_model():
    genai.configure(api_key=GOOGLE_API_KEY)
    return genai.GenerativeModel('gemini-2.5-flash')