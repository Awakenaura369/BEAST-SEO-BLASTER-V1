import streamlit as st
from groq import Groq
import requests

# --- إعدادات المحرك ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ خاصك تزيد GROQ_API_KEY فـ Streamlit Secrets!")

st.set_page_config(page_title="BEAST MAGNET V3.1", layout="wide")

# تصميم "الوحش"
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; }
    .stButton>button { background: linear-gradient(45deg, #ffd700, #b8860b); color: black; font-weight: bold; border-radius: 10px; }
    .copy-box { background-color: #111; border: 1px solid #00ffcc; padding: 15px; border-radius: 10px; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧲 Beast Magnet V3.1 (Manual & Auto Mode)")

# --- Sidebar ---
st.sidebar.header("🎯 Target Config")
niche = st.sidebar.text_input("Niche", value="Digital Marketing")
target_url = st.sidebar.text_input("Link to Promote")

tabs = st.tabs(["🔎 SEO Sniper", "✍️ Content Factory & Copy"])

# 1. صيد الكلمات
with tabs[0]:
    if st.button("Hunt Keywords"):
        url = f"http://suggestqueries.google.com/complete/search?output=firefox&q={niche}"
        suggestions = requests.get(url).json()[1]
        st.session_state['beast_keys'] = suggestions
        st.success("Found High-Traffic keywords!")
        st.write(suggestions)

# 2. صناعة المحتوى مع زر الكوبي
with tabs[1]:
    if 'beast_keys' in st.session_state:
        selected_key = st.selectbox("Select Keyword", st.session_state['beast_keys'])
        
        if st.button("Generate Article"):
            with st.spinner("AI is crafting..."):
                prompt = f"Write a 1000-word SEO article about '{selected_key}'. Target Link: {target_url}. Use HTML tags like <h2>, <h3> and <b>."
                res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                st.session_state['final_article'] = res.choices[0].message.content
        
        if 'final_article' in st.session_state:
            st.markdown("### 📝 المقالة الواجدة:")
            st.markdown(f'<div class="copy-box">{st.session_state["final_article"]}</div>', unsafe_allow_html=True)
            
            # --- زر الكوبي السحري ---
            content_to_copy = st.session_state['final_article'].replace("'", "\\'").replace("\n", "\\n")
            copy_button_html = f"""
            <button onclick="copyToClipboard()" style="margin-top:10px; background-color:#00ffcc; color:black; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">
                📋 Copy Full Article
            </button>

            <script>
            function copyToClipboard() {{
                const text = `{content_to_copy}`;
                navigator.clipboard.writeText(text).then(function() {{
                    alert('✅ المقالة تكوبات! دبا حطها (Paste) فين ما بغيتي.');
                }}, function(err) {{
                    console.error('Could not copy text: ', err);
                }});
            }}
            </script>
            """
            st.components.v1.html(copy_button_html, height=70)
            
            st.info("💡 نصيحة: فاش تكوبي المقالة، حطها فـ Blogger فـ وضع 'HTML View' باش يبقاو العناوين (H2, H3) مقادين.")
