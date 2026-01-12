import streamlit as st
from groq import Groq
import requests
import re
from st_copy_to_clipboard import st_copy_to_clipboard

# --- ⚙️ المحرك (Groq Cloud) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ خاصك تزيد GROQ_API_KEY فـ Streamlit Secrets!")

# إعداد الصفحة
st.set_page_config(page_title="Beast Sniper V4.8", layout="wide")

# --- 🎨 تصميم الداشبورد الاحترافي ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .article-output {
        background-color: #ffffff;
        color: #1a1a1a;
        padding: 30px;
        border-radius: 12px;
        line-height: 1.8;
        font-family: 'Segoe UI', sans-serif;
        border-left: 8px solid #00ffcc;
    }
    .stTabs [data-baseweb="tab"] { color: #00ffcc; font-weight: bold; }
    code { color: #ffaa00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Beast Sniper V4.8: The Final Weapon")

# --- 🕹️ لوحة التحكم ---
st.sidebar.header("🚀 Sniper Config")
niche = st.sidebar.text_input("Niche", value="AI Solutions")
target_url = st.sidebar.text_input("Fiverr Link", value="https://www.fiverr.com/s/EgLla1d")

tab1, tab2 = st.tabs(["🔎 Keyword Sniper", "📝 Content Factory"])

# 1. قسم صيد الكلمات
with tab1:
    if st.button("Hunt Keywords"):
        res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}").json()[1]
        st.session_state['beast_keys'] = res
        st.success(f"لقيت {len(res)} هدف!")
    
    if 'beast_keys' in st.session_state:
        st.write(st.session_state['beast_keys'])

# 2. قسم صناعة المحتوى (الزرع والنسخ)
with tab2:
    if 'beast_keys' in st.session_state:
        selected_key = st.selectbox("Select Target Keyword", st.session_state['beast_keys'])
        
        if st.button("Generate & Inject Link"):
            with st.spinner("الوحش يصطاد ويحقن الروابط..."):
                # برومبت صارم جداً لضمان زرع الرابط
                prompt = f"""
                Write a 500-word high-value SEO article about '{selected_key}'.
                MANDATORY: You MUST include the link '{target_url}' exactly 3 times.
                - Placement 1: In the first paragraph as [Get Expert Help Here]({target_url}).
                - Placement 2: Mid-article as [this professional AI solution]({target_url}).
                - Placement 3: In the CTA at the end as [Hire on Fiverr]({target_url}).
                
                Format: Use ## for H2 headers. Bullet points for benefits.
                Tone: Professional and persuasive.
                """
                
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.3 # تركيز مطلق على التعليمات
                )
                st.session_state['final_article'] = response.choices[0].message.content

        if 'final_article' in st.session_state:
            # عرض المعاينة
            st.markdown("### 📝 Preview:")
            st.markdown('<div class="article-output">', unsafe_allow_html=True)
            st.markdown(st.session_state['final_article'])
            st.markdown('</div>', unsafe_allow_html=True)

            # --- معالجة النص للنسخ (السحر التقني) ---
            raw_text = str(st.session_state['final_article'])
            # تحويل Markdown لـ HTML
            html_version = raw_text.replace("## ", "<h2>").replace("\n", "<br>")
            # تحويل روابط Markdown [Text](URL) لروابط HTML حقيقية <a href='URL'>
            html_with_links = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" style="color: #007bff; font-weight: bold;">\1</a>', html_version)
            
            st.write("---")
            st.subheader("📋 خيارات النسخ الذكي:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("1. نسخ لـ Reddit (Markdown)")
                st_copy_to_clipboard(text=raw_text, before_text="Copy Markdown 🔗")
            
            with col2:
                st.success("2. نسخ لـ Blogger (HTML Mode)")
                st_copy_to_clipboard(text=html_with_links, before_text="Copy HTML Code 🌐")
            
            st.warning("⚠️ نصيحة: فـ Blogger، استعمل وضع 'HTML View' ودير Paste باش الروابط يخدمو.")
