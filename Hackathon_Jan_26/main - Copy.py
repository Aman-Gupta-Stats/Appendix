import streamlit as st
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import plotly.express as px




with open("Data\data_dictionary.json", "r", encoding="utf-8-sig") as f:
    language_data = json.load(f)



#st.set_page_config(layout="wide")
st.set_page_config(layout="centered")


if "language" not in st.session_state:
    st.session_state.language = "English"

if "adol_prog" not in st.session_state:
    st.session_state.adol_prog = False

if "live_prog" not in st.session_state:
    st.session_state.live_prog = False

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

if "mob_login" not in st.session_state:
    st.session_state.mob_login = False

if "username" not in st.session_state:
    st.session_state.username = None

if "live_user_login" not in st.session_state:
    st.session_state.live_user_login = False


if "admin_user_login" not in st.session_state:
    st.session_state.admin_user_login = False

if "mob_user_login" not in st.session_state:
    st.session_state.mob_user_login = False

if "hard_init" not in st.session_state:
    st.session_state.hard_init = False

if "soft_init" not in st.session_state:
    st.session_state.soft_init = False


# language_data.get("",{}).get(st.session_state.language,"")

def main_page():


    cols = st.columns([1,4,0.56])
    with cols[0]:
        lan = st.selectbox("Language",("English", "हिंदी", "ਪੰਜਾਬੀ", "ಕನ್ನಡ"),)
        
        if lan == "English":
            st.session_state.language = "English"
        elif lan == "हिंदी":
            st.session_state.language = "Hindi"
        elif lan == "ਪੰਜਾਬੀ":
            st.session_state.language = "Punjabi"
        elif lan == "ಕನ್ನಡ":
            st.session_state.language = "Kannada"


        
    with cols[2]:
        if st.button(language_data.get("Admin Login",{}).get(st.session_state.language,"Admin Login")):
            st.session_state.admin_login = True
        
    cols = st.columns([4.7,0.5])
    
    with cols[1]:
    
        if st.button(language_data.get("Mobilizer Login",{}).get(st.session_state.language,"Mobilizer Login")):
            st.session_state.mob_login = True




    # 3.1. Logo (centered)
    cols = st.columns([1.3, 1, 1])
    with cols[1]:
        st.image("Data\Images\Magic-Bus-Logo.png", width=200)

    
    cols = st.columns([1.2, 1.5, 0.8])
    with cols[1]:
        st.markdown(
            """
    <h1 style="color:white; font-size:28px;">
        The <span style="color:red;">Magic</span> starts here
    </h1>
    """,
    unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("")
    # cols = st.columns([0.6,1,1.2,1, 1])
    # with cols[1]:
    #     st.image("Data\Images\program_adol_prog.png", width=400)

    # with cols[3]:
    #     st.image("Data\Images\program_live_prog.png", width=400)




    ### adding button
    cols = st.columns([0.62,1.1,1.2,1, 1])
    with cols[1]:
        st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            background-color: #FFBD05;  /* yellow hex */
            color: red;
            width: 200px;
            height: 50px;
            font-size: 48px;
            font-weight: bold;
            border-radius: 10px;
            border: none;
        }

        div[data-testid="stButton"] > button:hover {
            background-color: #FFC300;
            color: red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

        

        if st.button(language_data.get("Adolescent Program",{}).get(st.session_state.language,"Adolescent Program")):
            st.session_state.adol_prog = True


    with cols[3]:
        st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            background-color: #FFBD05;  /* yellow hex */
            color: red;
            width: 200px;
            height: 50px;
            font-size: 48px;
            font-weight: bold;
            border-radius: 10px;
            border: none;
        }

        div[data-testid="stButton"] > button:hover {
            background-color: #FFC300;
            color: red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

        

        if st.button(language_data.get("Livelihood Program",{}).get(st.session_state.language,"Livelihood Program")):
            st.session_state.live_prog = True

    st.rerun()

        
def login_page() :
    if st.session_state.adol_prog:
        pass

    elif st.session_state.live_prog:
        cols = st.columns([6, 0.1])
        with cols[0]:
            st.image("Data\Images\live_prog_banner.png", width=2000)

        cols = st.columns([1,4, 1])
        with cols[1]:
            
            st.title(language_data.get("Enter your Credentials",{}).get(st.session_state.language,"Enter your Credentials"), text_alignment= "center" )
            username = st.text_input(label="", placeholder=language_data.get("Enter Username",{}).get(st.session_state.language,"Enter Username"), key="username_input")
            password = st.text_input(label="", placeholder=language_data.get("Enter Password",{}).get(st.session_state.language,"Enter Password"), type="password", key="password_input")

            if st.button(language_data.get("Login",{}).get(st.session_state.language,"Login"), key="login_button", type ="primary",width  = "stretch"):
                    placeholder = st.empty()
                    combined_html = f"""
                    <style>
                    .loader {{
                        border: 4px solid #f3f3f3;
                        border-top: 4px solid #1f77b4;
                        border-radius: 50%;
                        width: 24px;
                        height: 24px;
                        animation: spin 1s linear infinite;
                    }}
                    @keyframes spin {{
                        0% {{ transform: rotate(0deg); }}
                        100% {{ transform: rotate(360deg); }}
                    }}
                    </style>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div class="loader"></div>
                        <span>👤 Attempting to log in as <b>{username}</b></span>
                    </div>
                    """
                    placeholder.markdown(combined_html, unsafe_allow_html=True)
                    time.sleep(0.5)

                    # In a real app, you’d verify username/password here.
                    # For demonstration, we assume it’s always successful.
                    placeholder.markdown(f"👤 Log In Successful!")
                    time.sleep(0.5)

                    st.session_state.username = username
                    st.session_state.live_user_login = True
                    st.rerun()
                    

    elif st.session_state.admin_login:
        cols = st.columns([6, 0.1])
        with cols[0]:
            st.image("Data\Images\\admin_banner.png", width=2000)

    elif st.session_state.mob_login:
        cols = st.columns([6, 0.1])
        with cols[0]:
            st.image("Data\Images\mob_banner.png", width=2000)

    if st.session_state.admin_login or st.session_state.mob_login:
        cols = st.columns([1,4,1])
        
        with cols[1]:
            st.title(language_data.get("Enter your Credentials",{}).get(st.session_state.language,"Enter your Credentials"), text_alignment= "center" )
            username = st.text_input(label="", placeholder=language_data.get("Enter Username",{}).get(st.session_state.language,"Enter Username"), key="username_input")
            password = st.text_input(label="", placeholder=language_data.get("Enter Password",{}).get(st.session_state.language,"Enter Password"), type="password", key="password_input")

            if st.button(language_data.get("Login",{}).get(st.session_state.language,"Login"), key="login_button",type ="primary",width  = "stretch"):
                    placeholder = st.empty()
                    combined_html = f"""
                    <style>
                    .loader {{
                        border: 4px solid #f3f3f3;
                        border-top: 4px solid #1f77b4;
                        border-radius: 50%;
                        width: 24px;
                        height: 24px;
                        animation: spin 1s linear infinite;
                    }}
                    @keyframes spin {{
                        0% {{ transform: rotate(0deg); }}
                        100% {{ transform: rotate(360deg); }}
                    }}
                    </style>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div class="loader"></div>
                        <span>👤 Attempting to log in as <b>{username}</b></span>
                    </div>
                    """
                    placeholder.markdown(combined_html, unsafe_allow_html=True)
                    time.sleep(0.5)

                    # In a real app, you’d verify username/password here.
                    # For demonstration, we assume it’s always successful.
                    placeholder.markdown(f"👤 Log In Successful!")
                    time.sleep(0.5)

                    st.session_state.username = username
                    if st.session_state.admin_login:
                        st.session_state.admin_user_login = True
                    elif st.session_state.mob_login:
                        st.session_state.mob_user_login = True
                    st.rerun()


        
def live_user_dashboard():
    cols = st.columns([6,1])
    with cols[1]:
        if st.button("Log Out",key = "7527527",type ="primary"):
            st.session_state.clear()
            #time.sleep(10)
            # st.session_state.adol_prog = False
            # st.session_state.live_prog= False
            # st.session_state.admin_login= False
            # st.session_state.mob_login= False
            # st.session_state.live_user_login= False
            # st.session_state.admin_user_login= False
            # st.session_state.mob_user_login= False
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()

    st.title("Welcome " + language_data.get("Aman",{}).get(st.session_state.language,"Aman"))
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([language_data.get("Feed",{}).get(st.session_state.language,"Feed"), language_data.get("Alumini Network",{}).get(st.session_state.language,"Alumini Network"), language_data.get("Videos",{}).get(st.session_state.language,"Videos")])
    with tab1:
        if st.session_state.language == "English":
            st.subheader("Aarav Mehta has been appointed today, 29 January 2026, with Starbucks, with a salary range of ₹15,000 - ₹17,000.")
            st.subheader("Sneha Raghavan has joined Reliance Trends today, 29 January 2026, with a salary package ranging from ₹18,000 to ₹ 20,000.")
            st.subheader("Rahul Chatterjee has joined IDBI Bank today, 29 January 2026, with a salary range of ₹23,000 - ₹25,000.")
            st.subheader("Kiran Deshpande has joined Teleperformance Solutions on 30 December 2025, with a salary range of ₹18,000 - ₹20,000.")
            st.subheader("Manoj Nambiar has joined TCS on 19 December 2025, with a salary range of ₹23,000 - ₹25,000.")
            st.subheader("Ishita Verma has joined McDonalds on 10 December 2025, with a salary range of ₹15,000 - ₹17,000.")

        elif st.session_state.language == "Hindi":
            st.subheader("आरव मेहता को आज, 29 जनवरी 2026 को Starbucks में नियुक्त किया गया है, जिनका वेतन पैकेज ₹15,000 - ₹17,000 है।")
            st.subheader("स्नेहा राघवन आज, 29 जनवरी 2026 को Reliance Trends से जुड़ी हैं, जिनका वेतन पैकेज ₹18,000 से ₹ 20,000 के बीच है।")
            st.subheader("राहुल चटर्जी आज, 29 जनवरी 2026 को IDBI Bank से जुड़े हैं, जिनका वेतन पैकेज ₹23,000 - ₹25,000 है।")
            st.subheader("किरण देशपांडे 30 दिसंबर 2025 को Teleperformance Solutions से जुड़े हैं, जिनका वेतनमान ₹18,000 - ₹20,000 है।")
            st.subheader("मनोज नायंबियार 19 दिसंबर 2025 को TCS से जुड़े हैं, जिनका वेतनमान ₹23,000 - ₹25,000 है।")
            st.subheader("इशिता वर्मा 10 दिसंबर 2025 को McDonalds से जुड़ी हैं, जिनका वेतनमान ₹15,000 - ₹17,000 है।")

        elif st.session_state.language == "Punjabi":
            st.subheader("ਆਰਵ ਮਹੇਤਾ ਨੂੰ ਅੱਜ, 29 ਜਨਵਰੀ 2026 ਨੂੰ Starbucks ਵਿੱਚ ਨਿਯੁਕਤ ਕੀਤਾ ਗਿਆ ਹੈ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹15,000 - ₹17,000 ਹੈ।")
            st.subheader("ਸਨੇਹਾ ਰਾਘਵਨ ਅੱਜ, 29 ਜਨਵਰੀ 2026 ਨੂੰ Reliance Trends ਨਾਲ ਜੁੜ ਗਈ ਹੈ, ਜਿਸਦੀ ਤਨਖ਼ਾਹ ₹18,000 ਤੋਂ ₹ 20,000 ਤੱਕ ਹੈ।")
            st.subheader("ਰਾਹੁਲ ਚੱਟਰਜੀ ਅੱਜ, 29 ਜਨਵਰੀ 2026 ਨੂੰ IDBI Bank ਨਾਲ ਜੁੜੇ ਹਨ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹23,000 - ₹25,000 ਹੈ।")
            st.subheader("ਕਿਰਨ ਦੇਸ਼ਪਾਂਡੇ 30 ਦਸੰਬਰ 2025 ਨੂੰ Teleperformance Solutions ਨਾਲ ਜੁੜੇ ਹਨ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹18,000 - ₹20,000 ਹੈ।")
            st.subheader("ਮਨੋਜ ਨਾਇੰਬਿਆਰ 19 ਦਸੰਬਰ 2025 ਨੂੰ TCS  ਨਾਲ ਜੁੜੇ ਹਨ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹23,000 - ₹25,000 ਹੈ।")
            st.subheader("ਇਸ਼ਿਤਾ ਵਰਮਾ 30 ਦਸੰਬਰ 2025 ਨੂੰ McDonalds ਨਾਲ ਜੁੜੀ ਹੈ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹15,000 - ₹17,000 ਹੈ।")

        elif st.session_state.language == "Kannada":
            st.subheader("ಆರವ್ ಮೇಹ್ತಾ ಅವರನ್ನು ಇಂದು, 29 ಜನವರಿ 2026 ರಂದು Starbucks ನಲ್ಲಿ ನೇಮಕ ಮಾಡಲಾಗಿದೆ, ಸಂಬಳ ಶ್ರೇಣಿಯು ₹15,000 - ₹17,000 ಆಗಿದೆ")
            st.subheader("ಸ್ನೇಹಾ ರಾಘವನ್ ಅವರು ಇಂದು, 29 ಜನವರಿ 2026 ರಂದು Reliance Trends ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಪ್ಯಾಕೇಜ್ ₹18,000 ರಿಂದ ₹ 20,000 ವರೆಗೆ ಇದೆ")
            st.subheader("ರಾಹುಲ್ ಚಟರ್ಜಿ ಅವರು ಇಂದು, 29 ಜನವರಿ 2026 ರಂದು IDBI Bank ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಶ್ರೇಣಿ ₹23,000 - ₹25,000 ಆಗಿದೆ")
            st.subheader("ಕಿರಣ್ ದೇಶಪಾಂಡೆ ಅವರು 30 ಡಿಸೆಂಬರ್ 2025 ರಂದು Teleperformance Solutions ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಶ್ರೇಣಿ ₹18,000 - ₹20,000 ಆಗಿದೆ")
            st.subheader("ಮನೋಜ್ ನಯ್ಯಂಬಿಯರ್ ಅವರು 19 ಡಿಸೆಂಬರ್ 2025 ರಂದು TCS ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಶ್ರೇಣಿ ₹23,000 - ₹25,000 ಆಗಿದೆ")
            st.subheader("ಇಶಿತಾ ವರ್ಮಾ ಅವರು 10 ಡಿಸೆಂಬರ್ 2025 ರಂದು McDonalds ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಶ್ರೇಣಿ ₹15,000 - ₹17,000 ಆಗಿದೆ")

    with tab2:
        if st.session_state.language == "English":
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p1.png", width=300)
                
                
            with cols[1]:
                st.subheader("Name: Vishwas")
                st.subheader("Employer: DMart")
                st.subheader("Age: 24 Years")
                st.subheader("Address PIN: 115733")
                st.subheader("Salary: 30,000")
            

            st.markdown("---")
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p2.png", width=300)
                
                
            with cols[1]:
                st.subheader("Name: Raghav")
                st.subheader("Employer: Reliance Trends")
                st.subheader("Age: 24 Years")
                st.subheader("Address PIN: 116793")
                st.subheader("Salary: 30,000")
            

            st.markdown("---")
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p3.png", width=300)
                
                
            with cols[1]:
                st.subheader("Name: Abhinav")
                st.subheader("Employer: Lenskart")
                st.subheader("Age: 24 Years")
                st.subheader("Address PIN: 110093")
                st.subheader("Salary: 35,000")
            

            st.markdown("---")

        if st.session_state.language == "Hindi":
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p3.png", width=300)
                
                
            with cols[1]:
                st.subheader("नाम : अभिनव")
                st.subheader("नियोक्ता : लेंसकार्ट")
                st.subheader("आयु : 24")
                st.subheader("पता पिन : 110093")
                st.subheader("वेतन : 35,000")
            

            st.markdown("---")

        if st.session_state.language == "Punjabi":
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p1.png", width=300)
                
                
            with cols[1]:
                st.subheader("ਨਾਂ : ਵਿਸ਼ਵਾਸ")
                st.subheader("ਨਿਯੋਤਾ : ਡੀਮਾਰਟ")
                st.subheader("ਉਮਰ : 24")
                st.subheader("ਪਤਾ ਪਿਨ : 115733")
                st.subheader("ਤਨਖਾਹ : 30,000")
            

            st.markdown("---")

        if st.session_state.language == "Kannada":
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p2.png", width=300)
                
                
            with cols[1]:
                st.subheader("ಹೆಸರು: ರಾಘವ್")
                st.subheader("ನಿಯೋಜಕ: ರಿಲಾಯನ್ಸ್ ಟ್ರೆಂಡ್ಸ್")
                st.subheader("ವಯಸ್ಸು: 24")
                st.subheader("ವಿಳಾಸ ಪಿನ್: 116793")
                st.subheader("ತಡೆಯವರು: 30,000")
            

            st.markdown("---")

    with tab3:
        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt1.png", width=300)
            
            
        with cols[1]:
            st.subheader("Personal Development Skills")
            st.markdown("- Confidence Building")
            st.markdown("- Self‑awareness")
            st.markdown("- Emotional Intelligence")
            st.markdown("- Self‑discipline & Motivation")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt2.png", width=300)
            
            
        with cols[1]:
            st.subheader("Communication & People Skills")
            st.markdown("- Public Speaking")
            st.markdown("- Active Listening")
            st.markdown("- Teamwork & Collaboration")
            st.markdown("- Customer Service Skills")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt3.png", width=300)
            
            
        with cols[1]:
            st.subheader("Cognitive & Problem-Solving Skills")
            st.markdown("- Critical Thinking")
            st.markdown("- Logical Reasoning")
            st.markdown("- Decision‑making")
            st.markdown("- Creative Problem Solving")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt4.png", width=300)
            
            
        with cols[1]:
            st.subheader("Digital & Technical Skills")
            st.markdown("- Basic Computer Literacy")
            st.markdown("- Using Smartphones & Apps")
            st.markdown("- Email, Online Forms & Digital Payments")
            st.markdown("- Introduction to MS Office / Google Workspace")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt5.png", width=300)
            
            
        with cols[1]:
            st.subheader("Career & Workplace Skills")
            st.markdown("- Interview Skills")
            st.markdown("- Resume Writing")
            st.markdown("- Workplace Etiquette & Professionalism")
            st.markdown("- Time Management & Organization")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt6.png", width=300)
            
            
        with cols[1]:
            st.subheader("Financial & Life Management Skills")
            st.markdown("- Basic Financial Literacy")
            st.markdown("- Budgeting & Saving")
            st.markdown("- Understanding Salaries, Tax, and Expenses")
            st.markdown("- Planning for Goals & Emergencies")

        st.markdown("---")

def live_user_onboard_dashboard():
    st.title("Welcome " + language_data.get("Rohan",{}).get(st.session_state.language,"Rohan"))
    st.markdown("---")


    tab1, tab2, tab3, tab4 = st.tabs([language_data.get("Profile",{}).get(st.session_state.language,"Profile"), language_data.get("Feed",{}).get(st.session_state.language,"Feed"), language_data.get("Alumini Network",{}).get(st.session_state.language,"Alumini Network"), language_data.get("Videos",{}).get(st.session_state.language,"Videos")])
    with tab1:
        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\Rohan.jpg", width=200)
            
        with cols[1]:
            st.subheader("Name: Rohan")
            st.subheader("Age: 21 Years")
            st.subheader("Address: H.No.132/4, Gandhi Road, Delhi")

        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="📚 Total Classes", value=10,border=True)

        with col2:
            st.metric(label="✅ Attended", value=8, border=True)

        with col3:
            st.metric(label="❌ Missed", value=2, border=True)

        st.markdown("---")

        
        
        


        st.header("Physical Test Score")
        physical_score = pd.DataFrame(
    {
        "Score Obtained": [14,18],
        "Max Score": [20,20],
        "Grade Obtained": ["B","A"],
    },
    index=["Week 1", "Week2"],
                                        )
        st.table(physical_score)

        st.markdown("---")
        st.header("Virtual Test Score")
        virtual_score = pd.DataFrame(
    {
        "Score Obtained": [10,18, 20],
        "Max Score": [20,20, 20],
        "Grade Obtained": ["C","A","A+"],
    },
    index=["Test 1", "Test 2", "Test 3"],
                                        )
        st.table(virtual_score)
        st.markdown("---")

        st.header("Likelihood of Attrition: 32%")
        st.markdown("---")

        

        
    with tab2:
        if st.session_state.language == "English":
            st.subheader("Aarav Mehta has been appointed today, 29 January 2026, with Starbucks, with a salary range of ₹15,000 - ₹17,000.")
            st.subheader("Sneha Raghavan has joined Reliance Trends today, 29 January 2026, with a salary package ranging from ₹18,000 to ₹ 20,000.")
            st.subheader("Rahul Chatterjee has joined IDBI Bank today, 29 January 2026, with a salary range of ₹23,000 - ₹25,000.")
            st.subheader("Kiran Deshpande has joined Teleperformance Solutions on 30 December 2025, with a salary range of ₹18,000 - ₹20,000.")
            st.subheader("Manoj Nambiar has joined TCS on 19 December 2025, with a salary range of ₹23,000 - ₹25,000.")
            st.subheader("Ishita Verma has joined McDonalds on 10 December 2025, with a salary range of ₹15,000 - ₹17,000.")

        elif st.session_state.language == "Hindi":
            st.subheader("आरव मेहता को आज, 29 जनवरी 2026 को Starbucks में नियुक्त किया गया है, जिनका वेतन पैकेज ₹15,000 - ₹17,000 है।")
            st.subheader("स्नेहा राघवन आज, 29 जनवरी 2026 को Reliance Trends से जुड़ी हैं, जिनका वेतन पैकेज ₹18,000 से ₹ 20,000 के बीच है।")
            st.subheader("राहुल चटर्जी आज, 29 जनवरी 2026 को IDBI Bank से जुड़े हैं, जिनका वेतन पैकेज ₹23,000 - ₹25,000 है।")
            st.subheader("किरण देशपांडे 30 दिसंबर 2025 को Teleperformance Solutions से जुड़े हैं, जिनका वेतनमान ₹18,000 - ₹20,000 है।")
            st.subheader("मनोज नायंबियार 19 दिसंबर 2025 को TCS से जुड़े हैं, जिनका वेतनमान ₹23,000 - ₹25,000 है।")
            st.subheader("इशिता वर्मा 10 दिसंबर 2025 को McDonalds से जुड़ी हैं, जिनका वेतनमान ₹15,000 - ₹17,000 है।")

        elif st.session_state.language == "Punjabi":
            st.subheader("ਆਰਵ ਮਹੇਤਾ ਨੂੰ ਅੱਜ, 29 ਜਨਵਰੀ 2026 ਨੂੰ Starbucks ਵਿੱਚ ਨਿਯੁਕਤ ਕੀਤਾ ਗਿਆ ਹੈ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹15,000 - ₹17,000 ਹੈ।")
            st.subheader("ਸਨੇਹਾ ਰਾਘਵਨ ਅੱਜ, 29 ਜਨਵਰੀ 2026 ਨੂੰ Reliance Trends ਨਾਲ ਜੁੜ ਗਈ ਹੈ, ਜਿਸਦੀ ਤਨਖ਼ਾਹ ₹18,000 ਤੋਂ ₹ 20,000 ਤੱਕ ਹੈ।")
            st.subheader("ਰਾਹੁਲ ਚੱਟਰਜੀ ਅੱਜ, 29 ਜਨਵਰੀ 2026 ਨੂੰ IDBI Bank ਨਾਲ ਜੁੜੇ ਹਨ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹23,000 - ₹25,000 ਹੈ।")
            st.subheader("ਕਿਰਨ ਦੇਸ਼ਪਾਂਡੇ 30 ਦਸੰਬਰ 2025 ਨੂੰ Teleperformance Solutions ਨਾਲ ਜੁੜੇ ਹਨ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹18,000 - ₹20,000 ਹੈ।")
            st.subheader("ਮਨੋਜ ਨਾਇੰਬਿਆਰ 19 ਦਸੰਬਰ 2025 ਨੂੰ TCS  ਨਾਲ ਜੁੜੇ ਹਨ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹23,000 - ₹25,000 ਹੈ।")
            st.subheader("ਇਸ਼ਿਤਾ ਵਰਮਾ 30 ਦਸੰਬਰ 2025 ਨੂੰ McDonalds ਨਾਲ ਜੁੜੀ ਹੈ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹15,000 - ₹17,000 ਹੈ।")

        elif st.session_state.language == "Kannada":
            st.subheader("ಆರವ್ ಮೇಹ್ತಾ ಅವರನ್ನು ಇಂದು, 29 ಜನವರಿ 2026 ರಂದು Starbucks ನಲ್ಲಿ ನೇಮಕ ಮಾಡಲಾಗಿದೆ, ಸಂಬಳ ಶ್ರೇಣಿಯು ₹15,000 - ₹17,000 ಆಗಿದೆ")
            st.subheader("ಸ್ನೇಹಾ ರಾಘವನ್ ಅವರು ಇಂದು, 29 ಜನವರಿ 2026 ರಂದು Reliance Trends ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಪ್ಯಾಕೇಜ್ ₹18,000 ರಿಂದ ₹ 20,000 ವರೆಗೆ ಇದೆ")
            st.subheader("ರಾಹುಲ್ ಚಟರ್ಜಿ ಅವರು ಇಂದು, 29 ಜನವರಿ 2026 ರಂದು IDBI Bank ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಶ್ರೇಣಿ ₹23,000 - ₹25,000 ಆಗಿದೆ")
            st.subheader("ಕಿರಣ್ ದೇಶಪಾಂಡೆ ಅವರು 30 ಡಿಸೆಂಬರ್ 2025 ರಂದು Teleperformance Solutions ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಶ್ರೇಣಿ ₹18,000 - ₹20,000 ಆಗಿದೆ")
            st.subheader("ಮನೋಜ್ ನಯ್ಯಂಬಿಯರ್ ಅವರು 19 ಡಿಸೆಂಬರ್ 2025 ರಂದು TCS ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಶ್ರೇಣಿ ₹23,000 - ₹25,000 ಆಗಿದೆ")
            st.subheader("ಇಶಿತಾ ವರ್ಮಾ ಅವರು 10 ಡಿಸೆಂಬರ್ 2025 ರಂದು McDonalds ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಶ್ರೇಣಿ ₹15,000 - ₹17,000 ಆಗಿದೆ")

    with tab3:
        if st.session_state.language == "English":
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p1.png", width=300)
                
                
            with cols[1]:
                st.subheader("Name: Vishwas")
                st.subheader("Employer: DMart")
                st.subheader("Age: 24 Years")
                st.subheader("Address PIN: 115733")
                st.subheader("Salary: 30,000")
            st.button("Connect",type ="primary",width  = "stretch")

            st.markdown("---")
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p2.png", width=300)
                
                
            with cols[1]:
                st.subheader("Name: Raghav")
                st.subheader("Employer: Reliance Trends")
                st.subheader("Age: 24 Years")
                st.subheader("Address PIN: 116793")
                st.subheader("Salary: 30,000")
            st.button("Connect",key= "hdsfydhf",type ="primary",width  = "stretch")

            st.markdown("---")
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p3.png", width=300)
                
                
            with cols[1]:
                st.subheader("Name: Abhinav")
                st.subheader("Employer: Lenskart")
                st.subheader("Age: 24 Years")
                st.subheader("Address PIN: 110093")
                st.subheader("Salary: 35,000")
            st.button("Connect",key= "hdsfydhfhdsw",type ="primary",width  = "stretch")

            st.markdown("---")

        if st.session_state.language == "Hindi":
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p3.png", width=300)
                
                
            with cols[1]:
                st.subheader("नाम : अभिनव")
                st.subheader("नियोक्ता : लेंसकार्ट")
                st.subheader("आयु : 24")
                st.subheader("पता पिन : 110093")
                st.subheader("वेतन : 35,000")
            st.button("Connect",key= "hdsfydhfss",type ="primary",width  = "stretch")

            st.markdown("---")

        if st.session_state.language == "Punjabi":
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p1.png", width=300)
                
                
            with cols[1]:
                st.subheader("ਨਾਂ : ਵਿਸ਼ਵਾਸ")
                st.subheader("ਨਿਯੋਤਾ : ਡੀਮਾਰਟ")
                st.subheader("ਉਮਰ : 24")
                st.subheader("ਪਤਾ ਪਿਨ : 115733")
                st.subheader("ਤਨਖਾਹ : 30,000")
            st.button("Connect",key= "hdsfydhfaaaaaa",type ="primary",width  = "stretch")

            st.markdown("---")

        if st.session_state.language == "Kannada":
            cols = st.columns([4, 6])
            with cols[0]:
                st.image("Data\Images\p2.png", width=300)
                
                
            with cols[1]:
                st.subheader("ಹೆಸರು: ರಾಘವ್")
                st.subheader("ನಿಯೋಜಕ: ರಿಲಾಯನ್ಸ್ ಟ್ರೆಂಡ್ಸ್")
                st.subheader("ವಯಸ್ಸು: 24")
                st.subheader("ವಿಳಾಸ ಪಿನ್: 116793")
                st.subheader("ತಡೆಯವರು: 30,000")
            st.button("Connect",key= "hdsfydssshf",type ="primary",width  = "stretch")

            st.markdown("---")

    with tab4:
        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt1.png", width=300)
            
            
        with cols[1]:
            st.subheader("Personal Development Skills")
            st.markdown("- Confidence Building")
            st.markdown("- Self‑awareness")
            st.markdown("- Emotional Intelligence")
            st.markdown("- Self‑discipline & Motivation")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt2.png", width=300)
            
            
        with cols[1]:
            st.subheader("Communication & People Skills")
            st.markdown("- Public Speaking")
            st.markdown("- Active Listening")
            st.markdown("- Teamwork & Collaboration")
            st.markdown("- Customer Service Skills")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt3.png", width=300)
            
            
        with cols[1]:
            st.subheader("Cognitive & Problem-Solving Skills")
            st.markdown("- Critical Thinking")
            st.markdown("- Logical Reasoning")
            st.markdown("- Decision‑making")
            st.markdown("- Creative Problem Solving")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt4.png", width=300)
            
            
        with cols[1]:
            st.subheader("Digital & Technical Skills")
            st.markdown("- Basic Computer Literacy")
            st.markdown("- Using Smartphones & Apps")
            st.markdown("- Email, Online Forms & Digital Payments")
            st.markdown("- Introduction to MS Office / Google Workspace")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt5.png", width=300)
            
            
        with cols[1]:
            st.subheader("Career & Workplace Skills")
            st.markdown("- Interview Skills")
            st.markdown("- Resume Writing")
            st.markdown("- Workplace Etiquette & Professionalism")
            st.markdown("- Time Management & Organization")

        st.markdown("---")

        cols = st.columns([4, 6])
        with cols[0]:
            st.image("Data\Images\\vt6.png", width=300)
            
            
        with cols[1]:
            st.subheader("Financial & Life Management Skills")
            st.markdown("- Basic Financial Literacy")
            st.markdown("- Budgeting & Saving")
            st.markdown("- Understanding Salaries, Tax, and Expenses")
            st.markdown("- Planning for Goals & Emergencies")

        st.markdown("---")

def admin_dashboard():
    st.title("Welcome " + st.session_state.username)
    st.markdown("---")

    st.title("Potential Hotspots")

    # -----------------------------
    # Load YOUR enriched file only
    # -----------------------------
    DATA_PATH = "Data\\rural_enrollment_india.csv"

    def load_table(path: str) -> pd.DataFrame:
        """Load CSV or Excel seamlessly."""
        ext = os.path.splitext(path.lower())[1]
        if ext in [".xlsx", ".xls"]:
            return pd.read_excel(path, engine="openpyxl")
        return pd.read_csv(path)

    df = load_table(DATA_PATH)

    # -----------------------------
    # Normalize & basic columns
    # -----------------------------
    def normalize_pincode(series: pd.Series) -> pd.Series:
        s = series.astype(str).str.extract(r"(\d+)")[0]
        return s.str[-6:]

    df["pincode_norm"] = normalize_pincode(df.get("pincode", ""))
    df["state"] = df.get("state", "").astype(str).str.strip()

    if "district" in df.columns:
        df["district"] = df["district"].astype(str).str.strip()
    elif "disctrict" in df.columns:
        df["district"] = df["disctrict"].astype(str).str.strip()
    else:
        df["district"] = ""

    df["past_enrolled"] = df.get("past_enrolled", "no").astype(str).str.lower().str.strip()

    # -----------------------------
    # Category labels (as requested)
    # -----------------------------
    def color_label(r):
        return "Target: people enrolled" if r["past_enrolled"] == "yes" else "Target: people not enrolled"

    df["color_label"] = df.apply(color_label, axis=1)

    # Legend colors
    color_map = {
        "Target: people not enrolled": "red",
        "Target: people enrolled": "green",
        "Data center": "blue",
    }

    # Icons (Maki symbols)
    def symbol_from_label(label: str) -> str:
        return {
            "Target: people not enrolled": "cross",
            "Target: people enrolled": "circle",
            "Data center": "marker",  # pin
        }.get(label, "marker")

    df["symbol"] = df["color_label"].map(symbol_from_label)

    # -----------------------------
    # BLUE centroid locations (always plotted)
    # -----------------------------
    centroids = pd.DataFrame([
        {
            "state": "Rajasthan",
            "district": "Alwar",
            "pincode_norm": "301001",
            "latitude": 27.560932,
            "longitude": 76.625015,
            "color_label": "Data center",
        },
        {
            "state": "Tamil Nadu",
            "district": "Madurai",
            "pincode_norm": "625001",
            "latitude": 9.9599655,
            "longitude": 78.1349839,
            "color_label": "Data center",
        },
    ])
    centroids["symbol"] = centroids["color_label"].map(symbol_from_label)

    # -----------------------------
    # Synthetic points near BLUE centroids (small donut)
    # -----------------------------
    def generate_random_points_near_centroid(centroid_row, n_min=20, n_max=30, r_min_deg=0.3, r_max_deg=0.4):
        n = np.random.randint(n_min, n_max + 1)

        center_lat = centroid_row["latitude"]
        center_lon = centroid_row["longitude"]
        state = centroid_row["state"]
        district = centroid_row["district"]
        pincode_base = centroid_row["pincode_norm"]

        angles = np.random.uniform(0, 2*np.pi, size=n)
        radii  = np.random.uniform(r_min_deg, r_max_deg, size=n)
        lat_offsets = radii * np.cos(angles)
        lon_offsets = radii * np.sin(angles)

        n_green = n // 2
        n_red   = n - n_green
        enrolled_flags = np.array(["yes"] * n_green + ["no"] * n_red)
        np.random.shuffle(enrolled_flags)

        pincode_synth = [pincode_base[:3] + f"{np.random.randint(0, 999):03d}" for _ in range(n)]

        df_rand = pd.DataFrame({
            "state": state,
            "district": district,
            "pincode_norm": pincode_synth,
            "latitude": center_lat + lat_offsets,
            "longitude": center_lon + lon_offsets,
            "past_enrolled": enrolled_flags,
        })
        df_rand["color_label"] = df_rand["past_enrolled"].map(
            lambda x: "Target: people enrolled" if x == "yes" else "Target: people not enrolled"
        )
        df_rand["symbol"] = df_rand["color_label"].map(symbol_from_label)
        return df_rand

    rand_alwar   = generate_random_points_near_centroid(centroids.iloc[0])
    rand_madurai = generate_random_points_near_centroid(centroids.iloc[1])
    df_random_near_blue = pd.concat([rand_alwar, rand_madurai], ignore_index=True)

    # -----------------------------
    # EXTRA: Red-only SCATTER clusters (NO donut)
    # -----------------------------
    def generate_red_points_scatter(*, center_lat, center_lon, state, district, pincode_base,
                                    n_min=30, n_max=40, std_km_lat=60, std_km_lon=95) -> pd.DataFrame:
        n = np.random.randint(n_min, n_max + 1)
        km_per_deg_lat = 111.0
        km_per_deg_lon_equator = 111.0
        scale_lon = np.cos(np.deg2rad(center_lat)) or 1.0

        std_deg_lat = std_km_lat / km_per_deg_lat
        std_deg_lon = (std_km_lon / km_per_deg_lon_equator) / scale_lon

        lat_offsets = np.random.normal(loc=0.0, scale=std_deg_lat, size=n)
        lon_offsets = np.random.normal(loc=0.0, scale=std_deg_lon, size=n)

        pincode_synth = [pincode_base[:3] + f"{np.random.randint(0, 999):03d}" for _ in range(n)]

        df_red = pd.DataFrame({
            "state": state,
            "district": district,
            "pincode_norm": pincode_synth,
            "latitude": center_lat + lat_offsets,
            "longitude": center_lon + lon_offsets,
            "past_enrolled": "no",
            "color_label": "Target: people not enrolled",
        })
        df_red["symbol"] = df_red["color_label"].map(symbol_from_label)
        return df_red

    def generate_red_points_scatter2(*, center_lat, center_lon, state, district, pincode_base,
                                    n_min=20, n_max=30, std_km_lat=100, std_km_lon=120) -> pd.DataFrame:
        n = np.random.randint(n_min, n_max + 1)
        km_per_deg_lat = 111.0
        km_per_deg_lon_equator = 111.0
        scale_lon = np.cos(np.deg2rad(center_lat)) or 1.0

        std_deg_lat = std_km_lat / km_per_deg_lat
        std_deg_lon = (std_km_lon / km_per_deg_lon_equator) / scale_lon

        lat_offsets = np.random.normal(loc=0.0, scale=std_deg_lat, size=n)
        lon_offsets = np.random.normal(loc=0.0, scale=std_deg_lon, size=n)

        pincode_synth = [pincode_base[:3] + f"{np.random.randint(0, 999):03d}" for _ in range(n)]

        df_red = pd.DataFrame({
            "state": state,
            "district": district,
            "pincode_norm": pincode_synth,
            "latitude": center_lat + lat_offsets,
            "longitude": center_lon + lon_offsets,
            "past_enrolled": "no",
            "color_label": "Target: people not enrolled",
        })
        df_red["symbol"] = df_red["color_label"].map(symbol_from_label)
        return df_red

    extra_red_specs = [
        dict(center_lat=23.0225, center_lon=72.5714, state="Gujarat",       district="Ahmedabad",       pincode_base="380001"),
        dict(center_lat=23.1815, center_lon=79.9864, state="Madhya Pradesh", district="Jabalpur",        pincode_base="482001"),
        dict(center_lat=12.9716, center_lon=77.5946, state="Karnataka",      district="Bengaluru Urban", pincode_base="560001"),
    ]
    extra_red_specs2 = [
        dict(center_lat=23.3441, center_lon=85.3096, state="Jharkhand", district="Ranchi", pincode_base="834001"),
        dict(center_lat=28.6139, center_lon=77.2090, state="Delhi",       district="New Delhi", pincode_base="110001"),
        dict(center_lat=17.3850, center_lon=78.4867, state="Telangana",   district="Hyderabad", pincode_base="500001"),
    ]

    df_more_red_clusters = []
    for spec in extra_red_specs:
        df_more_red_clusters.append(generate_red_points_scatter(**spec))
    for spec in extra_red_specs2:
        df_more_red_clusters.append(generate_red_points_scatter2(**spec))
    df_more_red = pd.concat(df_more_red_clusters, ignore_index=True)

    df_random_near_blue = pd.concat([df_random_near_blue, df_more_red], ignore_index=True)

    # -----------------------------
    # Sanity checks before plotting
    # -----------------------------
    required_cols = ["latitude", "longitude", "district", "state", "pincode_norm", "color_label", "symbol"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"Dataframe 'df' is missing required columns: {missing}\n"
            f"Use an enriched file that includes latitude & longitude per pincode."
        )

    # -----------------------------
    # HEATMAP + layered points
    # -----------------------------
    fig = px.density_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        radius=1,
        center=dict(lat=22.35, lon=79.0),
        zoom=4,
        hover_name="district",
        height=800,
    )

    # Base points: legend should show for these (red+green)
    fig_points = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="color_label",
        color_discrete_map=color_map,
        # symbol="symbol",   # << enable icons
        custom_data=["state", "district", "pincode_norm", "color_label", "past_enrolled"],
    )
    for tr in fig_points.data:
        tr.name = tr.customdata[0][3]  # "Target: people enrolled" / "Target: people not enrolled"
        tr.legendgroup = tr.name
        tr.showlegend = True

    # Blue centroids: legend should show for this (blue)
    fig_blue = px.scatter_mapbox(
        centroids,
        lat="latitude",
        lon="longitude",
        color="color_label",
        color_discrete_map=color_map,
        # symbol="symbol",   # << enable icons
        custom_data=["state", "district", "pincode_norm", "color_label"],
    )
    for tr in fig_blue.data:
        tr.name = "Data center"        # legend label
        tr.legendgroup = "Data center"
        tr.showlegend = True

    # Random/extra: legend should NOT show (avoid duplicates for red+green)
    fig_rand = px.scatter_mapbox(
        df_random_near_blue,
        lat="latitude",
        lon="longitude",
        color="color_label",
        color_discrete_map=color_map,
        # symbol="symbol",   # << enable icons
        custom_data=["state", "district", "pincode_norm", "color_label", "past_enrolled"],
    )
    for tr in fig_rand.data:
        tr.name = tr.customdata[0][3]
        tr.legendgroup = tr.name
        tr.showlegend = False   # hide duplicates in legend

    fig.data[0].showscale = False  # hide vertical heatmap color bar
    fig.update_layout(coloraxis_showscale=False)  # safet
    # -----------------------------
    # Add traces & clean hovers
    # -----------------------------
    def set_hover_points(t):
        t.hovertemplate = (
            "<b>%{customdata[1]}</b><br>"
            "State: %{customdata[0]}<br>"
            "Pincode: %{customdata[2]}<br>"
            "Category: %{customdata[3]}<br>"
            "Past enrolled: %{customdata[4]}<br>"
            "<extra></extra>"
        )

    def set_hover_blue(t):
        t.hovertemplate = (
            "<b>%{customdata[1]}</b><br>"
            "State: %{customdata[0]}<br>"
            "Pincode: %{customdata[2]}<br>"
            "Category: %{customdata[3]}<br>"
            "<extra></extra>"
        )

    def set_hover_rand(t):
        t.hovertemplate = (
            "<b>%{customdata[1]}</b><br>"
            "State: %{customdata[0]}<br>"
            "Pincode: %{customdata[2]}<br>"
            "Category: %{customdata[3]}<br>"
            "Past enrolled: %{customdata[4]}<br>"
            "<extra></extra>"
        )

    for t in fig_points.data:
        set_hover_points(t)
        fig.add_trace(t)

    for t in fig_blue.data:
        set_hover_blue(t)
        t.marker.update(size=18, opacity=1.0, allowoverlap=True)
        fig.add_trace(t)

    for t in fig_rand.data:
        set_hover_rand(t)
        t.marker.update(size=9, opacity=0.9)
        fig.add_trace(t)

    # -----------------------------
    # REMOVE the vertical heatmap color bar (densitymapbox)
    # -----------------------------
    for tr in fig.data:
        if getattr(tr, "type", "") == "densitymapbox":   # only the heatmap layer
            tr.showscale = False

    # -----------------------------
    # Layout
    # -----------------------------
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center=dict(lat=22.35, lon=79.0),
        margin=dict(l=0, r=0, t=40, b=0),
        legend_title="Legend",)


    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Summary metrics
    # -----------------------------
    df["latlon_key"] = df["latitude"].astype(str) + "_" + df["longitude"].astype(str)
    df_random_near_blue["latlon_key"] = (
        df_random_near_blue["latitude"].astype(str) + "_" + df_random_near_blue["longitude"].astype(str)
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mapped rows", len(df))
    c2.metric("Unique lat-lon points", df["latlon_key"].nunique())
    c3.metric("Centroid markers (Data centers)", len(centroids))
    c4.metric("Synthetic points near blue", len(df_random_near_blue))

    ########################################################################################################

    #df = pd.read_csv("Data\\rural_india_bpl_data.csv")


    st.title("Target Audience Visualization (18-25 & BPL)")

    # ---------------------------------------------
    # Load data
    # ---------------------------------------------
    CSV_PATH = "Data\\rural_india_bpl_data.csv"
    if not os.path.exists(CSV_PATH):
        st.error(f"CSV not found: {CSV_PATH}")
        st.stop()

    # Use low_memory=False to avoid mixed-type splits across chunks
    df_raw = pd.read_csv(CSV_PATH, low_memory=False)

    # ---------------------------------------------
    # Utilities
    # ---------------------------------------------
    def normalize_gender(x):
        if pd.isna(x):
            return "Unknown"
        s = str(x).strip().lower()
        if s in {"m", "male", "man", "boy"}:
            return "Male"
        if s in {"f", "female", "woman", "girl"}:
            return "Female"
        if s in {"other", "non-binary", "nonbinary", "nb", "o"}:
            return "Other"
        # Fallback
        t = str(x).strip().title()
        return t if t in {"Male", "Female", "Other"} else "Unknown"

    def to_bool_bpl(x):
        """
        Convert BPL tags to boolean: accepts True/False, 1/0, yes/no, y/n, strings like 'true'.
        """
        if pd.isna(x):
            return False
        if isinstance(x, (bool, np.bool_)):
            return bool(x)
        # numeric-like
        if isinstance(x, (int, float)) and not pd.isna(x):
            try:
                return bool(int(x))
            except Exception:
                pass
        s = str(x).strip().lower()
        truthy = {"true", "yes", "y", "1", "t"}
        falsy  = {"false", "no", "n", "0", "f"}
        if s in truthy:
            return True
        if s in falsy:
            return False
        return False

    def coalesce_col(df, candidates, create=False, default=None):
        """
        Return the first column name from `candidates` that exists in df.
        Optionally create the first name if none exist.
        """
        for c in candidates:
            if c in df.columns:
                return c
        if create:
            df[candidates[0]] = default
            return candidates[0]
        return None

    # ---------------------------------------------
    # Make a working copy; normalize & Arrow-proof
    # ---------------------------------------------
    df = df_raw.copy()

    # Ensure all object columns are Arrow-friendly strings (not Python objects)
    # We keep numerics as numerics; convert only true 'object' dtypes.
    obj_cols = df.select_dtypes(include=["object"]).columns.tolist()
    for col in obj_cols:
        # Convert to pandas StringDtype to preserve missing values as <NA>
        df[col] = df[col].astype("string").str.strip()

    # ----- Gender -----
    if "Gender" not in df.columns:
        df["Gender"] = pd.Series(pd.NA, index=df.index, dtype="string")
    df["Gender"] = df["Gender"].apply(normalize_gender).astype("string")

    # ----- Age -----
    age_col = coalesce_col(df, ["Age", "current_age"], create=True, default=np.nan)
    df[age_col] = pd.to_numeric(df[age_col], errors="coerce")

    # ----- District / State / Pincode -----
    if "District" not in df.columns:
        df["District"] = pd.Series("Unknown", index=df.index, dtype="string")
    if "state" not in df.columns:
        df["state"] = pd.Series("Unknown", index=df.index, dtype="string")

    # Title-case for nicer labels (avoid title-case for pin codes)
    df["District"] = df["District"].fillna("Unknown").astype("string").str.strip().str.title()
    df["state"] = df["state"].fillna("Unknown").astype("string").str.strip().str.title()

    # Pincode: keep as string for display/grouping; pad if numeric-like
    if "Pincode" not in df.columns:
        df["Pincode"] = pd.Series(pd.NA, index=df.index, dtype="string")
    df["Pincode"] = (
        df["Pincode"]
        .astype("string")
        .str.replace(r"\.0+$", "", regex=True)  # strip trailing .0 if came from Excel
        .str.strip()
    )
    # If looks numeric and length <= 6, left-pad to 6 digits
    df["Pincode"] = df["Pincode"].apply(
        lambda s: s.zfill(6) if (isinstance(s, str) and s.isdigit() and len(s) <= 6) else s
    ).astype("string")

    # ----- BPL boolean (handle multiple possible names) -----
    bpl_candidates = [
        "BPL_tag (income below 3 Lakh)",
        "BPL_tag",
        "BPL",
        "is_BPL",
        "bpl",
    ]
    bpl_col = coalesce_col(df, bpl_candidates, create=True, default="no")
    df[bpl_col] = df[bpl_col].apply(to_bool_bpl)

    # ----- Enrollment (past_enrolled_in_magic_bus / past_enrolled) -----
    enroll_col = coalesce_col(df, ["past_enrolled_in_magic_bus", "past_enrolled"], create=True, default="no")
    df[enroll_col] = (
        df[enroll_col]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({"y": "yes", "true": "yes", "1": "yes", "n": "no", "false": "no", "0": "no"})
    )
    df["enrolled_label"] = np.where(df[enroll_col] == "yes", "Target: people enrolled", "Target: people not enrolled")

    # ----- Family size & head-of-family -----
    if "no_of_family_members" in df.columns:
        df["no_of_family_members"] = pd.to_numeric(df["no_of_family_members"], errors="coerce")
    else:
        df["no_of_family_members"] = np.nan

    if "is_head_of_family" in df.columns:
        df["is_head_of_family"] = (
            df["is_head_of_family"]
            .astype("string").str.strip().str.lower()
            .replace({"y": "yes", "true": "yes", "1": "yes", "n": "no", "false": "no", "0": "no"})
            .isin(["yes"])
        )
    else:
        df["is_head_of_family"] = False

    # ----- Data recency -----
    if "last_govt_data_updated_on" in df.columns:
        df["last_govt_data_updated_on"] = pd.to_datetime(df["last_govt_data_updated_on"], errors="coerce")
        df["days_since_update"] = (pd.Timestamp("today").normalize() - df["last_govt_data_updated_on"]).dt.days

    # ---------------------------------------------
    # Data Quality Snapshot (Arrow-safe)
    # ---------------------------------------------
    # st.subheader("Data Quality Snapshot")
    # st.write("**Columns detected:**", list(df.columns))

    # # Build an Arrow-compatible dtypes table
    # dtypes_df = pd.DataFrame({
    #     "column": df.columns,
    #     "dtype": df.dtypes.astype(str).values,   # <-- critical: stringify dtypes for Arrow
    # })
    # st.dataframe(dtypes_df, use_container_width=True)

    # ---------------------------------------------
    # Filter to target cohort: Age 18–25 and BPL True
    # ---------------------------------------------
    target_mask = df[age_col].between(18, 25, inclusive="both") & (df[bpl_col] == True)
    df_target = df.loc[target_mask].copy()

    st.info(f"Total records: {len(df):,} | Target cohort (18–25 & <3L): {len(df_target):,}")

    # Use only the target cohort below
    df = df_target

    if df.empty:
        st.warning("No rows match the target cohort (18–25 ). Adjust your filters or check the data.")
        st.stop()

    # ---------------------------------------------
    # KPIs
    # ---------------------------------------------
    total = len(df)
    pct_female   = round(df["Gender"].eq("Female").mean() * 100, 1)
    pct_male=round(df["Gender"].eq("Male").mean() * 100, 1)
    pct_bpl      = round(df[bpl_col].mean() * 100, 1)  # should be 100% after filter, still safe
    pct_enrolled = round(df["enrolled_label"].eq("Target: people enrolled").mean() * 100, 1)
    med_famsz    = df["no_of_family_members"].median()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total youths (18–25)", total)
    c2.metric("% Female", f"{pct_female}%")
    c3.metric("% Male", f"{pct_male}%")
    c4.metric("% Enrolled", f"{pct_enrolled}%")
    c5.metric("Median family size", f"{med_famsz:.0f}" if pd.notna(med_famsz) else "—")

    # ---------------------------------------------
    # Visualizations
    # ---------------------------------------------

    # 1) Gender donut
    fig_gender = px.pie(df, names="Gender", title="Gender composition", hole=0.45)
    st.plotly_chart(fig_gender, use_container_width=True)

    # 2) Enrollment rate by Gender (bar)
    enroll_rate_gender = (
        df.groupby("Gender")["enrolled_label"]
        .apply(lambda s: (s == "Target: people enrolled").mean())
        .reset_index(name="rate")
    )
    fig_enroll_gender = px.bar(
        enroll_rate_gender, x="Gender", y="rate",
        text=(enroll_rate_gender["rate"] * 100).round(1),
        labels={"rate": "Enrollment rate"},
        title="Enrollment rate by gender"
    )
    fig_enroll_gender.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_enroll_gender.update_yaxes(tickformat=".0%", range=[0, 1])
    st.plotly_chart(fig_enroll_gender, use_container_width=True)

    # 3) Top 10 districts by youth count
    top_districts = (
        df.groupby(["state", "District"]).size().reset_index(name="count")
        .sort_values("count", ascending=False).head(10)
    )
    fig_top_districts = px.bar(
        top_districts, x="count", y="District", color="state",
        title="Top 10 districts by youth count", orientation="h"
    )
    st.plotly_chart(fig_top_districts, use_container_width=True)

    # 4) District × Enrollment rate heatmap
    rate_by_dist = (
        df.assign(val=(df["enrolled_label"] == "Target: people enrolled").astype(int))
        .groupby(["state", "District"])["val"].mean().reset_index(name="enroll_rate")
    )
    fig_heat = px.density_heatmap(
        rate_by_dist, x="state", y="District", z="enroll_rate",
        histfunc="avg",
        color_continuous_scale="Blues", title="Enrollment rate by district"
    )
    fig_heat.update_coloraxes(colorbar_title="Rate")
    fig_heat.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_heat, use_container_width=True)

    # 5) State→District treemap sized by audience, colored by rate
    size_col = "BPL_ID" if "BPL_ID" in df.columns else None
    treedata = (
        df.assign(enrolled=(df["enrolled_label"] == "Target: people enrolled").astype(int))
        .groupby(["state", "District"])
        .agg(n=(size_col if size_col else "Gender", "count"), rate=("enrolled", "mean"))
        .reset_index()
    )
    fig_tree = px.treemap(
        treedata, path=["state", "District"], values="n", color="rate",
        color_continuous_scale="Blues", title="Audience size (area) & enrollment rate (color)"
    )
    fig_tree.update_coloraxes(colorbar_title="Enroll rate")
    st.plotly_chart(fig_tree, use_container_width=True)



    # if "BPL_ID" in df.columns:
    #     dup_cnt = df["BPL_ID"].duplicated().sum()
    #     if dup_cnt > 0:
    #         st.warning(f"Duplicate BPL_ID rows in target cohort: {dup_cnt}")
    #     else:
    #         st.success("No duplicate BPL_ID in target cohort.")
    # else:
    #     st.info("Column 'BPL_ID' not present; duplicate check skipped.")

    # ---------------------------------------------
    # Done
    # ---------------------------------------------
    # st.success("Dashboard rendered successfully.")

    # ABove Mansi Code
    ###########################################################################
    df = pd.read_csv('Data\\rural_india_bpl_data.csv')
    df.columns = df.columns.str.lower()
    # Convert to lowercase safely
    df['past_enrolled_in_magic_bus'] = df['past_enrolled_in_magic_bus'].str.strip().str.lower()

    # Boolean flags
    df['target_audience'] = ((df['current_age'] >= 18) & (df['current_age'] <= 25)).astype(int)

    df['already_enrolled'] = (df['past_enrolled_in_magic_bus'] == 'yes').astype(int)

    df['already_enrolled_overlap'] = (
        (df['current_age'] >= 18) &
        (df['current_age'] <= 25) &
        (df['past_enrolled_in_magic_bus'] == 'yes')
    ).astype(int)

    df['potential_target'] = df['target_audience'] - df['already_enrolled_overlap']

    c1, c2 = st.columns([4, 1])
    with c1:
        stats = df.groupby('pincode', dropna=False).agg(
            target_audience=('target_audience', 'sum'),
            already_enrolled=('already_enrolled_overlap', 'sum'),
            potential_target=('potential_target', 'sum'),
            total_population=('pincode', 'size')
        ).reset_index().sort_values(by = "potential_target", ascending = False).head(5)
        #st.dataframe(stats)
        st.data_editor(stats, row_height = 90, height = 460,hide_index = True, disabled = list(stats.columns))

    with c2:
        st.write("Mobilizer Name")
        # st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        option = st.selectbox(label = "",label_visibility = "hidden",options= ["Aman","Rahul","Anjali"],placeholder = "Select Mobilizer")
        option = st.selectbox(label = "",label_visibility = "hidden",options= ["Shagun","Srishti","Arun"],placeholder = "Select Mobilizer")
        option = st.selectbox(label = "",label_visibility = "hidden",options= ["Shivani","Naina","Neha"],placeholder = "Select Mobilizer")
        option = st.selectbox(label = "",label_visibility = "hidden",options= ["Sneha","Rishi","Raghav"],placeholder = "Select Mobilizer")
        option = st.selectbox(label = "",label_visibility = "hidden",options= ["Riya","Rahul","Anjali"],placeholder = "Select Mobilizer")

    st.button("Submit",key="login_button_1276",type ="primary",width  = "stretch")
    
    

    





    def plot_gender_distribution_by_pincode(df, pincode):
        """
        Generates a pie chart of Male vs Female population 
        within the potential target audience for a given pincode.
        """
        
        # Filter dataset for the specific pincode AND potential target = 1
        subset = df[(df['pincode'] == pincode) & (df['potential_target'] == 1)]
        
        if subset.empty:
            print(f"No potential target data found for pincode {pincode}")
            return
        
        # Count male/female
        gender_counts = subset['gender'].str.strip().str.lower().value_counts()
        
        color_map = {
            "male": "#4F81BD",     # Blue  
            "female": "#C0504D"    # Red
        }
        
        # Map each label to the correct color
        colors = [color_map[g] for g in gender_counts.index]

        # plt.figure(figsize=(6,6))
        
        # plt.pie(
        #     gender_counts,
        #     labels=[g.title() for g in gender_counts.index],
        #     autopct='%1.1f%%',
        #     colors=colors,
        #     startangle=90
        # )
        
        # plt.title(f"Gender Distribution (Potential Target) – Pincode {pincode}")
        # plt.axis('equal')
        # plt.show()

        
        fig, ax = plt.subplots(figsize=(6, 6))

        ax.pie(
            gender_counts,
            labels=[g.title() for g in gender_counts.index],
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )

        ax.set_title(f"Gender Distribution (Potential Target) – Pincode {pincode}")
        ax.axis('equal')  # Ensures pie is drawn as a circle

        # Render in Streamlit
        st.pyplot(fig)


    plot_gender_distribution_by_pincode(df, 502075)

    plot_gender_distribution_by_pincode(df, 685862)


# def mob_dashboard():
#     st.title("Welcome " + st.session_state.username)
#     st.markdown("---")




def mob_dashboard():
    st.title("Welcome " + st.session_state.username)
    st.markdown("---")

    

    st.header("Registration Tracker")
    st.caption("PIN Address: 201388")
    # st.session_state.hard_init
    # if not st.session_state.hard_init:
        
    #     st.session_state.elig_cand = 480
    #     st.session_state.total_regs = 120
    #     st.session_state.reg_done = 0

    #     st.session_state.hard_init = True
    st.session_state.elig_cand = 156
    st.session_state.total_regs = 120
    st.session_state.reg_done = 0

    
# Pull locals from session so they're always defined
    elig_cand = st.session_state.get("elig_cand", 156)
    total = st.session_state.get("total_regs", 120)
    reg_done = st.session_state.get("reg_done",0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Eligible Candidates", value=elig_cand,border=True)

    with col2:
        st.metric(label="Total Registrations", value=total,border=True)

    with col3:
        st.metric(label="Registrations Done", value=reg_done, border=True)

    st.markdown("---")

    # --- Persistent TOTAL via session_state ---
    if "TOTAL" not in st.session_state:
        st.session_state.TOTAL = 120  # initial value

    # --- Keys for all widgets so we can reset them cleanly ---
    
    if "FIELD_KEYS" not in st.session_state or not st.session_state.soft_init:
        st.session_state.FIELD_KEYS = {
            "name": "name",
            "age": "age",
            "gender": "gender",
            "pursuing": "pursuing",
            "employed": "employed",
            "income": "income",
            "highest_edu": "highest_edu",
            "family_members": "family_members",
            "ready_toggle": "ready_toggle",
            "confidence": "confidence",
        }
        st.session_state.soft_init = True

    FIELD_KEYS = st.session_state.FIELD_KEYS




    # --- Screening flags ---
    triggered, reason = False, ""

    # 1) Name
    name = st.text_input("Name", key=FIELD_KEYS["name"])

    # 2) Age
    age = st.number_input("Age", min_value=0, step=1, format="%d", key=FIELD_KEYS["age"])
    if age > 0 and not triggered:
        if not (18 <= age <= 25):
            triggered, reason = True, "Age not in 18–25"

    # 3) Gender (only if not triggered and age provided)
    if not triggered and age > 0:
        gender = st.selectbox("Gender", ["— Select —", "Male", "Female", "Other"], key=FIELD_KEYS["gender"])
    else:
        gender = None

    # 4) Pursuing Studies (stop if Yes)
    if not triggered and gender and gender != "— Select —":
        pursuing = st.selectbox("Pursuing Studies", ["— Select —", "No", "Yes"], key=FIELD_KEYS["pursuing"])
        if pursuing == "Yes":
            triggered, reason = True, "Pursuing Studies == Yes"
    else:
        pursuing = None

    # 5) Employment Status (stop if Employed)
    if not triggered and pursuing == "No":
        employed = st.selectbox("Employment Status", ["— Select —", "No", "Yes"], key=FIELD_KEYS["employed"])
        if employed == "Yes":
            triggered, reason = True, "Person is employed"
    else:
        employed = None

    # 6) Income (stop if > 300000)
    if not triggered and employed == "No":
        income = st.number_input("Income (annual)", min_value=0, step=1000, format="%d", key=FIELD_KEYS["income"])
        if income > 300000:
            triggered, reason = True, "Income > 300000"
    else:
        income = 0

    # 7) Highest Education + 8) Number of family members (only if still eligible flow)
    highest_edu = None
    family_members = None
    if not triggered and employed == "No" and income <= 300000 and pursuing == "No":
        highest_edu = st.text_input("Highest Education", key=FIELD_KEYS["highest_edu"])
        family_members = st.number_input(
            "Number of family members", min_value=0, step=1, format="%d", key=FIELD_KEYS["family_members"]
        )

    # --- Eligibility: No disqualifying condition met yet and fields complete ---
    eligible = (
        not triggered
        and age > 0
        and gender is not None
        and gender != "— Select —"
        and pursuing == "No"
        and employed == "No"
        and income <= 300000
        and highest_edu is not None
        and highest_edu.strip() != ""
        and family_members is not None
    )

    # --- NEW: Row with a switch and a Confidence Range dropdown (side-by-side) ---
    # Place this near the submission area.
    c1, c2 = st.columns([1, 1])
    with c1:
        ready_to_submit = st.toggle("Ready to submit", value=False, key=FIELD_KEYS["ready_toggle"], disabled=not eligible)
    with c2:
        # Confidence dropdown appears next to the switch; enabled only when eligible
        confidence_options = ["— Select —", "High", "Medium", "Low"]
        confidence = st.selectbox(
            "Confidence Range",
            confidence_options,
            key=FIELD_KEYS["confidence"],
            disabled=not eligible
        )

    # --- Remaining cases preview rule ---
    # If ANY condition is met (triggered) OR fully eligible, preview Remaining = Total - 1; else Remaining = Total
    total_cases = st.session_state.TOTAL
    remaining = total_cases - 1 if (eligible or triggered) else total_cases

    # st.markdown(f"**Total cases:** {total_cases}")
    # st.markdown(f"**Remaining cases:** {remaining}")

    # --- Status ---
    if triggered:
        st.info(f"Stopped early — condition met: **{reason}**")
        st.session_state.elig_cand = st.session_state.elig_cand - 1
        
        
    # else:
    #     st.success("No disqualifying condition met yet.")

    # --- Submit button (disabled unless eligible) ---
    # Optionally, you can also require 'ready_to_submit' and a selected confidence:
    require_toggle = True
    require_confidence = True
    has_confidence = (confidence if 'confidence' in locals() else None) and (confidence != "— Select —")

    submit_enabled = eligible and (
        (not require_toggle or ready_to_submit) and (not require_confidence or has_confidence)
    )

    def reset_form_state():
        
        for k in FIELD_KEYS.values():
            if k in st.session_state:
                del st.session_state[k]

    # --- On submit: decrement TOTAL and full reset for new user ---
    if st.button("Submit"):
        st.success("Form Submitted Successfully!!!")
        st.success("The Generated Unique User ID is 1098.")
        st.session_state.total_regs = st.session_state.get("total_regs", 120) -1
        st.session_state.reg_done = st.session_state.get("reg_done", 120) +1
        
        c1, c2 = st.columns([1, 1])
        with c1:
            op = st.button("Register Another Candidate",key="login_button_12",type ="primary",width  = "stretch")

        with c2:
            if st.button("Log Out",key="login_button_123",type ="primary",width  = "stretch"):
                pass
        #         st.markdown("jdsghsd")
                
        #         triggered, reason = False, ""
        #         st.session_state.mob_login = False
        #         st.session_state.mob_user_login = False
        #         st.rerun()
        
        # triggered, reason = False, ""
        # st.session_state.mob_login = False
        # st.session_state.mob_user_login = False
        # st.rerun()
        
        
        

    
def router():
    if st.session_state.adol_prog or st.session_state.live_prog or st.session_state.admin_login or st.session_state.mob_login:
        if st.session_state.live_user_login and st.session_state.username == "1121":
            live_user_onboard_dashboard()
            return
        elif st.session_state.live_user_login:
            live_user_dashboard()
            return
        elif st.session_state.admin_user_login:
            admin_dashboard()
            return
        elif st.session_state.mob_user_login:
            mob_dashboard()
            return
        else:
            login_page()
            return
    else:
        main_page()
        return

router()

