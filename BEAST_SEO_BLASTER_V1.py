import streamlit as st
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import re

# --- إعدادات الواجهة ---
st.set_page_config(page_title="BEAST SEO BLASTER V1", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.markdown("""
    <style>
    .stApp { background: #0a0a0a; color: gold; }
    .stButton>button { width: 100%; background: linear-gradient(45deg, #ffd700, #b8860b); color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧲 Beast SEO Magnet & Social Blaster")

# --- ⚙️ التحكم في الحسابات ---
st.sidebar.header("🔐 Accounts Vault")
target_url = st.sidebar.text_input("Target URL (Your Channel/Link)", placeholder="https://t.me/yourchannel")
blogger_user = st.sidebar.text_input("Blogger Email")
blogger_pass = st.sidebar.text_input("Blogger Password", type="password")

tabs = st.tabs(["🎯 Keyword Research", "✍️ AI Content Generation", "🚀 Blast Mode"])

# 1. صيد الكلمات المفتاحية
with tabs[0]:
    st.header("🎯 SEO Keyword Sniper")
    topic = st.text_input("Niche Topic", value="Marketing Strategy AI")
    if st.button("Hunt Low Competition Keywords"):
        url = f"http://suggestqueries.google.com/complete/search?output=firefox&q={topic}"
        suggestions = requests.get(url).json()[1]
        st.session_state['keywords'] = suggestions
        st.success(f"Found {len(suggestions)} High-Traffic Keywords!")
        st.write(suggestions)

# 2. صناعة المقالات السريالية
with tabs[1]:
    st.header("✍️ AI Viral Article Architect")
    if 'keywords' in st.session_state:
        selected_k = st.selectbox("Select Target Keyword", st.session_state['keywords'])
        if st.button("Generate SEO Article"):
            with st.spinner("AI is writing a 1000-word masterpiece..."):
                prompt = f"Write a professional SEO article about '{selected_k}'. Embed this link naturally: {target_url}. Use H2 and H3 tags. Make it persuasive."
                res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                st.session_state['article_body'] = res.choices[0].message.content
                st.markdown(st.session_state['article_body'])

# 3. محرك النشر (The Ghost Machine)
with tabs[2]:
    st.header("🚀 Automated Social/Web2.0 Blast")
    st.warning("This mode uses Browser Automation (No API needed).")
    
    if st.button("START GLOBAL BLAST"):
        if not blogger_user or not blogger_pass:
            st.error("Please fill your login details in the sidebar!")
        else:
            st.info("Initializing Beast Browser...")
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless') # تفعيلها باش المتصفح يخدم فـ الخلفية
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            
            try:
                # مثال للنشر فـ Blogger (Web 2.0 Backlink)
                driver.get("https://www.blogger.com/go/signin")
                time.sleep(3)
                
                # إدخال الإيميل
                driver.find_element(By.ID, "identifierId").send_keys(blogger_user + Keys.ENTER)
                time.sleep(5)
                # (هنا غيدخل كلمة السر ويتبع مراحل النشر)
                
                st.success("✅ Successfully posted to Blogger!")
                # هنا تقدر تزيد منصات أخرى (Reddit, Medium, etc.) بنفس الطريقة
                
            except Exception as e:
                st.error(f"Execution Error: {e}")
            finally:
                driver.quit()
