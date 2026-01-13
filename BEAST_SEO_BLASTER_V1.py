import streamlit as st
from groq import Groq
import requests
from fpdf import FPDF

# --- ⚙️ الإعدادات ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.set_page_config(page_title="Beast Agency V8.5", layout="wide")

# --- 🛠️ وظيفة إنشاء PDF (المقال + الـ Hooks) ---
def create_beast_pdf(title, content, hooks=""):
    pdf = FPDF()
    pdf.add_page()
    # العنوان
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="BEAST CONTENT REPORT", ln=True, align='C')
    pdf.ln(10)
    # المقال
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Article: {title}", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, txt=content.encode('latin-1', 'ignore').decode('latin-1'))
    
    if hooks:
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Facebook Viral Hooks:", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, txt=hooks.encode('latin-1', 'ignore').decode('latin-1'))
        
    return pdf.output(dest='S').encode('latin-1')

# --- 🛠️ وظيفة النسخ (JS) ---
def beast_copy(text, label):
    safe_text = str(text).replace("`", "'").replace("\n", "\\n")
    btn_id = f"btn_{id(text)}"
    st.components.v1.html(f"""
    <button id="{btn_id}" style="background-color: #00ffcc; color: black; border: none; padding: 12px; border-radius: 10px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px;">{label}</button>
    <script>document.getElementById("{btn_id}").onclick = function() {{ const el = document.createElement('textarea'); el.value = `{safe_text}`; document.body.appendChild(el); el.select(); document.execCommand('copy'); document.body.removeChild(el); alert('✅ Copied to Clipboard!'); }};</script>
    """, height=70)

st.title("🦁 Beast Agency V8.5")

# --- 🎯 1. Target Info ---
st.header("🎯 1. Target Info")
niche_input = st.text_input("Niche:", value="AI Strategy")
target_url = st.text_input("Fiverr Link:", value="https://www.fiverr.com/s/EgLla1d")

# --- 🔎 2. Keywords ---
if st.button("🚀 Hunt Keywords Now"):
    res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche_input}").json()[1]
    st.session_state['keys'] = res

if 'keys' in st.session_state:
    selected_key = st.selectbox("Choose Keyword:", st.session_state['keys'])
    
    # --- 📝 3. Article ---
    st.header("📝 2. Professional Article")
    if st.button("✍️ Generate Article"):
        prompt = f"Write a 500-word SEO article about '{selected_key}'. Link 'Expert AI Service' to {target_url} 3 times."
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        st.session_state['article'] = res.choices[0].message.content
        st.session_state['current_key'] = selected_key

    if 'article' in st.session_state:
        st.write(st.session_state['article'])
        beast_copy(st.session_state['article'], "📋 Copy Article Text")

        # --- 🎯 4. Facebook Hooks ---
        st.header("🎯 3. Facebook Hooks")
        if st.button("🔥 Generate Viral Hooks"):
            fb_res = client.chat.completions.create(messages=[{"role": "user", "content": f"Write 3 viral FB hooks for: {st.session_state['article'][:300]}"}], model="llama-3.3-70b-versatile")
            st.session_state['fb_hooks'] = fb_res.choices[0].message.content
        
        if 'fb_hooks' in st.session_state:
            st.success(st.session_state['fb_hooks'])
            beast_copy(st.session_state['fb_hooks'], "📋 Copy Hooks Only")
            
            st.divider()
            # زر الـ PDF الشامل
            pdf_bytes = create_beast_pdf(st.session_state['current_key'], st.session_state['article'], st.session_state['fb_hooks'])
            st.download_button("📥 Download Full Report (Article + Hooks) PDF", data=pdf_bytes, file_name="Beast_Full_Report.pdf")

# --- 💼 5. Gig Architect ---
st.header("💼 4. Fiverr Gig Architect")
if st.button("🏗️ Build Gig Description"):
    res_gig = client.chat.completions.create(messages=[{"role": "user", "content": f"Write a Fiverr gig description for {niche_input}"}], model="llama-3.3-70b-versatile")
    st.session_state['gig_desc'] = res_gig.choices[0].message.content
if 'gig_desc' in st.session_state:
    st.info(st.session_state['gig_desc'])
    beast_copy(st.session_state['gig_desc'], "📋 Copy Gig Description")
