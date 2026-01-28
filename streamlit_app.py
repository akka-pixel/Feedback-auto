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

# Page configuration
st.set_page_config(
    page_title="Feedback Automation",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# PREMIUM CSS - MOBILE OPTIMIZED
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Outfit', sans-serif; }
    
    /* Background */
    .stApp {
        background: #000000;
        background-image: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.1) 0%, transparent 50%);
    }
    
    /* Container */
    .main .block-container {
        padding: 1.5rem 1rem !important;
        max-width: 100% !important;
    }
    
    @media (min-width: 640px) {
        .main .block-container {
            background: rgba(18, 18, 24, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 24px;
            padding: 2.5rem !important;
            max-width: 480px !important;
            margin: 2rem auto !important;
        }
    }
    
    /* Hide Streamlit UI */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none !important; }
    
    /* Title */
    h1 {
        background: linear-gradient(to right, #fff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin: 0 0 0.5rem 0 !important;
        font-size: 2.5rem !important;
        line-height: 1 !important;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    
    /* INPUTS - CLEAN & SIMPLE */
    .stTextInput > div > div, .stSelectbox > div > div {
        background: transparent !important;
    }
    
    .stTextInput input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        color: white !important;
        font-size: 15px !important;
        height: 50px !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput input:focus {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        min-height: 50px !important;
    }
    
    .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }
    
    .stTextInput label, .stSelectbox label {
        color: rgba(255, 255, 255, 0.6) !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* BUTTON */
    .stButton button {
        width: 100% !important;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        margin-top: 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 8px 16px -8px rgba(99, 102, 241, 0.5) !important;
    }
    
    .stButton button:active {
        transform: scale(0.98) !important;
    }
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.85rem !important;
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .streamlit-expanderContent {
        padding: 12px 0 !important;
        background: transparent !important;
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #a855f7) !important;
        height: 6px !important;
        border-radius: 10px !important;
    }
    
    .stProgress > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
    }
    
    /* Loading Spinner */
    .loading-container {
        text-align: center;
        padding: 3rem 0 2rem;
    }
    
    .spinner {
        margin: 0 auto;
        width: 60px;
        height: 60px;
        position: relative;
    }
    
    .spinner-ring {
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid rgba(99, 102, 241, 0.2);
        border-top-color: #6366f1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .loading-text {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        margin-top: 1.5rem;
        font-weight: 500;
    }
    
    /* Status Card */
    .status-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 12px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .status-icon {
        font-size: 1.25rem;
        flex-shrink: 0;
    }
    
    .status-text {
        flex: 1;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .status-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.6;
        margin-bottom: 2px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.1em;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("<h1>Feedback.</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Automated Feedback Entry</p>", unsafe_allow_html=True)

def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def render_status(text, subtext="Processing", icon="⚡", color="#6366f1"):
    return f"""
        <div class="status-card" style="border-left-color: {color}">
            <div class="status-icon" style="color: {color}">{icon}</div>
            <div style="flex: 1">
                <div class="status-label">{subtext}</div>
                <div class="status-text">{text}</div>
            </div>
        </div>
    """

# Session State
if 'processing' not in st.session_state:
    st.session_state.processing = False

def intermediate_form(browser, progress_bar, status_placeholder):
    wait = WebDriverWait(browser, 10)
    try:
        courses = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "intermediate-body")))
    except TimeoutException:
         raise Exception("No active intermediate feedback courses found.")
    
    num_courses = len(courses)
    for i in range(num_courses):
        courses = browser.find_elements(By.CLASS_NAME, "intermediate-body")
        course_names = browser.find_elements(By.CSS_SELECTOR, "h6.course")
        
        progress_bar.progress(30 + int(60 * (i / num_courses)))
        status_placeholder.markdown(
            render_status(course_names[i].text, "Completing Survey", "📝", "#a855f7"), 
            unsafe_allow_html=True
        )
        
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
                time.sleep(0.15)
            except StaleElementReferenceException:
                continue
                
        back_button = browser.find_element(By.CLASS_NAME, "overlay")
        browser.execute_script("arguments[0].click();", back_button)
        time.sleep(0.5)

def endsem_form(browser, progress_bar, status_placeholder):
    wait = WebDriverWait(browser, 15)
    try:
        staff_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.staff-item")))
    except TimeoutException:
        raise Exception("Staff list not found. Feedback might be closed or already completed.")
    
    num_staff = len(staff_list)
    for i in range(num_staff):
        staff_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.staff-item")))
        course_name = staff_list[i].find_element(By.CSS_SELECTOR, "span.ms-1").text
        
        progress_bar.progress(30 + int(60 * (i / num_staff)))
        status_placeholder.markdown(
            render_status(course_name, "Evaluating Staff", "👨‍🏫", "#3b82f6"), 
            unsafe_allow_html=True
        )
        
        browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click()", staff_list[i])
        wait.until(EC.presence_of_element_located((By.ID, "feedbackTableBody")))
        
        review_list = browser.find_elements(By.CSS_SELECTOR, "td.question-cell")
        for count in range(1, len(review_list) + 1):
            star_button = browser.find_element(By.XPATH, f"//tbody[@id='feedbackTableBody']/tr[{count}]/td[@class='rating-cell']/div[@class='star-rating']/label[{randint(1, 2)}]")
            browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click()", star_button)
            
        submit_button = browser.find_element(By.ID, "btnSave")
        browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click()", submit_button)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.img-fluid")))
        time.sleep(0.8)

    status_placeholder.markdown(render_status("All forms completed", "Finalizing", "🚀", "#10b981"), unsafe_allow_html=True)
    final_submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnFinalSubmit")))
    browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click()", final_submit_button)

def run_automation(index, rollno, password, progress_bar, status_placeholder):
    browser = None
    try:
        progress_bar.progress(5)
        status_placeholder.markdown(render_status("Initializing Browser", "System", "⚙️", "#94a3b8"), unsafe_allow_html=True)
        
        browser = create_driver()
        wait = WebDriverWait(browser, 20)

        progress_bar.progress(15)
        status_placeholder.markdown(render_status("Connecting to Portal", "Network", "🌐", "#6366f1"), unsafe_allow_html=True)
        browser.get("https://ecampus.psgtech.ac.in/studzone")

        progress_bar.progress(25)
        status_placeholder.markdown(render_status("Authenticating User", "Security", "🔐", "#f59e0b"), unsafe_allow_html=True)
        
        wait.until(EC.presence_of_element_located((By.ID, "rollno"))).send_keys(rollno)
        browser.find_element(By.ID, "password").send_keys(password)
        
        try:
            browser.execute_script("arguments[0].click();", browser.find_element(By.ID, "terms"))
            browser.execute_script("arguments[0].click();", browser.find_element(By.ID, "btnLogin"))
        except Exception:
             raise Exception("Login elements changed or unavailable.")

        progress_bar.progress(35)
        status_placeholder.markdown(render_status("Accessing Module", "Navigation", "🧭", "#ec4899"), unsafe_allow_html=True)
        
        try:
            feedback_card = wait.until(EC.element_to_be_clickable((By.XPATH, f"//h5[text()='Feedback']")))
            browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", feedback_card)
        except TimeoutException:
             raise Exception("Login failed. Check Credentials or Portal Status.")

        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-body")))
            feedbacks = browser.find_elements(By.CLASS_NAME, "card-body")
            browser.execute_script("arguments[0].click();", feedbacks[index])
        except Exception:
            raise Exception("Feedback section not responsive.")
        
        if index == 0:
            endsem_form(browser, progress_bar, status_placeholder)
        else:
            intermediate_form(browser, progress_bar, status_placeholder)
            
        progress_bar.progress(100)
        status_placeholder.markdown(render_status("Feedback Submitted Successfully", "Complete", "🎉", "#10b981"), unsafe_allow_html=True)
        return "Success"

    except Exception as e:
        error_msg = str(e)
        status_placeholder.markdown(render_status(error_msg, "Process Failed", "❌", "#ef4444"), unsafe_allow_html=True)
        return "Error"
    finally:
        if browser:
            browser.quit()

# ----- UI LOGIC -----
if not st.session_state.processing:
    # Input Form
    rollno = st.text_input("Roll Number", placeholder="e.g. 29X201", help="College Roll Number")
    password = st.text_input("Password", type="password", placeholder="•••••••", help="eCampus Password")
    
    feedback_type = st.selectbox(
        "Automation Target",
        options=[("End Semester Feedback", 0), ("Intermediate Feedback", 1)],
        format_func=lambda x: x[0]
    )

    # Terms Section
    with st.expander("📋 Terms of Use"):
        st.markdown("""
            <div style='font-size: 0.85rem; color: rgba(255,255,255,0.7); line-height: 1.6;'>
                <p><strong>Educational Purpose Only</strong><br>
                This system helps understand browser automation. By using it, you agree to:</p>
                <ul style="padding-left: 1.2rem; margin-top: 5px;">
                    <li>Use responsibly and ethically</li>
                    <li>Not store personal credentials</li>
                    <li>Accept full responsibility for usage</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Submit Button
    if st.button("INITIATE SEQUENCE"):
        if not rollno or not password:
            st.error("⚠️ Authentication credentials required")
        else:
            st.session_state.processing = True
            st.session_state.rollno = rollno
            st.session_state.password = password
            st.session_state.feedback_idx = feedback_type[1]
            st.rerun()

else:
    # Processing View - CLEAN LOADING
    st.markdown("""
        <div class="loading-container">
            <div class="spinner">
                <div class="spinner-ring"></div>
            </div>
            <div class="loading-text">Processing your request...</div>
        </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    
    result = run_automation(st.session_state.feedback_idx, st.session_state.rollno, st.session_state.password, progress_bar, status_placeholder)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.processing = False
            st.rerun()
    
    if result == "Success":
        st.balloons()
        

# Footer
st.markdown("<div class='footer'>SECURE • PRIVATE • EDUCATIONAL</div>", unsafe_allow_html=True)
