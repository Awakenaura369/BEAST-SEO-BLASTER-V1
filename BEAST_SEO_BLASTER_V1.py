import streamlit as st
from groq import Groq
import requests
import re
from fpdf import FPDF
import base64

# --- ⚙️ الإعدادات ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.set_page_config(page_title="Beast Agency V8.0", layout="wide")

# --- 🛠️ وظيفة إنشاء PDF احترافي ---
def create_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    # تنظيف النص من الرموز الغريبة
    clean_content = content.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_content)
    return pdf.output(dest='S').encode('latin-1')

# --- 🛠️ وظيفة النسخ (JS) ---
def beast_copy(text, label):
    safe_text = str(text).replace("`", "'").replace("\n", "\\n")
    btn_id = f"btn_{id(text)}"
    st.components.v1.html(f"""
    <button id="{btn_id}" style="background-color: #00ffcc; color: black; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%;">{label}</button>
    <script>document.getElementById("{btn_id}").onclick = function() {{ const el = document.createElement('textarea'); el.value = `{safe_text}`; document.body.appendChild(el); el.select(); document.execCommand('copy'); document.body.removeChild(el); alert('✅ Copied!'); }};</script>
    """, height=60)

st.title("🦁 Beast Agency V8.0: The Full Solution")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔎 Keywords", "📝 Sniper Article", "🎨 Image Prompts", "🎯 Facebook Sniper", "💼 Gig Architect"])

# --- التبويبات السابقة تبقى كما هي مع إضافة زر PDF في Tab 2 ---
with tab2:
    if 'keys' in st.session_state:
        selected_key = st.selectbox("Select Target", st.session_state['keys'])
        if st.button("Generate Professional Article"):
            prompt = f"Write a 500-word expert SEO article about '{selected_key}'. Link 'Expert AI Service' to {st.sidebar.text_input('Link', 'https://fiverr.com')}."
            res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            st.session_state['article'] = res.choices[0].message.content
        
        if 'article' in st.session_state:
            st.info("📄 Article is ready!")
            # زر تحميل PDF
            pdf_data = create_pdf(selected_key, st.session_state['article'])
            st.download_button(label="📥 Download Article as PDF", data=pdf_data, file_name=f"{selected_key}.pdf", mime="application/pdf")
            beast_copy(st.session_state['article'], "Copy Text Content")

# --- Tab 5: Gig Architect (الميزة الجديدة) ---
with tab5:
    st.subheader("💼 Create a Winning Fiverr Gig")
    service_type = st.selectbox("What service are you selling?", ["SEO Article Writing", "AI Image Prompt Engineering", "Facebook Ad Strategy"])
    if st.button("Generate High-Converting Gig Description"):
        gig_prompt = f"Write a professional Fiverr Gig Description for: {service_type}. Include: About this gig, Why choose me, and 3 packages (Basic, Standard, Premium). Focus on AI expertise."
        res_gig = client.chat.completions.create(messages=[{"role": "user", "content": gig_prompt}], model="llama-3.3-70b-versatile")
        st.session_state['gig_desc'] = res_gig.choices[0].message.content
    
    if 'gig_desc' in st.session_state:
        st.text_area("Gig Description:", st.session_state['gig_desc'], height=300)
        beast_copy(st.session_state['gig_desc'], "Copy Gig Description")

