# utils/pdf_utils.py
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from io import BytesIO

def generate_pdf_from_text(text_content, title="Dokumen Streamlit"):
    """
    Menghasilkan file PDF dari string teks yang diberikan.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom style for title
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['h1'],
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # Custom style for normal text
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=12
    )

    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(text_content.replace('\n', '<br/>'), normal_style)) # Replace newline with <br/> for ReportLab

    try:
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

def generate_analysis_pdf(analysis_data, title="Analisis Promosi"):
    """
    Menghasilkan file PDF dari data analisis yang diberikan dalam format yang terstruktur.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['h1'],
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor='#1ABC9C' # Warna hijau toska
    )
    section_title_style = ParagraphStyle(
        'SectionTitleStyle',
        parent=styles['h2'],
        fontSize=18,
        leading=22,
        spaceAfter=10,
        textColor='#34495E' # Warna biru keabuan
    )
    point_style = ParagraphStyle(
        'PointStyle',
        parent=styles['h3'],
        fontSize=14,
        leading=16,
        spaceBefore=10,
        spaceAfter=5,
        textColor='#2C3E50' # Warna biru gelap
    )
    description_style = ParagraphStyle(
        'DescriptionStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=13,
        spaceAfter=10,
        leftIndent=20
    )
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor='#777777',
        spaceBefore=30
    )

    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.3 * inch))

    for key, items in analysis_data.items():
        story.append(Paragraph(key, section_title_style))
        story.append(Spacer(1, 0.1 * inch))
        if isinstance(items, list):
            for item in items:
                story.append(Paragraph(f"👉 {item.get('poin', '')}", point_style))
                story.append(Paragraph(item.get('deskripsi', ''), description_style))
        else: # Handle cases where value might be a string (e.g., if JSON structure changes)
            story.append(Paragraph(str(items), description_style))
        story.append(Spacer(1, 0.2 * inch))

    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(f"© {datetime.now().year} Nusantara Story AI. Dibuat dengan ✨ oleh Kholish Fauzan.", footer_style))

    try:
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        print(f"Error generating analysis PDF: {e}")
        return None