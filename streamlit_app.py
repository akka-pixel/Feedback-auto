import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from random import randint
import time

# Page configuration - Bunker Style
st.set_page_config(
    page_title="Feedback Automation - PSG Tech",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Bunker-Style CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Bunker Purple Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0c 0%, #1a0a1f 50%, #0a0a0c 100%);
        background-attachment: fixed;
    }
    
    /* Aurora Blobs (Bunker Style) */
    .stApp::before {
        content: "";
        position: fixed;
        top: -50%;
        left: -20%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
        animation: float 25s infinite alternate;
        pointer-events: none;
        z-index: 0;
    }
    
    .stApp::after {
        content: "";
        position: fixed;
        bottom: -50%;
        right: -20%;
        width: 120%;
        height: 120%;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.12) 0%, transparent 70%);
        animation: float 25s infinite alternate-reverse;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(30px, -30px) scale(1.1); }
    }
    
    /* Main Content - Glass Panel */
    .main .block-container {
        position: relative;
        z-index: 10;
        background: rgba(18, 18, 24, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 32px;
        padding: 2.5rem 2rem;
        backdrop-filter: blur(15px) saturate(140%);
        -webkit-backdrop-filter: blur(15px) saturate(140%);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
        max-width: 480px;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Header - Bunker Glow Effect */
    h1 {
        color: #ffffff;
        font-weight: 800;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em;
        filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.4));
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.4);
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 2rem;
    }
    
    /* Input Labels - Bunker Style */
    .stTextInput label, .stSelectbox label {
        color: rgba(255, 255, 255, 0.6) !important;
        font-weight: 600 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem !important;
    }
    
    /* Glass Inputs */
    .stTextInput input, .stSelectbox select {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 18px !important;
        padding: 1rem 1.25rem !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1, 0 0 30px rgba(99, 102, 241, 0.2) !important;
        outline: none !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.3);
    }
    
    /* Button - Liquid Gradient */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 1rem 2rem !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4) !important;
        letter-spacing: 0.02em;
    }
    
    .stButton button:hover:not(:disabled) {
        transform: scale(1.02);
        box-shadow: 0 15px 35px rgba(99, 102, 241, 0.5) !important;
        filter: brightness(1.1);
    }
    
    .stButton button:active:not(:disabled) {
        transform: scale(0.98);
    }
    
    .stButton button:disabled {
        background: rgba(100, 100, 110, 0.3) !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        opacity: 0.5;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 10px;
    }
    
    .stProgress > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        color: #6ee7b7 !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        color: #fca5a5 !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Info Card */
    .info-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1rem;
        margin-top: 2rem;
        text-align: center;
    }
    
    .info-text {
        color: rgba(255, 255, 255, 0.4);
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }
    
    /* Status Pill Animation */
    @keyframes pulse-ring {
        0% { transform: scale(0.95); opacity: 0.8; box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
        70% { transform: scale(1); opacity: 1; box-shadow: 0 0 0 6px rgba(99, 102, 241, 0); }
        100% { transform: scale(0.95); opacity: 0.8; box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
    }
    
    .status-pill {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 99px;
        padding: 0.75rem 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        margin: 1rem auto;
        width: fit-content;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        animation: pulse-ring 2s infinite;
    }
    
    .status-icon {
        font-size: 1.25rem;
    }
    
    .status-text {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.05em;
        background: linear-gradient(90deg, #fff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Section Headers */
    h3 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.01em;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>Feedback.</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>PSG Tech Automation</p>", unsafe_allow_html=True)

# Spacer
st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Input Section
st.markdown("### Enter Details")

rollno = st.text_input(
    "Roll Number",
    placeholder="e.g., 23z309",
    help="Your PSG Tech roll number"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter password",
    help="Your eCampus password"
)

feedback_type = st.selectbox(
    "Feedback Type",
    options=[("End Semester Feedback", 0), ("Intermediate Feedback", 1)],
    format_func=lambda x: x[0]
)

# Terms & Conditions - Bunker Style
st.markdown("<div style='margin: 1.5rem 0 0.5rem 0;'></div>", unsafe_allow_html=True)

with st.expander("📜 Terms & Conditions", expanded=False):
    st.markdown("""
    <div style='color: rgba(255,255,255,0.7); font-size: 13px; line-height: 1.6;'>
        <p style='font-weight: 600; color: rgba(255,255,255,0.9); margin-bottom: 0.75rem;'>Educational Use Policy</p>
        <p style='margin-bottom: 0.5rem;'>This tool is designed strictly for educational purposes to help students understand automation concepts.</p>
        
        <p style='font-weight: 600; color: rgba(255,255,255,0.9); margin: 1rem 0 0.5rem 0;'>Your Responsibility</p>
        <ul style='margin: 0; padding-left: 1.25rem;'>
            <li style='margin-bottom: 0.35rem;'>Use this tool responsibly and ethically</li>
            <li style='margin-bottom: 0.35rem;'>Ensure compliance with PSG Tech's policies</li>
            <li style='margin-bottom: 0.35rem;'>Your credentials are processed securely and not stored</li>
            <li style='margin-bottom: 0.35rem;'>You are solely responsible for your usage</li>
        </ul>
        
        <p style='font-weight: 600; color: rgba(255,255,255,0.9); margin: 1rem 0 0.5rem 0;'>Privacy & Security</p>
        <p style='margin-bottom: 0.5rem;'>• No data is stored or logged<br>
        • Credentials are used only for automation<br>
        • Session ends immediately after completion</p>
        
        <p style='margin-top: 1rem; padding: 0.75rem; background: rgba(99, 102, 241, 0.1); border-radius: 12px; border-left: 3px solid #6366f1; font-size: 12px;'>
        <strong>⚠️ Disclaimer:</strong> By using this tool, you acknowledge that you understand and accept these terms. The developers are not responsible for any misuse or consequences.
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_driver():
    """Sets up Selenium WebDriver for Streamlit Cloud (uses Chromium)."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium"
    
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def intermediate_form(browser, progress_bar, status_text):
    wait = WebDriverWait(browser, 10)
    courses = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "intermediate-body")))
    if not courses:
        raise Exception("No intermediate feedback courses found.")

    num_courses = len(courses)
    for i in range(num_courses):
        courses = browser.find_elements(By.CLASS_NAME, "intermediate-body")
        course_names = browser.find_elements(By.CSS_SELECTOR, "h6.course")
        progress = 30 + int(60 * (i / num_courses))
        progress_bar.progress(progress)
        status_text.markdown(f"<div class='status-pill'><span class='status-icon'>📚</span><span class='status-text'>{course_names[i].text}</span></div>", unsafe_allow_html=True)
        
        browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", courses[i])
        questions_text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.bottom-0"))).text
        questions = int(questions_text.split()[-1])
        clicks = 0
        while clicks < questions:
            try:
                radio_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[@for='radio-{clicks + 1}-1']")))
                browser.execute_script("arguments[0].click();", radio_button)
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='carousel-control-next']")))
                browser.execute_script("arguments[0].click();", next_button)
                clicks += 1
                time.sleep(0.2)
            except StaleElementReferenceException:
                continue
        back_button = browser.find_element(By.CLASS_NAME, "overlay")
        browser.execute_script("arguments[0].click();", back_button)
        time.sleep(0.5)


def endsem_form(browser, progress_bar, status_text):
    wait = WebDriverWait(browser, 15)
    try:
        staff_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.staff-item")))
    except TimeoutException:
        raise Exception("Could not find the list of staff for feedback.")

    num_staff = len(staff_list)
    for i in range(num_staff):
        staff_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.staff-item")))
        course_name = staff_list[i].find_element(By.CSS_SELECTOR, "span.ms-1").text
        progress = 30 + int(60 * (i / num_staff))
        progress_bar.progress(progress)
        status_text.markdown(f"<div class='status-pill'><span class='status-icon'>📚</span><span class='status-text'>{course_name}</span></div>", unsafe_allow_html=True)
        
        browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click()", staff_list[i])
        wait.until(EC.presence_of_element_located((By.ID, "feedbackTableBody")))
        review_list = browser.find_elements(By.CSS_SELECTOR, "td.question-cell")
        for count in range(1, len(review_list) + 1):
            star_button = browser.find_element(By.XPATH, f"//tbody[@id='feedbackTableBody']/tr[{count}]/td[@class='rating-cell']/div[@class='star-rating']/label[{randint(1, 2)}]")
            browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click()", star_button)
        submit_button = browser.find_element(By.ID, "btnSave")
        browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click()", submit_button)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.img-fluid")))
        time.sleep(1)

    progress_bar.progress(95)
    status_text.markdown("<div class='status-pill'><span class='status-icon'>✨</span><span class='status-text'>Finalizing...</span></div>", unsafe_allow_html=True)
    final_submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnFinalSubmit")))
    browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click()", final_submit_button)


def run_automation(index, rollno, password, progress_bar, status_text):
    """Main automation function."""
    browser = None
    try:
        progress_bar.progress(0)
        status_text.markdown("<div class='status-pill'><span class='status-icon'>🚀</span><span class='status-text'>Initializing...</span></div>", unsafe_allow_html=True)
        browser = create_driver()
        wait = WebDriverWait(browser, 20)

        progress_bar.progress(5)
        status_text.markdown("<div class='status-pill'><span class='status-icon'>🌐</span><span class='status-text'>Connecting...</span></div>", unsafe_allow_html=True)
        browser.get("https://ecampus.psgtech.ac.in/studzone")

        progress_bar.progress(10)
        status_text.markdown("<div class='status-pill'><span class='status-icon'>🔐</span><span class='status-text'>Logging in...</span></div>", unsafe_allow_html=True)
        rollno_field = wait.until(EC.presence_of_element_located((By.ID, "rollno")))
        rollno_field.send_keys(rollno)
        password_field = browser.find_element(By.ID, "password")
        password_field.send_keys(password)
        checkbox = browser.find_element(By.ID, "terms")
        browser.execute_script("arguments[0].click();", checkbox)
        login_button = browser.find_element(By.ID, "btnLogin")
        browser.execute_script("arguments[0].click();", login_button)

        progress_bar.progress(20)
        status_text.markdown("<div class='status-pill'><span class='status-icon'>📍</span><span class='status-text'>Navigating...</span></div>", unsafe_allow_html=True)
        feedback_card = wait.until(EC.element_to_be_clickable((By.XPATH, f"//h5[text()='Feedback']")))
        browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", feedback_card)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-body")))
        feedbacks = browser.find_elements(By.CLASS_NAME, "card-body")
        
        progress_bar.progress(30)
        status_text.markdown("<div class='status-pill'><span class='status-icon'>✅</span><span class='status-text'>Starting...</span></div>", unsafe_allow_html=True)
        browser.execute_script("arguments[0].click();", feedbacks[index])
        
        if index == 0:
            endsem_form(browser, progress_bar, status_text)
        else:
            intermediate_form(browser, progress_bar, status_text)
            
        progress_bar.progress(100)
        status_text.markdown("<div class='status-pill' style='border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.1);'><span class='status-icon'>🎉</span><span class='status-text' style='color: #6ee7b7;'>Success!</span></div>", unsafe_allow_html=True)
        return True

    except TimeoutException as e:
        status_text.markdown("<div class='status-pill' style='border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.1);'><span class='status-icon'>❌</span><span class='status-text' style='color: #fca5a5;'>Check credentials</span></div>", unsafe_allow_html=True)
        return False
    except Exception as e:
        status_text.markdown(f"<div class='status-pill' style='border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.1);'><span class='status-icon'>⚠️</span><span class='status-text' style='color: #fca5a5;'>Error: {str(e)}</span></div>", unsafe_allow_html=True)
        return False
    finally:
        if browser:
            browser.quit()



# Submit button
if st.button("🚀 Submit Feedback", type="primary", disabled=not (rollno and password)):
    if not rollno or not password:
        st.error("⚠️ Please enter both roll number and password")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("Running..."):
            success = run_automation(feedback_type[1], rollno, password, progress_bar, status_text)
        
        if success:
            st.success("🎉 Feedback submitted successfully!")
            st.balloons()

# Info Card - Bunker Style
st.markdown("""
    <div class='info-card'>
        <p class='info-text'>⚠️ Educational use only • Use responsibly</p>
    </div>
""", unsafe_allow_html=True)

