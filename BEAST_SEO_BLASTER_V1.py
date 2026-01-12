import streamlit as st
from groq import Groq
import requests
from st_copy_to_clipboard import st_copy_to_clipboard

# --- ⚙️ إعدادات الحماية والـ API ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ ملقيتش الـ API Key! ضيف GROQ_API_KEY فـ Streamlit Secrets.")

# إعداد الصفحة (تصحيح page_title)
st.set_page_config(page_title="Beast Dashboard V3.6", layout="wide")

# --- 🎨 تصميم الداشبورد الاحترافي (Dark & Neon) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1c24; border-radius: 10px; color: #00ffcc; padding: 10px 20px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #00ffcc !important; color: #000 !important; }
    .article-box { background-color: #1a1c24; border-left: 5px solid #00ffcc; padding: 25px; border-radius: 12px; color: #e0e0e0; line-height: 1.6; }
    .prompt-box { background-color: #1a1c24; border-left: 5px solid #ffaa00; padding: 20px; border-radius: 12px; color: #ffd700; font-style: italic; }
    .copy-section { background: #262730; padding: 15px; border-radius: 10px; border: 1px dashed #444; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 Beast Content & SEO Machine")

# --- 🕹️ لوحة التحكم الجانبية ---
st.sidebar.header("🎯 Target & Links")
niche_input = st.sidebar.text_input("Niche / Industry", value="AI Solutions")
target_link = st.sidebar.text_input("Your Affiliate/Gig Link", value="https://www.fiverr.com/s/EgLla1d")
st.sidebar.info("هاد الرابط غيتزرع أوتوماتيكياً وسط المقال.")

# --- 📑 الأقسام المنظمة ---
tab1, tab2, tab3 = st.tabs(["🔎 SEO Sniper", "📝 Article Factory", "🎨 Image Architect"])

# --- 1. قسم صيد الكلمات ---
with tab1:
    st.subheader("🎯 Keyword Opportunity Hunter")
    if st.button("Hunt Hot Keywords"):
        with st.spinner("Searching Google Suggest..."):
            url = f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche_input}"
            res = requests.get(url).json()[1]
            st.session_state['beast_keys'] = res
            st.success(f"Found {len(res)} keywords for {niche_input}!")
    
    if 'beast_keys' in st.session_state:
        st.write("Keywords found:", st.session_state['beast_keys'])

# --- 2. قسم المقالة (مع حل مشكل الروابط) ---
with tab2:
    st.subheader("✍️ Article Generation (With Backlinks)")
    if 'beast_keys' in st.session_state:
        selected_key = st.selectbox("Select Target Keyword", st.session_state['beast_keys'])
        
        if st.button("Generate Final Article"):
            with st.spinner("AI is crafting your SEO masterpiece..."):
                prompt = f"""
                Write a professional 1000-word SEO article about '{selected_key}'. 
                Naturally integrate this exact link as the best solution: {target_link}. 
                Use Markdown formatting: ## for H2, ### for H3, and **bold** for emphasis. 
                Ensure the link is clickable in Markdown format like this: [Fiverr]({target_link}).
                """
                response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                st.session_state['final_article'] = response.choices[0].message.content

        if 'final_article' in st.session_state:
            st.markdown('<div class="article-box">', unsafe_allow_html=True)
            st.markdown(st.session_state['final_article'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # --- خيارات النسخ الذكي (لضمان بقاء الروابط) ---
            st.markdown('<div class="copy-section">', unsafe_allow_html=True)
            st.write("📋 **Smart Copy Options:**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("لـ Reddit و Github (Markdown):")
                st_copy_to_clipboard(st.session_state['final_article'], before_text="Copy Markdown 🔗")
            
            with col2:
                # تحويل بسيط لـ HTML لضمان النشر فـ Blogger بروابط شغالة
                html_version = st.session_state['final_article'].replace("## ", "<h2>").replace("### ", "<h3>").replace("\n", "<br>")
                # زر نسخ بصيغة HTML
                st.write("لـ Blogger و WordPress (HTML):")
                st_copy_to_clipboard(html_version, before_text="Copy HTML Code 🌐")
            st.markdown('</div>', unsafe_allow_html=True)

# --- 3. قسم برومبت الصورة (منفصل) ---
with tab3:
    st.subheader("🎨 Image Prompt Architect")
    if 'final_article' not in st.session_state:
        st.warning("⚠️ صاوب المقال أولاً باش الوحش يحللو ويصاوب ليه صورة مطابقة.")
    else:
        if st.button("Generate Image Prompt"):
            with st.spinner("Analyzing visuals..."):
                img_req = f"Based on this article: {st.session_state['final_article'][:500]}. Create a professional image prompt for DALL-E 3. High resolution, futuristic, {niche_input} style."
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_req}], model="llama-3.3-70b-versatile")
                st.session_state['img_prompt'] = res_img.choices[0].message.content
        
        if 'img_prompt' in st.session_state:
            st.markdown('<div class="prompt-box">', unsafe_allow_html=True)
            st.write(st.session_state['img_prompt'])
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("👇 Copy Image Prompt:")
            st_copy_to_clipboard(st.session_state['img_prompt'])
