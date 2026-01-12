import streamlit as st
from groq import Groq
import requests
import re
from st_copy_to_clipboard import st_copy_to_clipboard

# --- ⚙️ الإعدادات (Groq Engine) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ خاصك تزيد GROQ_API_KEY فـ Streamlit Secrets!")

st.set_page_config(page_title="Beast Dashboard V5.1", layout="wide")

# --- 🎨 مظهر الداشبورد الاحترافي ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .article-output { background-color: white; color: black; padding: 30px; border-radius: 10px; line-height: 1.8; font-family: sans-serif; }
    .prompt-box { background-color: #1a1c24; border: 1px dashed #ffaa00; padding: 20px; border-radius: 10px; color: #ffd700; font-family: monospace; }
    .stTabs [data-baseweb="tab"] { color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 Beast V5.1: The Final Weapon")

# Sidebar
st.sidebar.header("⚙️ Target Config")
niche = st.sidebar.text_input("Niche", value="AI Solutions")
target_url = st.sidebar.text_input("Fiverr Link", value="https://www.fiverr.com/s/EgLla1d")

tab1, tab2, tab3 = st.tabs(["🔎 SEO Sniper", "📝 Sniper Article", "🎨 Image Architect"])

# --- 1. Keywords Sniper ---
with tab1:
    if st.button("Hunt Keywords"):
        res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}").json()[1]
        st.session_state['keys'] = res
        if res:
            st.success(f"لقيت {len(res)} كلمة مفتاحية!")
    if 'keys' in st.session_state:
        st.write(st.session_state['keys'])

# --- 2. Sniper Article (500 كلمة مع روابط مزروعة) ---
with tab2:
    if 'keys' in st.session_state:
        selected_key = st.selectbox("Select Target", st.session_state['keys'])
        if st.button("Generate Sniper Article"):
            with st.spinner("Writing & Injecting..."):
                prompt = f"Write a professional 500-word SEO article about '{selected_key}'. MANDATORY: Hyperlink the text 'this expert service' and 'Hire on Fiverr' to: {target_url} using Markdown [Text](URL). Use ## for headers."
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.4)
                st.session_state['article'] = response.choices[0].message.content

        if 'article' in st.session_state:
            st.markdown('<div class="article-output">', unsafe_allow_html=True)
            st.markdown(st.session_state['article'])
            st.markdown('</div>', unsafe_allow_html=True)

            # تحويل HTML احترافي للنسخ (حل مشكلة الروابط فـ Blogger)
            html = str(st.session_state['article']).replace("## ", "<h2 style='color:#d32f2f;'>").replace("\n", "<br>")
            html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" style="color:#1976d2; font-weight:bold;">\1</a>', html)
            
            st.write("---")
            # حل مشكلة TypeError بضمان تمرير النص كـ string
            st_copy_to_clipboard(text=str(html), before_text="Copy HTML Code for Blogger 🌐")

# --- 3. Image Architect (رجوع ميزة الصور) ---
with tab3:
    st.subheader("🎨 Image Prompt Creator")
    if 'article' in st.session_state:
        if st.button("Generate Thumbnail Prompt"):
            with st.spinner("Analyzing content..."):
                img_req = f"Based on this article summary: {st.session_state['article'][:300]}. Generate a high-end DALL-E 3 image prompt. Style: Professional, cinematic, futuristic {niche}."
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_req}], model="llama-3.3-70b-versatile")
                st.session_state['img_p'] = res_img.choices[0].message.content
        
        if 'img_p' in st.session_state:
            st.markdown(f'<div class="prompt-box">{st.session_state["img_p"]}</div>', unsafe_allow_html=True)
            # زر نسخ برومبت الصورة بلا أخطاء
            st_copy_to_clipboard(text=str(st.session_state['img_p']), before_text="Copy Image Prompt 🎨")
    else:
        st.warning("⚠️ صاوب المقالة أولاً فـ Tab 2.")
