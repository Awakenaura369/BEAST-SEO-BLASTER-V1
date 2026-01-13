import streamlit as st
from groq import Groq
import requests
from fpdf import FPDF

# --- ⚙️ الإعدادات ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.set_page_config(page_title="Beast Agency V8.4", layout="wide")

# --- 🛠️ وظيفة إنشاء PDF ---
def create_beast_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="BEAST CONTENT REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content.encode('latin-1', 'ignore').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# --- 🎨 الستايل ---
st.markdown("<style>button { background-color: #00ffcc !important; color: black !important; font-weight: bold !important; height: 3em !important; border-radius: 10px !important; }</style>", unsafe_allow_html=True)

st.title("🦁 Beast Agency V8.4 (Mobile Optimized)")

# --- 1. التحكم الأساسي ---
st.header("🎯 1. Target Info")
niche_input = st.text_input("Niche (مثال: Organic Skincare)", value="AI Strategy")
target_url = st.text_input("Fiverr Link", value="https://www.fiverr.com/s/EgLla1d")

st.divider()

# --- 2. الكلمات المفتاحية ---
st.header("🔎 2. Keywords")
if st.button("🚀 Hunt Keywords Now"):
    res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche_input}").json()[1]
    st.session_state['keys'] = res
    st.success("Keywords Found!")

if 'keys' in st.session_state:
    selected_key = st.selectbox("Choose a Keyword:", st.session_state['keys'])
    
    st.divider()
    
    # --- 3. المقال والـ PDF ---
    st.header("📝 3. Article & PDF")
    if st.button("✍️ Generate Pro Article"):
        with st.spinner("Beast is writing..."):
            prompt = f"Write a 500-word SEO article about '{selected_key}'. Link 'Expert AI Service' to {target_url} 3 times."
            response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            st.session_state['article'] = response.choices[0].message.content
            st.session_state['current_key'] = selected_key

    if 'article' in st.session_state:
        st.write(st.session_state['article'])
        pdf_bytes = create_beast_pdf(st.session_state['current_key'], st.session_state['article'])
        st.download_button("📥 Download PDF Report", data=pdf_bytes, file_name="Report.pdf")

        st.divider()

        # --- 4. فيسبوك ---
        st.header("🎯 4. Facebook Hooks")
        if st.button("🔥 Generate FB Hooks"):
            res_fb = client.chat.completions.create(messages=[{"role": "user", "content": f"Write 3 viral FB hooks for: {st.session_state['article'][:200]}"}], model="llama-3.3-70b-versatile")
            st.session_state['fb_hooks'] = res_fb.choices[0].message.content
        if 'fb_hooks' in st.session_state:
            st.success(st.session_state['fb_hooks'])

st.divider()

# --- 5. Gig Architect ---
st.header("💼 5. Gig Architect")
if st.button("🏗️ Build Fiverr Gig Description"):
    res_gig = client.chat.completions.create(messages=[{"role": "user", "content": f"Write a Fiverr gig description for {niche_input}"}], model="llama-3.3-70b-versatile")
    st.session_state['gig_desc'] = res_gig.choices[0].message.content
if 'gig_desc' in st.session_state:
    st.info(st.session_state['gig_desc'])
