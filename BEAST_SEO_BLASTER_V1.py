import streamlit as st
from groq import Groq
import requests
from st_copy_to_clipboard import st_copy_to_clipboard

# --- إعدادات المحرك ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ خاصك تزيد GROQ_API_KEY فـ Streamlit Secrets!")

st.set_page_config(page_name="Beast Dashboard V3.3", layout="wide")

# --- التصميم السريالي (Dark Dashboard) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #1a1c24; border-radius: 10px 10px 0 0; padding: 0 20px; color: #00ffcc; }
    .stTabs [aria-selected="true"] { background-color: #00ffcc !important; color: #000 !important; font-weight: bold; }
    .result-box { background-color: #1a1c24; border: 1px solid #333; padding: 20px; border-radius: 12px; border-left: 5px solid #00ffcc; }
    .prompt-box { background-color: #1a1c24; border: 1px solid #ffaa00; padding: 20px; border-radius: 12px; border-left: 5px solid #ffaa00; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 Beast Content Machine Dashboard")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Configuration")
niche = st.sidebar.text_input("Niche / Industry", value="Artificial Intelligence")
target_url = st.sidebar.text_input("Link to Promote")

# --- الأقسام المنفصلة (Tabs) ---
tab1, tab2, tab3 = st.tabs(["🔎 SEO Sniper", "📝 Article Factory", "🎨 Image Prompt Creator"])

# 1. قسم صيد الكلمات
with tab1:
    st.subheader("🎯 Keyword Opportunities")
    if st.button("Hunt Low-Competition Keywords"):
        url = f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}"
        suggestions = requests.get(url).json()[1]
        st.session_state['beast_keys'] = suggestions
        st.success(f"لقيت {len(suggestions)} كلمة مفتاحية ذهبية!")
        st.write(suggestions)

# 2. قسم صناعة المقال (منفصل)
with tab2:
    st.subheader("✍️ Article Generation")
    if 'beast_keys' in st.session_state:
        selected_key = st.selectbox("اختار الكلمة المستهدفة", st.session_state['beast_keys'])
        if st.button("Generate Final Article"):
            with st.spinner("الوحش يكتب الآن..."):
                prompt = f"Write a 1000-word SEO article about '{selected_key}'. Link: {target_url}. Use H2, H3 tags."
                res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                st.session_state['final_article'] = res.choices[0].message.content
        
        if 'final_article' in st.session_state:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(st.session_state['final_article'])
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("👇 انسخ المقالة:")
            st_copy_to_clipboard(st.session_state['final_article'])

# 3. قسم صناعة برومبت الصورة (منفصل تماماً)
with tab3:
    st.subheader("🎨 AI Image Prompt Generator")
    st.info("هذا القسم كايصاوب ليك وصف احترافي لصورة المقال باش تحطو فـ Midjourney أو DALL-E.")
    
    if 'final_article' not in st.session_state:
        st.warning("⚠️ خاصك تصاوب المقال أولاً باش الـ AI يحللو ويصاوب ليه صورة مناسبة.")
    else:
        if st.button("Generate Professional Image Prompt"):
            with st.spinner("جاري تحليل المقال وتصميم البرومبت..."):
                img_prompt_req = f"""
                Based on this article summary: {st.session_state['final_article'][:500]}
                Generate a high-end, professional image prompt for AI art (DALL-E/Midjourney).
                The image should be cinematic, 4k, futuristic, and represent the topic '{niche}'.
                Only return the prompt text.
                """
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_prompt_req}], model="llama-3.3-70b-versatile")
                st.session_state['img_prompt'] = res_img.choices[0].message.content
        
        if 'img_prompt' in st.session_state:
            st.markdown("### 🖼️ Your Image Prompt:")
            st.markdown(f'<div class="prompt-box">{st.session_state["img_prompt"]}</div>', unsafe_allow_html=True)
            
            st.write("👇 انسخ برومبت الصورة:")
            st_copy_to_clipboard(st.session_state['img_prompt'])
            st.success("✅ البرومبت واجد! ديرو Paste فـ أي مولد صور بالذكاء الاصطناعي.")
