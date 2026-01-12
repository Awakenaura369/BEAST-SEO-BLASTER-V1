import streamlit as st
from groq import Groq
import requests
from st_copy_to_clipboard import st_copy_to_clipboard

# --- ⚙️ الإعدادات الأساسية (Groq Engine) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ خاصك تزيد GROQ_API_KEY فـ Streamlit Secrets!")

# إعداد الصفحة (V4.6 Sniper Edition)
st.set_page_config(page_title="Beast Sniper V4.6", layout="wide")

# --- 🎨 تصميم الـ UI السريالي (Clean Sniper Style) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    /* مظهر المقالة المختصرة والاحترافية */
    .article-container {
        background-color: #ffffff;
        color: #1a1a1a;
        padding: 40px;
        border-radius: 12px;
        border-left: 10px solid #00ffcc;
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .article-container h2 { color: #004a99; font-weight: bold; margin-top: 20px; }
    .article-container a { color: #3498db; font-weight: bold; text-decoration: underline; }
    .stTabs [data-baseweb="tab"] { color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Beast Sniper V4.6: Quality Mode")

# --- 🕹️ لوحة التحكم الجانبية ---
st.sidebar.header("🚀 Sniper Config")
niche = st.sidebar.text_input("Niche", value="AI Business Solutions")
target_url = st.sidebar.text_input("Fiverr/Affiliate Link", value="https://www.fiverr.com/s/EgLla1d")
st.sidebar.markdown("---")
st.sidebar.write("💡 هدفنا: 500 كلمة عالية القيمة مع روابط فعالة.")

# --- 📑 الأقسام ---
tab1, tab2, tab3 = st.tabs(["🔎 SEO Sniper", "✍️ Sniper Content", "🎨 Image Architect"])

# 1. قسم صيد الكلمات
with tab1:
    st.subheader("🎯 Target Keyword Discovery")
    if st.button("Hunt Keywords"):
        with st.spinner("Searching..."):
            res = requests.get(f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}").json()[1]
            st.session_state['keys'] = res
            st.success(f"لقيت {len(res)} كلمة مفتاحية!")
    
    if 'keys' in st.session_state:
        st.write(st.session_state['keys'])

# 2. صناعة المحتوى (Sniper 500 Words)
with tab2:
    st.subheader("📝 Sniper Article Factory")
    if 'keys' in st.session_state:
        selected_key = st.selectbox("Select Target", st.session_state['keys'])
        
        if st.button("Generate High-Value Article"):
            with st.spinner("الوحش يركز على الجودة..."):
                # برومبت Sniper: يركز على القيمة، الاختصار، والروابط
                prompt = f"""
                Write a HIGH-IMPACT SEO article about '{selected_key}'. 
                MAX LENGTH: 500 words. 
                STRICT RULE: You MUST include this link: {target_url} exactly 3 times.
                - 1st time: In the introduction.
                - 2nd time: Mid-article using anchor text like "this specialized AI service".
                - 3rd time: In the final Call to Action.
                
                TONE: Authoritative, professional, and helpful. 
                FORMAT: Use ## for H2, bullet points for key benefits. Use Markdown [Fiverr]({target_url}).
                """
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.6 # تركيز عالي لمنع الحشو
                )
                st.session_state['article'] = response.choices[0].message.content

        if 'article' in st.session_state:
            # عرض المقالة (Preview)
            st.markdown('<div class="article-container">', unsafe_allow_html=True)
            st.markdown(st.session_state['article'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # خيارات النسخ الذكي
            st.write("---")
            st.markdown("### 📋 Copy & Post Options:")
            col1, col2 = st.columns(2)
            with col1:
                st.info("Copy for Reddit/Markdown")
                st_copy_to_clipboard(text=str(st.session_state['article']))
            
            with col2:
                # تحويل HTML احترافي لـ Blogger
                html_sniper = f"""
                <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                {st.session_state['article'].replace('## ', '<h2>').replace('### ', '<h3>').replace('\n', '<br>')}
                </div>
                """
                st.success("Copy for Blogger (HTML Mode)")
                st_copy_to_clipboard(text=html_sniper)

# 3. قسم برومبت الصورة
with tab3:
    st.subheader("🎨 Thumbnail Prompt Architect")
    if 'article' in st.session_state:
        if st.button("Generate Image Prompt"):
            with st.spinner("Analyzing content..."):
                img_prompt_req = f"Create a professional DALL-E 3 prompt for an article about {selected_key}. Cinematic, clean, tech style."
                res_img = client.chat.completions.create(messages=[{"role": "user", "content": img_prompt_req}], model="llama-3.3-70b-versatile")
                st.session_state['img_p'] = res_img.choices[0].message.content
        
        if 'img_p' in st.session_state:
            st.code(st.session_state['img_p'])
            st_copy_to_clipboard(text=str(st.session_state['img_p']))
