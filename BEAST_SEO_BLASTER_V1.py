import streamlit as st
from groq import Groq
import requests
import re

# --- ⚙️ الإعدادات ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.set_page_config(page_title="Beast Sniper V7.0", layout="wide")

# --- 🛠️ وظيفة النسخ بـ JavaScript (الحل النهائي للـ TypeError) ---
def beast_copy_button(text, label):
    # تنظيف النص باش ما يهرسش كود الجافاسكريبت
    safe_text = str(text).replace("`", "'").replace("\n", "\\n")
    button_id = f"btn_{id(text)}"
    html = f"""
    <button id="{button_id}" style="background-color: #00ffcc; color: black; border: none; 
    padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">
        {label}
    </button>
    <script>
    document.getElementById("{button_id}").onclick = function() {{
        const el = document.createElement('textarea');
        el.value = `{safe_text}`;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
        alert('✅ تم النسخ بنجاح!');
    }};
    </script>
    """
    st.components.v1.html(html, height=60)

# --- 🎨 مظهر الداشبورد ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .article-box { background-color: #ffffff; color: #000; padding: 25px; border-radius: 12px; line-height: 1.8; }
    .prompt-box { background-color: #1a1c24; border: 1px dashed #00ffcc; padding: 15px; border-radius: 8px; color: #00ffcc; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Beast Sniper V7.0: Gig Booster Edition")

# Sidebar
st.sidebar.header("🚀 Target Config")
niche = st.sidebar.text_input("Niche", value="AI Ad Strategy")
target_url = st.sidebar.text_input("Fiverr Link", value="https://www.fiverr.com/s/EgLla1d")

tab1, tab2, tab3 = st.tabs(["🔎 Keyword Sniper", "📝 High-Value Article", "🎨 Image Architect"])

# 1. Keywords
with tab1:
    if st.button("Hunt Gold Keywords"):
        res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}").json()[1]
        st.session_state['keys'] = res
        st.success(f"لقيت {len(res)} كلمة مفتاحية!")

# 2. Article (500 كلمة مركزة)
with tab2:
    if 'keys' in st.session_state:
        selected_key = st.selectbox("Select Target", st.session_state['keys'])
        if st.button("Generate & Inject Link"):
            with st.spinner("الوحش يركز على الجودة..."):
                prompt = f"Write a 500-word expert SEO article about '{selected_key}'. MANDATORY: Include the link '{target_url}' exactly 3 times as [Expert AI Service]({target_url})."
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.3)
                st.session_state['article'] = response.choices[0].message.content

        if 'article' in st.session_state:
            st.markdown('<div class="article-box">', unsafe_allow_html=True)
            st.markdown(st.session_state['article'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # تحويل HTML نقي لـ Blogger
            html = str(st.session_state['article']).replace("## ", "<h2>").replace("\n", "<br>")
            html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', html)
            beast_copy_button(html, "Copy HTML Article 🌐")

# 3. Image Prompt (الميزة اللي رجعات)
with tab3:
    st.subheader("🖼️ Thumbnail Prompt Designer")
    if 'article' in st.session_state:
        if st.button("Create Pro Image Prompt"):
            with st.spinner("Generating..."):
                img_prompt = f"Create a DALL-E 3 prompt for an AI service thumbnail about {selected_key}. Use cinematic lighting, futuristic 3D elements, and professional style."
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_prompt}], model="llama-3.3-70b-versatile")
                st.session_state['img_p'] = res_img.choices[0].message.content
        
        if 'img_p' in st.session_state:
            st.markdown(f'<div class="prompt-box">{st.session_state["img_p"]}</div>', unsafe_allow_html=True)
            beast_copy_button(st.session_state['img_p'], "Copy Image Prompt 🎨")
