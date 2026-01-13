import streamlit as st
from groq import Groq
import requests
import re

# --- ⚙️ الإعدادات ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.set_page_config(page_title="Beast Sniper V7.5", layout="wide")

# --- 🛠️ وظيفة النسخ الذكي (JavaScript) ---
def beast_copy(text, label):
    safe_text = str(text).replace("`", "'").replace("\n", "\\n")
    btn_id = f"btn_{id(text)}"
    html = f"""
    <button id="{btn_id}" style="background-color: #00ffcc; color: black; border: none; 
    padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%;">
        {label}
    </button>
    <script>
    document.getElementById("{btn_id}").onclick = function() {{
        const el = document.createElement('textarea');
        el.value = `{safe_text}`;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
        alert('✅ Copied!');
    }};
    </script>
    """
    st.components.v1.html(html, height=60)

# --- 🎨 الستايل ---
st.markdown("<style>.stApp { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

st.title("🦁 Beast Sniper V7.5: Facebook Edition")

# Sidebar
st.sidebar.header("🚀 Target Config")
niche = st.sidebar.text_input("Niche", value="AI Strategy")
target_url = st.sidebar.text_input("Fiverr Link", value="https://www.fiverr.com/s/EgLla1d")

tab1, tab2, tab3, tab4 = st.tabs(["🔎 Keywords", "📝 Sniper Article", "🎨 Image Architect", "🎯 Facebook Sniper"])

# 1. Keywords
with tab1:
    if st.button("Hunt Keywords"):
        res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}").json()[1]
        st.session_state['keys'] = res
        st.success("Found!")

# 2. Article
with tab2:
    if 'keys' in st.session_state:
        selected_key = st.selectbox("Select Target", st.session_state['keys'])
        if st.button("Generate Article"):
            prompt = f"Write a 500-word SEO article about '{selected_key}'. Link 'Expert AI Service' to {target_url} 3 times."
            response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.3)
            st.session_state['article'] = response.choices[0].message.content
        if 'article' in st.session_state:
            st.write(st.session_state['article'])
            html = str(st.session_state['article']).replace("## ", "<h2>").replace("\n", "<br>")
            html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', html)
            beast_copy(html, "Copy HTML Article 🌐")

# 3. Image
with tab3:
    if 'article' in st.session_state:
        if st.button("Generate Image Prompt"):
            img_req = f"Masterpiece DALL-E 3 prompt for {selected_key}. Cinematic, high-tech."
            res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_req}], model="llama-3.3-70b-versatile")
            st.session_state['img_p'] = res_img.choices[0].message.content
        if 'img_p' in st.session_state:
            st.info(st.session_state['img_p'])
            beast_copy(st.session_state['img_p'], "Copy Prompt 🎨")

# 4. Facebook Sniper (الميزة الجديدة)
with tab4:
    st.subheader("🎯 Viral Social Media Hooks")
    if 'article' in st.session_state:
        if st.button("Generate FB Hooks & Tags"):
            fb_prompt = f"Based on this article: {st.session_state['article'][:300]}, write 3 viral Facebook hooks. One should be a question, one a shocking fact, and one a direct benefit. Include 5 trending hashtags."
            res_fb = client.chat.completions.create(messages=[{"role": "user", "content": fb_prompt}], model="llama-3.3-70b-versatile")
            st.session_state['fb_hooks'] = res_fb.choices[0].message.content
        if 'fb_hooks' in st.session_state:
            st.success(st.session_state['fb_hooks'])
            beast_copy(st.session_state['fb_hooks'], "Copy FB Content 🚀")
