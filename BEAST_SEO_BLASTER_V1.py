import streamlit as st
from groq import Groq
import requests
from st_copy_to_clipboard import st_copy_to_clipboard

# --- ⚙️ إعدادات الحماية والـ API ---
# حل مشكلة KeyError اللي كانت عندك فالبداية
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("⚠️ ملقيتش GROQ_API_KEY فـ Streamlit Secrets!")
except Exception as e:
    st.error(f"⚠️ خطأ فـ الإعدادات: {e}")

# تصحيح خطأ TypeError فـ set_page_config
st.set_page_config(page_title="Beast Dashboard V3.7", layout="wide")

# --- 🎨 التصميم الداكن (Dark Mode) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1c24; border-radius: 10px; color: #00ffcc; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #00ffcc !important; color: #000 !important; font-weight: bold; }
    .article-box { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 20px; border-radius: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 Beast Content Dashboard V3.7")

# --- 🕹️ لوحة التحكم الجانبية ---
st.sidebar.header("🎯 Target Setting")
niche = st.sidebar.text_input("Niche / Industry", value="AI Solutions")
# الرابط ديال الجيج ديالك اللي غايتزرع فالمقالة
target_url = st.sidebar.text_input("Your Link (Fiverr)", value="https://www.fiverr.com/s/EgLla1d")

tab1, tab2, tab3 = st.tabs(["🔎 SEO Sniper", "📝 Article Factory", "🎨 Image Prompt"])

# --- 1. قسم صيد الكلمات ---
with tab1:
    st.subheader("🎯 Keyword Opportunities")
    if st.button("Hunt Keywords"):
        with st.spinner("Searching..."):
            url = f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}"
            res = requests.get(url).json()[1]
            st.session_state['beast_keys'] = res
            # حل مشكلة "0 كلمة" بالتأكد من النتيجة
            if res:
                st.success(f"لقيت {len(res)} كلمة مفتاحية!")
            else:
                st.warning("جرب كلمة أخرى فـ Niche.")

    if 'beast_keys' in st.session_state:
        st.write(st.session_state['beast_keys'])

# --- 2. قسم المقالة وزر النسخ (تصحيح الخطأ الأخير) ---
with tab2:
    st.subheader("✍️ Article Creation")
    if 'beast_keys' in st.session_state and st.session_state['beast_keys']:
        selected_key = st.selectbox("Select Keyword", st.session_state['beast_keys'])
        if st.button("Generate Final Article"):
            with st.spinner("AI writing..."):
                prompt = f"Write a 1000-word SEO article about '{selected_key}'. Naturally include this link: {target_url}. Use H2 and H3 tags."
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                st.session_state['final_article'] = response.choices[0].message.content
        
        if 'final_article' in st.session_state:
            st.markdown('<div class="article-box">', unsafe_allow_html=True)
            st.markdown(st.session_state['final_article'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # تصحيح TypeError فـ النسخ
            # كانأكدوا بلي كانمررو النص مباشرة كـ string
            st.write("---")
            st.write("📋 **Smart Copy Options:**")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Copy as Markdown (Reddit/GitHub):")
                st_copy_to_clipboard(text=str(st.session_state['final_article']))
            
            with col2:
                # نسخة HTML بسيطة لـ Blogger
                html_article = str(st.session_state['final_article']).replace("## ", "<h2>").replace("\n", "<br>")
                st.write("Copy as HTML (Blogger):")
                st_copy_to_clipboard(text=html_article)

# --- 3. قسم برومبت الصورة ---
with tab3:
    st.subheader("🎨 Image Prompt Creator")
    if 'final_article' in st.session_state:
        if st.button("Generate Image Prompt"):
            with st.spinner("Creating prompt..."):
                img_prompt_req = f"Create a professional AI image prompt for an article about {niche}. Cinematic style, 4k."
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_prompt_req}], model="llama-3.3-70b-versatile")
                st.session_state['img_prompt'] = res_img.choices[0].message.content
        
        if 'img_prompt' in st.session_state:
            st.write(st.session_state['img_prompt'])
            st_copy_to_clipboard(text=str(st.session_state['img_prompt']))
