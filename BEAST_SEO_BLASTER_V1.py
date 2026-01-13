import streamlit as st
from groq import Groq
import requests
import re
from fpdf import FPDF

# --- ⚙️ المحرك الأساسي ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.set_page_config(page_title="Beast Agency V8.2", layout="wide")

# --- 🛠️ وظيفة إنشاء PDF احترافي ومنظم ---
def create_beast_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    
    # Header - العنوان
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 255, 204) # اللون الأخضر ديال الوحش
    pdf.cell(200, 20, txt="BEAST CONTENT REPORT", ln=True, align='C')
    pdf.ln(5)
    
    # Subject - الموضوع
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt=f"Topic: {title}", ln=True, align='L')
    pdf.ln(10)
    
    # Content - المحتوى
    pdf.set_font("Arial", size=12)
    # تنظيف النص وتنسيقه للـ PDF
    paragraphs = content.split('\n')
    for p in paragraphs:
        clean_p = p.encode('latin-1', 'ignore').decode('latin-1')
        if clean_p.startswith('##'): # تحويل العناوين الفرعية
            pdf.set_font("Arial", 'B', 14)
            pdf.multi_cell(0, 10, txt=clean_p.replace('##', '').strip())
            pdf.set_font("Arial", size=12)
        else:
            pdf.multi_cell(0, 7, txt=clean_p)
        pdf.ln(2)
        
    return pdf.output(dest='S').encode('latin-1')

# --- 🎨 الستايل والتبويبات (كما هي في V8.0) ---
st.title("🦁 Beast Agency V8.2: Professional Reports")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔎 Keywords", "📝 Sniper Article", "🎨 Image Prompts", "🎯 Facebook Sniper", "💼 Gig Architect"])

# --- ميزة الـ PDF فـ Tab 2 ---
with tab2:
    if 'article' in st.session_state:
        st.write("---")
        st.subheader("📥 Export Your Professional Report")
        if st.button("Build PDF Report"):
            pdf_bytes = create_beast_pdf(st.session_state.get('last_key', 'Article'), st.session_state['article'])
            st.download_button(
                label="📥 Download Pro PDF (Ready for Fiverr)",
                data=pdf_bytes,
                file_name="Beast_Expert_Report.pdf",
                mime="application/pdf"
            )
