import streamlit as st
from groq import Groq
import requests
import re
from fpdf import FPDF

# --- ⚙️ الإعدادات ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ خاصك تزيد GROQ_API_KEY فـ Streamlit Secrets!")

st.set_page_config(page_title="Beast Agency V8.3", layout="wide")

# --- 🛠️ وظيفة إنشاء PDF احترافي ---
def create_beast_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(200, 20, txt="BEAST CONTENT REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Topic: {title}", ln=True, align='L')
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
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

# --- 🎨 الستايل ---
st.markdown("<style>.stApp { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

# --- 🚀 Sidebar: هنا فين كادخل المعلومات (المحرك) ---
st.sidebar.header("🎯 Master Control")
niche_input = st.sidebar.text_input("Niche (e.g. AI Ads)", value="AI Strategy")
target_url = st.sidebar.text_input("Fiverr Link", value="https://www.fiverr.com/s/EgLla1d")

st.title("🦁 Beast Agency V8.3: The Full Arsenal")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔎 Keywords", "📝 Sniper Article", "🎨 Image Prompts", "🎯 Facebook Sniper", "💼 Gig Architect"])

# --- 1. Keywords ---
with tab1:
    st.subheader("🔎 Hunt for Traffic")
    if st.button("Generate Gold Keywords"):
        res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche_input}").json()[1]
        st.session_state['keys'] = res
        st.success("Target Locked!")
    if 'keys' in st.session_state:
        st.write(st.session_state['keys'])

# --- 2. Article (الكلمات + المقال + PDF) ---
with tab2:
    st.subheader("📝 Sniper Article Factory")
    if 'keys' in st.session_state:
        selected_key = st.selectbox("Select Keyword to Target", st.session_state['keys'])
        if st.button("Generate Professional Article"):
            with st.spinner("Writing..."):
                prompt = f"Write a 500-word SEO article about '{selected_key}'. MANDATORY: Link 'Expert AI Service' to {target_url} 3 times."
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                st.session_state['article'] = response.choices[0].message.content
                st.session_state['current_key'] = selected_key

        if 'article' in st.session_state:
            st.markdown("### Preview:")
            st.write(st.session_state['article'])
            
            # أزرار النسخ والـ PDF
            col1, col2 = st.columns(2)
            with col1:
                beast_copy(st.session_state['article'], "📋 Copy Article Text")
            with col2:
                pdf_bytes = create_beast_pdf(st.session_state['current_key'], st.session_state['article'])
                st.download_button(label="📥 Download Pro PDF", data=pdf_bytes, file_name=f"{st.session_state['current_key']}.pdf", mime="application/pdf")

# --- 3. Image Prompt ---
with tab3:
    st.subheader("🎨 Image Architect")
    if 'article' in st.session_state:
        if st.button("Generate Image Prompt"):
            res_img = client.chat.completions.create(messages=[{"role": "user", "content": f"Create DALL-E 3 prompt for {st.session_state['current_key']}"}], model="llama-3.3-70b-versatile")
            st.session_state['img_p'] = res_img.choices[0].message.content
        if 'img_p' in st.session_state:
            st.info(st.session_state['img_p'])
            beast_copy(st.session_state['img_p'], "📋 Copy Prompt")

# --- 4. Facebook Sniper ---
with tab4:
    st.subheader("🎯 Social Media Hooks")
    if 'article' in st.session_state:
        if st.button("Generate Viral FB Hooks"):
            res_fb = client.chat.completions.create(messages=[{"role": "user", "content": f"Write 3 FB hooks for this: {st.session_state['article'][:300]}"}], model="llama-3.3-70b-versatile")
            st.session_state['fb_hooks'] = res_fb.choices[0].message.content
        if 'fb_hooks' in st.session_state:
            st.success(st.session_state['fb_hooks'])
            beast_copy(st.session_state['fb_hooks'], "📋 Copy Hooks")

# --- 5. Gig Architect ---
with tab5:
    st.subheader("💼 Gig Description Creator")
    service = st.selectbox("Choose Service", ["SEO Writing", "AI Image Creation", "FB Ad Strategy"])
    if st.button("Build Gig Description"):
        res_gig = client.chat.completions.create(messages=[{"role": "user", "content": f"Write a Fiverr gig description for {service}"}], model="llama-3.3-70b-versatile")
        st.session_state['gig_desc'] = res_gig.choices[0].message.content
    if 'gig_desc' in st.session_state:
        st.write(st.session_state['gig_desc'])
        beast_copy(st.session_state['gig_desc'], "📋 Copy Gig Description")
