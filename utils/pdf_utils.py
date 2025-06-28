# utils/pdf_utils.py
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import streamlit as st # Masih perlu untuk st.session_state dan st.error

def generate_pdf_from_text(text_content, filename_prefix="document"):
    """Menghasilkan PDF dari teks biasa."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()

    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.leading = 14

    title_style = styles['h1']
    title_style.fontSize = 18
    title_style.alignment = 1

    story = []
    if "judul_objek" in st.session_state and st.session_state.judul_objek:
        story.append(Paragraph(st.session_state.judul_objek, title_style))
        story.append(Spacer(1, 0.2 * inch))

    paragraphs = text_content.split('\n\n')
    for para_text in paragraphs:
        if para_text.strip():
            story.append(Paragraph(para_text.replace('\n', '<br/>'), normal_style))
            story.append(Spacer(1, 0.1 * inch))

    try:
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Gagal membuat PDF narasi: {e}")
        return None

def generate_analysis_pdf(analysis_data, filename_prefix="analysis"):
    """Menghasilkan PDF dari data analisis dalam bentuk layout terpisah, bukan tabel."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()

    title_style = styles['h1']
    title_style.fontSize = 18
    title_style.alignment = 1

    section_title_style = ParagraphStyle('SectionTitle',
                                         parent=styles['h2'],
                                         fontName='Helvetica-Bold',
                                         fontSize=12,
                                         spaceAfter=6)

    sub_point_style = ParagraphStyle('SubPoint',
                                     parent=styles['Normal'],
                                     fontName='Helvetica-Bold',
                                     fontSize=10,
                                     spaceAfter=2,
                                     leftIndent=20)

    description_style = ParagraphStyle('Description',
                                       parent=styles['Normal'],
                                       fontSize=9,
                                       spaceAfter=12,
                                       leftIndent=20)

    story = []
    story.append(Paragraph("Wawasan & Optimasi Promosi dari Gemini AI", title_style))
    story.append(Spacer(1, 0.2 * inch))

    if analysis_data:
        ordered_keys = [
            "Poin Jual Utama",
            "Segmen Wisatawan Ideal",
            "Ide Monetisasi & Produk Pariwisata",
            "Saran Peningkatan Pesan Promosi",
            "Potensi Kolaborasi Lokal"
        ]

        for key in ordered_keys:
            if key in analysis_data:
                story.append(Paragraph(key, section_title_style))
                items = analysis_data[key]
                for item in items:
                    if "poin" in item and "deskripsi" in item:
                        story.append(Paragraph(f"{item['poin']}:", sub_point_style))
                        story.append(Paragraph(item['deskripsi'], description_style))
                    elif "deskripsi" in item:
                        story.append(Paragraph(f"• {item['deskripsi']}", description_style))
                    else:
                        story.append(Paragraph(f"• {str(item)}", description_style))
                story.append(Spacer(1, 0.2 * inch))

    else:
        story.append(Paragraph("Tidak ada data analisis yang valid untuk ditampilkan.", styles['Normal']))

    try:
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Gagal membuat PDF analisis: {e}")
        return None