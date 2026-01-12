import streamlit as st
from groq import Groq
import requests
from st_copy_to_clipboard import st_copy_to_clipboard

# --- ⚙️ إعدادات الحماية والـ API ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"]) # حل مشكلة KeyError
except Exception:
    st.error("⚠️ ملقيتش الـ API Key! ضيف GROQ_API_KEY فـ Streamlit Secrets.")

# تصحيح خطأ TypeError: نستخدم page_title وليس page_name
st.set_page_config(page_title="Beast Dashboard V3.5", layout="wide")

# --- 🎨 تصميم الداشبورد (Dark Mode) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1c24; border-radius: 10px; color: #00ffcc; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #00ffcc !important; color: #000 !important; font-weight: bold; }
    .article-box { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 20px; border-radius: 10px; color: white; }
    .prompt-box { background-color: #1a1c24; border-left: 5px solid #ffaa00; padding: 20px; border-radius: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 Beast Content Machine Dashboard")

# --- 🕹️ لوحة التحكم الجانبية ---
st.sidebar.header("🎯 Target Setting")
niche = st.sidebar.text_input("Niche / Industry", value="Technology")
target_url = st.sidebar.text_input("Link to Promote")

# --- 📑 الأقسام المنظمة فـ Tabs منفصلة ---
tab1, tab2, tab3 = st.tabs(["🔎 SEO Sniper", "📝 Article Factory", "🎨 Image Prompt Architect"])

# --- 1. قسم صيد الكلمات ---
with tab1:
    st.subheader("🎯 Keyword Opportunities")
    if st.button("Hunt Keywords"):
        with st.spinner("Searching..."):
            url = f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}"
            res = requests.get(url).json()[1]
            st.session_state['beast_keys'] = res
            st.success(f"لقيت {len(res)} كلمة مفتاحية!")
    
    if 'beast_keys' in st.session_state:
        st.write(st.session_state['beast_keys'])

# --- 2. قسم المقالة وزر النسخ ---
with tab2:
    st.subheader("✍️ Article Factory")
    if 'beast_keys' in st.session_state:
        selected_key = st.selectbox("Select Keyword", st.session_state['beast_keys'])
        if st.button("Generate Final Article"):
            with st.spinner("الوحش يكتب الآن..."):
                prompt = f"Write a professional SEO article about '{selected_key}'. Naturally promote: {target_url}. Use H2, H3 tags."
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                st.session_state['final_article'] = response.choices[0].message.content
        
        if 'final_article' in st.session_state:
            st.markdown('<div class="article-box">', unsafe_allow_html=True)
            st.markdown(st.session_state['final_article'])
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("👇 Copy Article Content:")
            st_copy_to_clipboard(st.session_state['final_article'])

# --- 3. قسم برومبت الصورة (منفصل تماماً) ---
with tab3:
    st.subheader("🎨 Image Prompt Architect")
    st.info("هنا كايصاوب ليك AI وصف للصورة اللي كاتناسب المقال ديالك.")
    if 'final_article' not in st.session_state:
        st.warning("⚠️ صاوب المقال أولاً باش الوحش يحللو ويصاوب ليك صورة مطابقة.")
    else:
        if st.button("Generate Image Prompt"):
            with st.spinner("Analyzing visuals..."):
                prompt_req = f"Based on this article: {st.session_state['final_article'][:400]}. Create a professional image prompt for AI (Midjourney/DALL-E). Focus on {niche} style."
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": prompt_req}], model="llama-3.3-70b-versatile")
                st.session_state['img_prompt'] = res_img.choices[0].message.content
        
        if 'img_prompt' in st.session_state:
            st.markdown('<div class="prompt-box">', unsafe_allow_html=True)
            st.write(st.session_state['img_prompt'])
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("👇 Copy Prompt:")
            st_copy_to_clipboard(st.session_state['img_prompt'])
