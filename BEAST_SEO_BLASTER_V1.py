import streamlit as st
from groq import Groq
import requests
import re

# --- ⚙️ المحرك الأساسي ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.set_page_config(page_title="Beast Sniper V6.5", layout="wide")

# --- 🛠️ زر النسخ الذكي (JavaScript - حل نهائي للـ TypeError) ---
def professional_copy(text_to_copy, button_label):
    # تحويل النص لـ string وتنظيفه من الرموز اللي كاتهرس الكود
    safe_text = str(text_to_copy).replace("`", "'").replace("\n", "\\n")
    html_button = f"""
    <div style="margin: 10px 0;">
        <button onclick="copyToClipboard{id(text_to_copy)}()" 
        style="background-color: #00ffcc; color: black; border: none; padding: 12px 24px; 
        border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px;">
            {button_label}
        </button>
    </div>
    <script>
    function copyToClipboard{id(text_to_copy)}() {{
        const text = `{safe_text}`;
        const tempInput = document.createElement('textarea');
        tempInput.value = text;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
        alert('✅ Copied to Clipboard!');
    }}
    </script>
    """
    st.components.v1.html(html_button, height=70)

# --- 🎨 مظهر الداشبورد (Clean Dark UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .article-box { background-color: white; color: black; padding: 25px; border-radius: 12px; line-height: 1.8; font-family: sans-serif; }
    .prompt-box { background-color: #1a1c24; border: 1px dashed #00ffcc; padding: 15px; border-radius: 8px; color: #00ffcc; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Beast Sniper V6.5: Ultimate Stability")

# Sidebar
st.sidebar.header("⚙️ Sniper Configuration")
niche = st.sidebar.text_input("Niche", value="AI Solutions")
target_url = st.sidebar.text_input("Fiverr Link", value="https://www.fiverr.com/s/EgLla1d")

tab1, tab2, tab3 = st.tabs(["🔎 Keyword Sniper", "📝 Sniper Article", "🎨 Image Architect"])

# --- 1. Keywords Sniper ---
with tab1:
    if st.button("Hunt Keywords"):
        res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}").json()[1]
        st.session_state['keys'] = res
        st.success(f"لقيت {len(res)} كلمة مفتاحية!")
    if 'keys' in st.session_state:
        st.write(st.session_state['keys'])

# --- 2. Sniper Article (500 كلمة + روابط محقونة) ---
with tab2:
    if 'keys' in st.session_state:
        selected_key = st.selectbox("Select Target", st.session_state['keys'])
        if st.button("Generate Article"):
            with st.spinner("Writing & Injecting..."):
                prompt = f"Write a 500-word SEO article about '{selected_key}'. MANDATORY: Link 'this expert service' and 'Hire on Fiverr' to: {target_url} using Markdown [Text](URL)."
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.3)
                st.session_state['article'] = response.choices[0].message.content

        if 'article' in st.session_state:
            st.markdown('<div class="article-box">', unsafe_allow_html=True)
            st.markdown(st.session_state['article'])
            st.markdown('</div>', unsafe_allow_html=True)

            # معالجة HTML لـ Blogger
            html_raw = str(st.session_state['article']).replace("## ", "<h2>").replace("\n", "<br>")
            html_final = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', html_raw)
            
            st.write("---")
            st.subheader("📋 Copy for Blogger (HTML View):")
            professional_copy(html_final, "Copy HTML Article 🌐")

# --- 3. Image Architect (رجوع ميزة الصور) ---
with tab3:
    st.subheader("🖼️ Thumbnail Designer")
    if 'article' in st.session_state:
        if st.button("Create Image Prompt"):
            with st.spinner("Analyzing content..."):
                img_req = f"DALL-E 3 prompt for article about {selected_key}. Cinematic, professional, 4k."
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_req}], model="llama-3.3-70b-versatile")
                st.session_state['img_p'] = res_img.choices[0].message.content
        
        if 'img_p' in st.session_state:
            st.markdown(f'<div class="prompt-box">{st.session_state["img_p"]}</div>', unsafe_allow_html=True)
            professional_copy(st.session_state['img_p'], "Copy Image Prompt 🎨")
    else:
        st.warning("⚠️ صاوب المقالة أولاً فـ Tab 2.")
