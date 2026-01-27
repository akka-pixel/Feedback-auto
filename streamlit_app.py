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

# Advanced CSS Architecture
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #6366f1;
        --secondary: #a855f7;
        --accent: #ec4899;
        --bg-deep: #000000;
        --glass-border: rgba(255, 255, 255, 0.15);
        --text: #ffffff;
        --card-bg: #121212;
    }

    /* Global Reset & Typography */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        color: var(--text);
        background-color: var(--bg-deep);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Background - Mobile Optimized */
    .stApp {
        background-color: var(--bg-deep);
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 100% 100%, rgba(168, 85, 247, 0.08) 0%, transparent 40%);
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    /* Main Content Container - Mobile First */
    .main .block-container {
        background: transparent;
        padding: 1.5rem 1rem;
        max-width: 100%;
        margin: 0 auto;
    }
    
    /* Desktop override */
    @media (min-width: 640px) {
        .main .block-container {
            background: rgba(18, 18, 24, 0.4);
            border: 1px solid var(--glass-border);
            border-radius: 32px;
            padding: 2.5rem 2rem;
            max-width: 480px;
            margin: 2rem auto;
            box-shadow: 0 30px 60px -15px rgba(0,0,0,0.5);
        }
    }

    /* Hide Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Typography - Mobile Optimized */
    h1 {
        background: linear-gradient(to right, #fff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.25rem !important;
        font-size: 2.5rem !important;
        letter-spacing: -0.03em;
        filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.3));
        line-height: 1.1;
    }
    
    @media (min-width: 640px) {
        h1 {
            font-size: 3.5rem !important;
        }
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
        font-weight: 600;
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    
    @media (min-width: 640px) {
        .subtitle {
            font-size: 0.85rem;
            margin-bottom: 2.5rem;
        }
    }

    /* MOBILE-FRIENDLY INPUTS */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div[class*="singleValue"] {
        background-color: #111 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 16px !important;
        padding: 16px 18px !important;
        font-size: 16px !important; /* Prevents zoom on iOS */
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        height: auto !important;
        min-height: 52px !important; /* Better touch target */
        box-shadow: none !important;
    }

    .stSelectbox > div > div {
        background-color: #111 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        color: white !important;
        min-height: 52px !important;
    }

    /* Focus States - Mobile Friendly */
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within {
        background-color: #181818 !important;
        border-color: var(--primary) !important;
        border-width: 2px !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
        transform: none !important;
    }

    /* Labels - Mobile Optimized */
    .stTextInput label, .stSelectbox label {
        color: rgba(255, 255, 255, 0.65) !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem !important;
        margin-left: 0.25rem !important;
    }

    /* Button - Mobile Optimized with Large Touch Target */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 1rem !important;
        min-height: 56px !important; /* Minimum touch target */
        border-radius: 16px !important;
        border: none !important;
        transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        font-size: 1rem !important;
        letter-spacing: 0.05em !important;
        position: relative;
        overflow: hidden;
        margin-top: 1.25rem !important;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4) !important;
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
    }
    
    @media (min-width: 640px) {
        .stButton > button {
            padding: 1.2rem !important;
            font-size: 1.1rem !important;
        }
    }
    
    .stButton > button:active {
        transform: scale(0.97) !important;
    }

    /* Progress Bar - Mobile Friendly */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border-radius: 10px;
        height: 8px !important;
    }
    
    .stProgress > div {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        height: 8px !important;
    }
    
    /* Remove default margins */
    .stTextInput {margin-bottom: 1rem;}
    .stSelectbox {margin-bottom: 1rem;}

    /* Status Card - Mobile Optimized */
    .status-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1rem;
        margin: 1.25rem 0;
        display: flex;
        align-items: center;
        gap: 0.875rem;
        animation: slideIn 0.4s ease-out;
        backdrop-filter: blur(10px);
    }
    
    @media (min-width: 640px) {
        .status-card {
            padding: 1.25rem;
            border-radius: 24px;
            gap: 1rem;
        }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .status-icon-box {
        width: 40px;
        height: 40px;
        background: rgba(99, 102, 241, 0.15);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #a5b4fc;
        font-size: 1.25rem;
        flex-shrink: 0;
    }
    
    @media (min-width: 640px) {
        .status-icon-box {
            width: 44px;
            height: 44px;
            font-size: 1.35rem;
        }
    }
    
    .status-content {
        flex: 1;
        min-width: 0;
    }
    
    .status-title {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    @media (min-width: 640px) {
        .status-title {
            font-size: 0.75rem;
        }
    }
    
    .status-desc {
        color: white;
        font-weight: 600;
        font-size: 0.95rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    @media (min-width: 640px) {
        .status-desc {
            font-size: 1rem;
        }
    }

    /* Expander - Mobile Friendly */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 0.85rem !important;
        padding: 0.875rem !important;
        min-height: 48px !important;
    }
    
    @media (min-width: 640px) {
        .streamlit-expanderHeader {
            border-radius: 16px !important;
            font-size: 0.9rem !important;
            padding: 1rem !important;
        }
    }
    
    .streamlit-expanderContent {
        background: transparent !important;
        border: none !important;
        padding-top: 0.875rem !important;
    }
    
    /* Footer */
    .info-footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        color: rgba(255, 255, 255, 0.25);
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    @media (min-width: 640px) {
        .info-footer {
            margin-top: 4rem;
            padding-top: 2rem;
            font-size: 0.75rem;
        }
    }
    
    /* Error/Success Messages - Mobile Friendly */
    .stError, .stSuccess {
        border-radius: 14px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.9rem !important;
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

def render_status(text, subtext="Processing...", icon="⚡", color="#6366f1"):
    return f"""
        <div class="status-card" style="border-left: 3px solid {color}">
            <div class="status-icon-box" style="background: {color}20; color: {color}">
                {icon}
            </div>
            <div class="status-content">
                <div class="status-title">{subtext}</div>
                <div class="status-desc">{text}</div>
            </div>
        </div>
    """

# Session State Handling
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
        
        # Update progress
        progress_bar.progress(30 + int(60 * (i / num_courses)))
        status_placeholder.markdown(
            render_status(course_names[i].text, "Completing Survey", "📝", "#a855f7"), 
            unsafe_allow_html=True
        )
        
        browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", courses[i])
        
        # Form filling logic
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
        
        # Login Logic
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
        # Clean up error message for display
        if "Message:" in error_msg:
            # Handle selenium generic errors if any leak through
            pass 
        status_placeholder.markdown(render_status(error_msg, "Process Failed", "❌", "#ef4444"), unsafe_allow_html=True)
        return "Error"
    finally:
        if browser:
            browser.quit()

# Logic to toggle views
if not st.session_state.processing:
    # Input Container
    with st.container():
        st.markdown("<div style='padding: 0 0.5rem;'>", unsafe_allow_html=True) # Mobile padding
        rollno = st.text_input("Roll Number", placeholder="e.g. 25U201", help="College Roll Number")
        password = st.text_input("Password", type="password", placeholder="•••••••", help="eCampus Password")
        
        feedback_type = st.selectbox(
            "Automation Target",
            options=[("End Semester Feedback", 0), ("Intermediate Feedback", 1)],
            format_func=lambda x: x[0]
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Terms Section
    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    with st.expander("Terms of Use", expanded=False):
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

    # Action Button
    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
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
    # Processing View (Inputs Hidden) - PREMIUM LOADING ANIMATION
    st.markdown("""
        <div style='text-align: center; margin: 3rem 0 2rem 0; position: relative;'>
            <!-- Outer pulsing ring -->
            <div class='pulse-ring'></div>
            
            <!-- Middle spinning ring -->
            <div class='spinner-ring'></div>
            
            <!-- Inner glowing core -->
            <div class='core-glow'></div>
            
            <!-- Animated dots -->
            <div class='loading-dots'>
                <span class='dot'></span>
                <span class='dot'></span>
                <span class='dot'></span>
            </div>
            
            <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 8rem; font-weight: 600; letter-spacing: 0.05em;'>
                Processing your request<span class='dot-animate'>.</span><span class='dot-animate'>.</span><span class='dot-animate'>.</span>
            </p>
        </div>
        
        <style>
            @keyframes pulse {
                0%, 100% { 
                    transform: scale(1); 
                    opacity: 0.6; 
                }
                50% { 
                    transform: scale(1.15); 
                    opacity: 0.3; 
                }
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @keyframes glow {
                0%, 100% { 
                    box-shadow: 0 0 20px rgba(99, 102, 241, 0.5), 
                                0 0 40px rgba(168, 85, 247, 0.3),
                                inset 0 0 20px rgba(99, 102, 241, 0.3);
                }
                50% { 
                    box-shadow: 0 0 30px rgba(99, 102, 241, 0.8), 
                                0 0 60px rgba(168, 85, 247, 0.5),
                                inset 0 0 30px rgba(99, 102, 241, 0.5);
                }
            }
            
            @keyframes bounce {
                0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
                40% { transform: translateY(-10px); opacity: 1; }
            }
            
            @keyframes dotFade {
                0%, 100% { opacity: 0; }
                50% { opacity: 1; }
            }
            
            .pulse-ring {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 120px;
                height: 120px;
                border: 3px solid rgba(99, 102, 241, 0.3);
                border-radius: 50%;
                animation: pulse 2s ease-in-out infinite;
            }
            
            .spinner-ring {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 80px;
                height: 80px;
                border: 4px solid transparent;
                border-top: 4px solid #6366f1;
                border-right: 4px solid #8b5cf6;
                border-radius: 50%;
                animation: spin 1.2s linear infinite;
            }
            
            .core-glow {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                border-radius: 50%;
                animation: glow 2s ease-in-out infinite;
            }
            
            .loading-dots {
                position: absolute;
                top: calc(50% + 70px);
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 8px;
            }
            
            .loading-dots .dot {
                width: 8px;
                height: 8px;
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                border-radius: 50%;
                animation: bounce 1.4s infinite ease-in-out;
            }
            
            .loading-dots .dot:nth-child(1) {
                animation-delay: 0s;
            }
            
            .loading-dots .dot:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .loading-dots .dot:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            .dot-animate {
                animation: dotFade 1.5s infinite;
            }
            
            .dot-animate:nth-child(1) {
                animation-delay: 0s;
            }
            
            .dot-animate:nth-child(2) {
                animation-delay: 0.3s;
            }
            
            .dot-animate:nth-child(3) {
                animation-delay: 0.6s;
            }
        </style>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    
    # Run the automation
    result = run_automation(st.session_state.feedback_idx, st.session_state.rollno, st.session_state.password, progress_bar, status_placeholder)
    
    # Show back button after completion
    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.processing = False
            st.rerun()
    
    if result == "Success":
        st.balloons()

# Footer
st.markdown("<div class='info-footer'>Secure • Private • Educational</div>", unsafe_allow_html=True)

