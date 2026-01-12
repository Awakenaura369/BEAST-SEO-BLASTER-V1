import streamlit as st
from groq import Groq
import requests
from st_copy_to_clipboard import st_copy_to_clipboard

# --- ⚙️ إعدادات الحماية والـ API ---
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("⚠️ ملقيتش GROQ_API_KEY فـ Streamlit Secrets!")
except Exception as e:
    st.error(f"⚠️ خطأ فـ الإعدادات: {e}")

# إعداد الصفحة
st.set_page_config(page_title="Beast Dashboard V3.8", layout="wide")

# --- 🎨 تصميم الداشبورد ومظهر المقالة (The Beast UI) ---
st.markdown("""
    <style>
    /* مظهر الصفحة العام */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* تصميم الـ Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1c24; border-radius: 10px; color: #00ffcc; padding: 10px 20px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #00ffcc !important; color: #000 !important; }
    
    /* مظهر المقالة الاحترافي (لحل مشكلة "النتيجة العيانة") */
    .article-output {
        background-color: #ffffff;
        color: #1a1a1a;
        padding: 35px;
        border-radius: 15px;
        border-left: 10px solid #00ffcc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.8;
        margin-top: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    .article-output h2 { color: #1a1a1a; border-bottom: 2px solid #00ffcc; padding-bottom: 5px; margin-top: 25px; }
    .article-output h3 { color: #2c3e50; margin-top: 20px; }
    .article-output a { color: #007bff; font-weight: bold; text-decoration: underline; }
    
    /* مظهر برومبت الصورة */
    .prompt-box { background-color: #1a1c24; border: 1px dashed #ffaa00; padding: 20px; border-radius: 10px; color: #ffd700; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 Beast Content Machine V3.8")

# --- 🕹️ لوحة التحكم الجانبية (Sidebar) ---
st.sidebar.header("🎯 Target & Link Settings")
niche = st.sidebar.text_input("Niche / Industry", value="AI Solutions")
target_url = st.sidebar.text_input("Link to Promote (Fiverr/Affiliate)", value="https://www.fiverr.com/s/EgLla1d")
st.sidebar.markdown("---")
st.sidebar.write("💡 هاد الرابط غيتزرع فالمقالة أوتوماتيكياً.")

# --- 📑 الأقسام المنظمة ---
tab1, tab2, tab3 = st.tabs(["🔎 SEO Sniper", "📝 Article Factory", "🎨 Image Architect"])

# --- 1. قسم صيد الكلمات ---
with tab1:
    st.subheader("🎯 Keyword Opportunity Hunter")
    if st.button("Hunt Hot Keywords"):
        with st.spinner("Searching Google Suggest..."):
            url = f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}"
            res = requests.get(url).json()[1]
            st.session_state['beast_keys'] = res
            if res:
                st.success(f"لقيت {len(res)} كلمة مفتاحية ذهبية لـ {niche}!")
            else:
                st.warning("جرب كلمة أخرى.")

    if 'beast_keys' in st.session_state:
        st.write("Keywords Found:", st.session_state['beast_keys'])

# --- 2. قسم المقالة (التصحيح الشامل للمظهر والنسخ) ---
with tab2:
    st.subheader("✍️ Content Generation")
    if 'beast_keys' in st.session_state and st.session_state['beast_keys']:
        selected_key = st.selectbox("Select Target Keyword", st.session_state['beast_keys'])
        
        if st.button("Generate Professional Article"):
            with st.spinner("الوحش يكتب الآن..."):
                prompt = f"""
                Write a 1000-word professional SEO article about '{selected_key}'. 
                Use a professional business tone.
                Naturally include this link as the ultimate solution: {target_url}. 
                Format: Use ## for main headings (H2), ### for subheadings (H3). 
                Make the link clickable in Markdown like this: [Fiverr]({target_url}).
                """
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                st.session_state['final_article'] = response.choices[0].message.content

        if 'final_article' in st.session_state:
            # عرض المقالة بمظهر احترافي (Preview)
            st.markdown('<div class="article-output">', unsafe_allow_html=True)
            st.markdown(st.session_state['final_article'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # --- أزرار النسخ الذكي (حل مشكلة الروابط و TypeError) ---
            st.write("---")
            st.markdown("### 📋 Copy Options (Choose Your Platform):")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("Option 1: Copy for Reddit / Markdown")
                # تحويل النص لـ string لضمان عدم وقوع TypeError
                st_copy_to_clipboard(str(st.session_state['final_article']))
            
            with col2:
                st.success("Option 2: Copy for Blogger / WordPress (HTML)")
                # تحويل Markdown لـ HTML بسيط لضمان بقاء الروابط والعناوين فـ Blogger
                html_ready = str(st.session_state['final_article']).replace("## ", "<h2>").replace("### ", "<h3>").replace("\n", "<br>")
                st_copy_to_clipboard(html_ready)

# --- 3. قسم برومبت الصورة ---
with tab3:
    st.subheader("🎨 AI Image Prompt Creator")
    if 'final_article' in st.session_state:
        if st.button("Generate Pro Image Prompt"):
            with st.spinner("Analyzing content for visuals..."):
                img_prompt_req = f"Based on this article summary: {st.session_state['final_article'][:400]}. Generate a high-end image prompt for DALL-E 3 or Midjourney. Style: Professional, 4k, futuristic {niche}."
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_prompt_req}], model="llama-3.3-70b-versatile")
                st.session_state['img_prompt'] = res_img.choices[0].message.content
        
        if 'img_prompt' in st.session_state:
            st.markdown("### 🖼️ Your Image Prompt:")
            st.markdown(f'<div class="prompt-box">{st.session_state["img_prompt"]}</div>', unsafe_allow_html=True)
            st.write("👇 Copy Prompt:")
            st_copy_to_clipboard(str(st.session_state['img_prompt']))
