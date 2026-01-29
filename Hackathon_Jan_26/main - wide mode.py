import streamlit as st
import time

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




def main_page():


    cols = st.columns([0.5,4,0.56])
    with cols[0]:
        st.session_state.language = st.selectbox("Language",("English", "Hindi", "Punjabi", "Kannada"),)
        
    with cols[2]:
        if st.button("Admin Login"):
            st.session_state.admin_login = True
        
    cols = st.columns([4,0.5])
    
    with cols[1]:
    
        if st.button("Mobilizer Login"):
            st.session_state.mob_login = True




    # 3.1. Logo (centered)
    cols = st.columns([1.3, 1, 1])
    with cols[1]:
        st.image("Data\Images\Magic-Bus-Logo.png", width=200)

    
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        st.markdown(
            """
    <h1 style="color:white; font-size:64px;">
        The <span style="color:red;">Magic</span> starts here
    </h1>
    """,
    unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("")
    cols = st.columns([0.6,1,1.2,1, 1])
    with cols[1]:
        st.image("Data\Images\program_adol_prog.png", width=400)

    with cols[3]:
        st.image("Data\Images\program_live_prog.png", width=400)




    ### adding button
    cols = st.columns([0.54,1,1.2,1, 1])
    with cols[1]:
        st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            background-color: #FFBD05;  /* yellow hex */
            color: red;
            width: 400px;
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

        

        if st.button("Adolescent Program"):
            st.session_state.adol_prog = True


    with cols[3]:
        st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            background-color: #FFBD05;  /* yellow hex */
            color: red;
            width: 400px;
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

        

        if st.button("Livelihood Program"):
            st.session_state.live_prog = True

    st.rerun()

        
def login_page() :
    if st.session_state.adol_prog:
        pass

    elif st.session_state.live_prog:
        cols = st.columns([6, 0.1])
        with cols[0]:
            st.image("Data\Images\live_prog_banner.png", width=2000)

        cols = st.columns([8, 4])
        with cols[1]:
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.title("Enter your Credentials", text_alignment= "center" )
            username = st.text_input(label="", placeholder="Enter Username", key="username_input")
            password = st.text_input(label="", placeholder="Enter Password", type="password", key="password_input")

            if st.button("Login", key="login_button", type ="primary",width  = "stretch"):
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
        cols = st.columns([4,4,4])
        
        with cols[1]:
            st.title("Enter your Credentials", text_alignment= "center" )
            username = st.text_input(label="", placeholder="Enter Username", key="username_input")
            password = st.text_input(label="", placeholder="Enter Password", type="password", key="password_input")

            if st.button("Login", key="login_button",type ="primary",width  = "stretch"):
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
    st.title("Welcome " + st.session_state.username)
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Feed", "Alumini Network", "Videos"])
    with tab1:
        if st.session_state.language == "English":
            st.subheader("Aarav Mehta has been appointed today, 29 January 2026, with Starbucks, with a salary range of ₹15,000 - ₹17,000.")
            st.subheader("Sneha Raghavan has joined Reliance Trends today, 29 January 2026, with a salary package ranging from ₹18,000 to ₹ 20,000.")
            st.subheader("Rahul Chatterjee has joined IDBI Bank today, 29 January 2026, with a salary range of ₹23,000 - ₹25,000.")
        
        elif st.session_state.language == "Hindi":
            st.subheader("आरव मेहता को आज, 29 जनवरी 2026 को Starbucks में नियुक्त किया गया है, जिनका वेतन पैकेज ₹15,000 - ₹17,000 है।")
            st.subheader("स्नेहा राघवन आज, 29 जनवरी 2026 को Reliance Trends से जुड़ी हैं, जिनका वेतन पैकेज ₹18,000 से ₹ 20,000 के बीच है।")
            st.subheader("राहुल चटर्जी आज, 29 जनवरी 2026 को IDBI Bank से जुड़े हैं, जिनका वेतन पैकेज ₹23,000 - ₹25,000 है।")

        elif st.session_state.language == "Punjabi":
            st.subheader("ਆਰਵ ਮਹੇਤਾ ਨੂੰ ਅੱਜ, 29 ਜਨਵਰੀ 2026 ਨੂੰ Starbucks ਵਿੱਚ ਨਿਯੁਕਤ ਕੀਤਾ ਗਿਆ ਹੈ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹15,000 - ₹17,000 ਹੈ।")
            st.subheader("ਸਨੇਹਾ ਰਾਘਵਨ ਅੱਜ, 29 ਜਨਵਰੀ 2026 ਨੂੰ Reliance Trends ਨਾਲ ਜੁੜ ਗਈ ਹੈ, ਜਿਸਦੀ ਤਨਖ਼ਾਹ ₹18,000 ਤੋਂ ₹ 20,000 ਤੱਕ ਹੈ।")
            st.subheader("ਰਾਹੁਲ ਚੱਟਰਜੀ ਅੱਜ, 29 ਜਨਵਰੀ 2026 ਨੂੰ IDBI Bank ਨਾਲ ਜੁੜੇ ਹਨ, ਜਿੱਥੇ ਤਨਖ਼ਾਹ ਦੀ ਰੇਂਜ ₹23,000 - ₹25,000 ਹੈ।")

        elif st.session_state.language == "Kannada":
            st.subheader("ಆರವ್ ಮೇಹ್ತಾ ಅವರನ್ನು ಇಂದು, 29 ಜನವರಿ 2026 ರಂದು Starbucks ನಲ್ಲಿ ನೇಮಕ ಮಾಡಲಾಗಿದೆ, ಸಂಬಳ ಶ್ರೇಣಿಯು ₹15,000 - ₹17,000 ಆಗಿದೆ")
            st.subheader("ಸ್ನೇಹಾ ರಾಘವನ್ ಅವರು ಇಂದು, 29 ಜನವರಿ 2026 ರಂದು Reliance Trends ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಪ್ಯಾಕೇಜ್ ₹18,000 ರಿಂದ ₹ 20,000 ವರೆಗೆ ಇದೆ")
            st.subheader("ರಾಹುಲ್ ಚಟರ್ಜಿ ಅವರು ಇಂದು, 29 ಜನವರಿ 2026 ರಂದು IDBI Bank ಗೆ ಸೇರ್ಪಡೆಯಾಗಿದ್ದಾರೆ, ಸಂಬಳ ಶ್ರೇಣಿ ₹23,000 - ₹25,000 ಆಗಿದೆ")



def admin_dashboard():
    st.title("Welcome " + st.session_state.username)
    st.markdown("---")

def mob_dashboard():
    st.title("Welcome " + st.session_state.username)
    st.markdown("---")


if st.session_state.adol_prog or st.session_state.live_prog or st.session_state.admin_login or st.session_state.mob_login:
    if st.session_state.live_user_login:
        live_user_dashboard()
    elif st.session_state.admin_user_login:
        admin_dashboard()
    elif st.session_state.mob_user_login:
        mob_dashboard()
    else:
        login_page()
else:
    main_page()



