import streamlit as st
from groq import Groq
import requests
import re

# --- ⚙️ الإعدادات ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.set_page_config(page_title="Beast Sniper V6.0", layout="wide")

# --- 🛠️ وظيفة النسخ الاحترافية (بديلة للمكتبة المهروسة) ---
def copy_button(text_to_copy, label="Copy Text"):
    # كود JavaScript بسيط كيهز النص للمحفظة بلا مشاكل TypeError
    html_code = f"""
    <button onclick="navigator.clipboard.writeText(`{text_to_copy}`)" 
    style="background-color: #00ffcc; color: black; border: none; padding: 10px 20px; 
    border-radius: 5px; font-weight: bold; cursor: pointer;">
    {label}
    </button>
    """
    st.components.v1.html(html_code, height=50)

# --- 🎨 مظهر الداشبورد ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .article-box { background-color: white; color: black; padding: 25px; border-radius: 10px; line-height: 1.6; }
    .prompt-box { background-color: #1a1c24; border: 1px dashed #00ffcc; padding: 15px; border-radius: 8px; color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 Beast Sniper V6.0: The Stable King")

# Sidebar
st.sidebar.header("🎯 Configuration")
niche = st.sidebar.text_input("Niche", value="AI Solutions")
target_url = st.sidebar.text_input("Fiverr Link", value="https://www.fiverr.com/s/EgLla1d")

tab1, tab2, tab3 = st.tabs(["🔎 SEO Sniper", "📝 Sniper Article", "🎨 Image Architect"])

# 1. Keywords
with tab1:
    if st.button("Hunt Keywords"):
        res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}").json()[1]
        st.session_state['keys'] = res
        st.success(f"لقيت {len(res)} كلمة مفتاحية!")
    if 'keys' in st.session_state:
        st.write(st.session_state['keys'])

# 2. Article (الروابط + 500 كلمة)
with tab2:
    if 'keys' in st.session_state:
        selected_key = st.selectbox("Select Target", st.session_state['keys'])
        if st.button("Generate Article"):
            with st.spinner("الوحش يكتب..."):
                prompt = f"Write a professional 500-word SEO article about '{selected_key}'. MANDATORY: Hyperlink 'this expert service' and 'Hire on Fiverr' to: {target_url} using Markdown [Text](URL)."
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.3)
                st.session_state['article'] = response.choices[0].message.content

        if 'article' in st.session_state:
            st.markdown('<div class="article-box">', unsafe_allow_html=True)
            st.markdown(st.session_state['article'])
            st.markdown('</div>', unsafe_allow_html=True)

            # معالجة HTML
            html = str(st.session_state['article']).replace("## ", "<h2>").replace("\n", "<br>")
            html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', html)
            
            st.write("---")
            st.write("📋 **Copy for Blogger (HTML Mode):**")
            copy_button(html.replace("`", "'"), "Copy HTML Code 🌐")

# 3. Image (الميزة اللي رجعناها)
with tab3:
    if 'article' in st.session_state:
        if st.button("Generate Image Prompt"):
            with st.spinner("Analyzing..."):
                img_req = f"Professional DALL-E 3 prompt for article about {niche}. Cinematic style."
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_req}], model="llama-3.3-70b-versatile")
                st.session_state['img_p'] = res_img.choices[0].message.content
        
        if 'img_p' in st.session_state:
            st.markdown(f'<div class="prompt-box">{st.session_state["img_p"]}</div>', unsafe_allow_html=True)
            copy_button(str(st.session_state['img_p']).replace("`", "'"), "Copy Image Prompt 🎨")
