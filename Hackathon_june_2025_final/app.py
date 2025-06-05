import streamlit as st
import pandas as pd
import time
import base64
from io import BytesIO
from math import sqrt
from shapely.geometry import LineString
from PIL import Image



from streamlit_folium import st_folium
import pycountry
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from folium.plugins import AntPath
import itertools
import bisect
from datetime import timedelta


# Convert DataFrame to Excel in memory


def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# ------------------------------------------------------------------
# 1. INITIAL SESSION-STATE SETUP
# ------------------------------------------------------------------

# Track which sign-in button was clicked (“KYC”, “RD” or “QC”)


# Track whether the user has successfully logged in yet
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Track which role actually logged in (once login is successful)
if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

if "company_name" not in st.session_state:
    st.session_state.company_name = None

if "Fetch_Full_Serve_Data" not in st.session_state:
    st.session_state.Fetch_Full_Serve_Data = False

if "Fetch_Company_House_Data" not in st.session_state:
    st.session_state.Fetch_Company_House_Data = False

if "Fetch_D_B_Data" not in st.session_state:
    st.session_state.Fetch_D_B_Data = False

if "end_button" not in st.session_state:
    st.session_state.end_button = False


if "end_button_2" not in st.session_state:
    st.session_state.end_button_2 = False


if "fetch_transaction_data" not in st.session_state:
    st.session_state.fetch_transaction_data = False



if "visualize_data" not in st.session_state:
    st.session_state.visualize_data = False

if "populate_caar" not in st.session_state:
    st.session_state.populate_caar = False

if "integrate" not in st.session_state:
    st.session_state.integrate = False


if "generate_report_kyc2" not in st.session_state:
    st.session_state.generate_report_kyc2 = False

if "generate_report_kyc2_act" not in st.session_state:
    st.session_state.generate_report_kyc2_act = False

 
if "send_qc" not in st.session_state:
    st.session_state.send_qc = False



if "the_end" not in st.session_state:
    st.session_state.the_end = False








if "text_extract_from_pdf" not in st.session_state:
    st.session_state.text_extract_from_pdf = False

if "external_data_file" not in st.session_state:
    st.session_state.external_data_file = False

if "compare_difference" not in st.session_state:
    st.session_state.compare_difference = False


if "analyze_transaction" not in st.session_state:
    st.session_state.analyze_transaction = False


if "network_graph" not in st.session_state:
    st.session_state.network_graph = False

if "play_date" not in st.session_state:
    st.session_state.play_date = None

if "playing" not in st.session_state:
    st.session_state.playing = False
# ------------------------------------------------------------------
# 2. DASHBOARD (AFTER LOGIN)  
# ------------------------------------------------------------------

def show_dashboard():
    """
    Once logged_in is True, we land here.
    We display a “Welcome <ROLE>” header and two tabs: Pending / Complete.
    Each tab shows an Excel sheet. 
    """
    role = st.session_state.role  # “KYC”, “RD” or “QC”
    username = st.session_state.username

    # 2.1. Header
    st.markdown(f"## Welcome **{role}** **{username}**")
    st.markdown("---")

    # 2.2. Determine which Excel file to load for this role:
    #     You can adjust these file‐names/paths as needed. 
    if role == "RD":
        file_path = "Data/RD.xlsx"

        # 2.3. Create two tabs: “Pending Cases” (default) and “Complete Cases”
        pending_tab, complete_tab = st.tabs(["Pending Cases", "Complete Cases"])

        # 2.4. In “Pending Cases”, read and display the Excel (or show a message if missing)
        with pending_tab:

            try:
                st.markdown("#### Unassigned Cases")
                df_pending = pd.read_excel(file_path, sheet_name="Pending_Cases")
                # Format dates for readability
                df_pending['Case Assigned Date'] = df_pending['Case Assigned Date'].dt.strftime('%d %b %Y')
                df_pending['Due Date'] = df_pending['Due Date'].dt.strftime('%d %b %Y')

                if df_pending.empty:
                    st.info("No pending cases found.")
                else:
                    # 3.1. Build header row (column names + 1 extra for the Open Case button)
                    column_names = list(df_pending.columns)
                    header_cols = st.columns(len(column_names) + 1)
                    for idx, col_name in enumerate(column_names):
                        header_cols[idx].markdown(f"**{col_name}**")
                    header_cols[-1].markdown("**Action**")

                    # 3.2. Loop through each row and render its values + button
                    for i, row in df_pending.iterrows():
                        row_cols = st.columns(len(column_names) + 1)
                        # Write each cell value
                        for col_idx, col_name in enumerate(column_names):
                            row_cols[col_idx].write(row[col_name])

                        # The “Open Case” button. Use a unique key per row (e.g. by index)
                        button_label = f"Open"
                        if row_cols[-1].button(button_label, key=f"pending_open_{i}"):
                            # Store the selected company name in session_state
                            # (replace 'Company' with whichever column holds the company name in your df)
                            selected_company = row.get("Company Name", None)
                            if selected_company is not None:
                                st.session_state.company_name = selected_company
                                st.success(f"▶️ Opening case of: **{selected_company}**")
                                time.sleep(0.2)
                                st.rerun()
                            else:
                                st.warning("⚠️ Could not find a 'Company Name' column in your DataFrame.")

            except FileNotFoundError:
                st.error(f"Could not find the file at `{file_path}`. Make sure it exists.")
            except Exception as e:
                st.error(f"Error loading `{file_path}`: {e}")

        # 2.5. In “Complete Cases”, you could either:
        #       – Reuse the same file (if it has multiple sheets),
        #       – Or point to a “complete” file. For now, we reuse the same file but
        #         let the user pick a different sheet. You can customize as needed.
        with complete_tab:
            st.markdown("### ✔️ Complete Cases")
            try:
                # Example: if the same Excel has a sheet named “Complete”:
                df_complete = pd.read_excel(file_path, sheet_name="Complete_Cases")
                df_complete['Case Assigned Date'] = df_complete['Case Assigned Date'].dt.strftime('%d %b %Y')
                df_complete['Complete Date'] = df_complete['Complete Date'].dt.strftime('%d %b %Y')
                st.dataframe(df_complete, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading “Complete” data: {e}")


    elif (role == "KYC") and (st.session_state.end_button_2 == True):
        file_path_as = "Data/KYC_2_assigned.xlsx"
        file_path_unas = "Data/KYC_2_unassigned.xlsx"

        # 2.3. Create two tabs: “Pending Cases” (default) and “Complete Cases”
        pending_tab, complete_tab = st.tabs(["Pending Cases", "Complete Cases"])

        # 2.4. In “Pending Cases”, read and display the Excel (or show a message if missing)
        with pending_tab:
            try:
                st.markdown("#### Unassigned Cases")
                df_pending = pd.read_excel(file_path_unas, sheet_name="Pending_Cases")
                # Format dates for readability
                df_pending['Due Date'] = df_pending['Due Date'].dt.strftime('%d %b %Y')

                if df_pending.empty:
                    st.info("No pending cases found.")
                else:
                    # 3.1. Build header row (column names + 1 extra for the Open Case button)
                    column_names = list(df_pending.columns)
                    header_cols = st.columns(len(column_names) + 1)
                    for idx, col_name in enumerate(column_names):
                        header_cols[idx].markdown(f"**{col_name}**")
                    header_cols[-1].markdown("**Action**")

                    # 3.2. Loop through each row and render its values + button
                    for i, row in df_pending.iterrows():
                        row_cols = st.columns(len(column_names) + 1)
                        # Write each cell value
                        for col_idx, col_name in enumerate(column_names):
                            row_cols[col_idx].write(row[col_name])

                        # The “Open Case” button. Use a unique key per row (e.g. by index)
                        button_label = f"Assign to myself"
                        if row_cols[-1].button(button_label, key=f"pending_open_{i}"):
                            # Store the selected company name in session_state
                            # (replace 'Company' with whichever column holds the company name in your df)
                            selected_company = row.get("Company Name", None)
                            if selected_company is not None:
                                st.session_state.company_name = selected_company
                                st.success(f"▶️ Opening case of: **{selected_company}**")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.warning("⚠️ Could not find a 'Company Name' column in your DataFrame.")



                #####################################################
                st.markdown("----")
                st.markdown("#### Assigned Cases")
                df_pending_as = pd.read_excel(file_path_as)
                # Format dates for readability
                df_pending_as['Due Date'] = df_pending_as['Due Date'].dt.strftime('%d %b %Y')
                df_pending_as['Case Assigned Date'] = df_pending_as['Case Assigned Date'].dt.strftime('%d %b %Y')
                

                if df_pending_as.empty:
                    st.info("No pending cases found.")
                else:
                    # 3.1. Build header row (column names + 1 extra for the Open Case button)
                    column_names = list(df_pending_as.columns)
                    header_cols = st.columns(len(column_names) + 1)
                    for idx, col_name in enumerate(column_names):
                        header_cols[idx].markdown(f"**{col_name}**")
                    header_cols[-1].markdown("**Action**")

                    # 3.2. Loop through each row and render its values + button
                    for i, row in df_pending_as.iterrows():
                        row_cols = st.columns(len(column_names) + 1)
                        # Write each cell value
                        for col_idx, col_name in enumerate(column_names):
                            row_cols[col_idx].write(row[col_name])

                        # The “Open Case” button. Use a unique key per row (e.g. by index)
                        button_label = f"Open"
                        if row_cols[-1].button(button_label, key=f"pending_open_as_{i}"):
                            # Store the selected company name in session_state
                            # (replace 'Company' with whichever column holds the company name in your df)
                            selected_company = row.get("Company Name", None)
                            if selected_company is not None:
                                st.session_state.company_name = selected_company
                                st.success(f"▶️ Opening case of: **{selected_company}**")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.warning("⚠️ Could not find a 'Company Name' column in your DataFrame.")

            except FileNotFoundError:
                st.error(f"Could not find the file at `{file_path}`. Make sure it exists.")
            except Exception as e:
                st.error(f"Error loading `{file_path}`: {e}")

        # 2.5. In “Complete Cases”, you could either:
        #       – Reuse the same file (if it has multiple sheets),
        #       – Or point to a “complete” file. For now, we reuse the same file but
        #         let the user pick a different sheet. You can customize as needed.
        with complete_tab:
            st.markdown("### ✔️ Complete Cases")
            try:
                # Example: if the same Excel has a sheet named “Complete”:
                df_complete = pd.read_excel(file_path, sheet_name="Complete_Cases")
                df_complete['Case Assigned Date'] = df_complete['Case Assigned Date'].dt.strftime('%d %b %Y')
                df_complete['Complete Date'] = df_complete['Complete Date'].dt.strftime('%d %b %Y')
                st.dataframe(df_complete, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading “Complete” data: {e}")






    elif role == "KYC":
        # If you have a separate KYC file, adjust here:
        file_path = "Data/KYC.xlsx"

        # 2.3. Create two tabs: “Pending Cases” (default) and “Complete Cases”
        pending_tab, complete_tab = st.tabs(["Pending Cases", "Complete Cases"])

        # 2.4. In “Pending Cases”, read and display the Excel (or show a message if missing)
        with pending_tab:
            try:
                st.markdown("#### Unassigned Cases")
                df_pending = pd.read_excel(file_path, sheet_name="Pending_Cases")
                # Format dates for readability
                df_pending['Due Date'] = df_pending['Due Date'].dt.strftime('%d %b %Y')

                if df_pending.empty:
                    st.info("No pending cases found.")
                else:
                    # 3.1. Build header row (column names + 1 extra for the Open Case button)
                    column_names = list(df_pending.columns)
                    header_cols = st.columns(len(column_names) + 1)
                    for idx, col_name in enumerate(column_names):
                        header_cols[idx].markdown(f"**{col_name}**")
                    header_cols[-1].markdown("**Action**")

                    # 3.2. Loop through each row and render its values + button
                    for i, row in df_pending.iterrows():
                        row_cols = st.columns(len(column_names) + 1)
                        # Write each cell value
                        for col_idx, col_name in enumerate(column_names):
                            row_cols[col_idx].write(row[col_name])

                        # The “Open Case” button. Use a unique key per row (e.g. by index)
                        button_label = f"Assign to myself"
                        if row_cols[-1].button(button_label, key=f"pending_open_{i}"):
                            # Store the selected company name in session_state
                            # (replace 'Company' with whichever column holds the company name in your df)
                            selected_company = row.get("Company Name", None)
                            if selected_company is not None:
                                st.session_state.company_name = selected_company
                                st.success(f"▶️ Opening case of: **{selected_company}**")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.warning("⚠️ Could not find a 'Company Name' column in your DataFrame.")

            except FileNotFoundError:
                st.error(f"Could not find the file at `{file_path}`. Make sure it exists.")
            except Exception as e:
                st.error(f"Error loading `{file_path}`: {e}")

        # 2.5. In “Complete Cases”, you could either:
        #       – Reuse the same file (if it has multiple sheets),
        #       – Or point to a “complete” file. For now, we reuse the same file but
        #         let the user pick a different sheet. You can customize as needed.
        with complete_tab:
            st.markdown("### ✔️ Complete Cases")
            try:
                # Example: if the same Excel has a sheet named “Complete”:
                df_complete = pd.read_excel(file_path, sheet_name="Complete_Cases")
                df_complete['Case Assigned Date'] = df_complete['Case Assigned Date'].dt.strftime('%d %b %Y')
                df_complete['Complete Date'] = df_complete['Complete Date'].dt.strftime('%d %b %Y')
                st.dataframe(df_complete, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading “Complete” data: {e}")







    elif role == "QC":
        # If you have a separate QC file, adjust here:
        file_path = "Data/QC.xlsx"


        # 2.3. Create two tabs: “Pending Cases” (default) and “Complete Cases”
        pending_tab, complete_tab = st.tabs(["Pending Cases", "Complete Cases"])

        # 2.4. In “Pending Cases”, read and display the Excel (or show a message if missing)
        with pending_tab:
            try:
                st.markdown("#### Unassigned Cases")
                df_pending = pd.read_excel(file_path, sheet_name="Pending_Cases")
                # Format dates for readability
                df_pending['Case Assigned Date'] = df_pending['Case Assigned Date'].dt.strftime('%d %b %Y')

                if df_pending.empty:
                    st.info("No pending cases found.")
                else:
                    # 3.1. Build header row (column names + 1 extra for the Open Case button)
                    column_names = list(df_pending.columns)
                    header_cols = st.columns(len(column_names) + 1)
                    for idx, col_name in enumerate(column_names):
                        header_cols[idx].markdown(f"**{col_name}**")
                    header_cols[-1].markdown("**Action**")

                    # 3.2. Loop through each row and render its values + button
                    for i, row in df_pending.iterrows():
                        row_cols = st.columns(len(column_names) + 1)
                        # Write each cell value
                        for col_idx, col_name in enumerate(column_names):
                            row_cols[col_idx].write(row[col_name])

                        # The “Open Case” button. Use a unique key per row (e.g. by index)
                        button_label = f"Assign to myself"
                        if row_cols[-1].button(button_label, key=f"pending_open_{i}"):
                            # Store the selected company name in session_state
                            # (replace 'Company' with whichever column holds the company name in your df)
                            selected_company = row.get("Company Name", None)
                            if selected_company is not None:
                                st.session_state.company_name = selected_company
                                st.success(f"▶️ Opening case of: **{selected_company}**")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.warning("⚠️ Could not find a 'Company Name' column in your DataFrame.")

            except FileNotFoundError:
                st.error(f"Could not find the file at `{file_path}`. Make sure it exists.")
            except Exception as e:
                st.error(f"Error loading `{file_path}`: {e}")

        # 2.5. In “Complete Cases”, you could either:
        #       – Reuse the same file (if it has multiple sheets),
        #       – Or point to a “complete” file. For now, we reuse the same file but
        #         let the user pick a different sheet. You can customize as needed.
        with complete_tab:
            st.markdown("### ✔️ Complete Cases")
            try:
                # Example: if the same Excel has a sheet named “Complete”:
                df_complete = pd.read_excel(file_path, sheet_name="Complete_Cases")
                df_complete['Case Assigned Date'] = df_complete['Case Assigned Date'].dt.strftime('%d %b %Y')
                df_complete['Complete Date'] = df_complete['Complete Date'].dt.strftime('%d %b %Y')
                st.dataframe(df_complete, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading “Complete” data: {e}")




    # 2.6. Optionally, you could add a “Logout” button here:
    st.markdown("---")
    if st.button("🔄 Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()


# ------------------------------------------------------------------
# 3. LOGIN PAGE (BEFORE LOGIN)
# ------------------------------------------------------------------

def show_login_page():
    """
    Display logo, “CAARmatic” header, three sign-in buttons,
    and then Username/Password inputs + “Login” spinner logic.
    """
    # 3.1. Logo (centered)
    cols = st.columns([1.3, 1, 1])
    with cols[1]:
        st.image("Data/barclays-icon.svg", width=200)

    # 3.2. “CAARmatic” with hover effect
    cols = st.columns([1.25, 1, 1])
    with cols[1]:
        st.markdown(
            """
            <style>
            .caar-text {
                font-size: 48px;
                font-weight: bold;
                color: #262730;
                display: inline-block;
                cursor: default;
            }
            .caar-text:hover {
                color: #1f77b4;
            }
            </style>
            <div class="caar-text">KYC Accelerate</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # 3.3. Three buttons: KYC, RD, QC
    btn_cols = st.columns([0.8, 0.5, 0.5, 1])
    with btn_cols[1]:
        if st.button("  KYC Sign In  "):
            st.session_state.role = "KYC"
    with btn_cols[2]:
        if st.button("  RD Sign In  "):
            st.session_state.role = "RD"
    with btn_cols[3]:
        if st.button("  QC Sign In  "):
            st.session_state.role = "QC"

    # 3.4. If a role is chosen, show Username/Password fields + Login button
    if st.session_state.role in ["KYC", "RD", "QC"]:
        left, center, right = st.columns([1, 2, 1])
        with center:
            # 3.4.1. Set field placeholders based on which role was clicked
            if st.session_state.role == "KYC":
                user_ph = "Enter KYC Username"
                pass_ph = "Enter KYC Password"
            elif st.session_state.role == "RD":
                user_ph = "Enter RD Username"
                pass_ph = "Enter RD Password"
            else:  # QC
                user_ph = "Enter QC Username"
                pass_ph = "Enter QC Password"

            username = st.text_input(label="", placeholder=user_ph, key="username_input")
            password = st.text_input(label="", placeholder=pass_ph, type="password", key="password_input")

            # 3.4.2. “Login” button + spinner/text
            if st.button("Login", key="login_button"):
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
                    <span>👤 Attempting to log in to <b>{st.session_state.role}</b> Portal as <b>{username}</b></span>
                </div>
                """
                placeholder.markdown(combined_html, unsafe_allow_html=True)
                time.sleep(0.5)

                # In a real app, you’d verify username/password here.
                # For demonstration, we assume it’s always successful.
                placeholder.markdown(f"👤 Log In Successful!")
                time.sleep(0.5)

                # 3.4.3. Mark session as “logged in” 
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()  # immediately rerun so dashboard appears


def show_end_page():
    """
    Display logo, “CAARmatic” header, three sign-in buttons,
    and then Username/Password inputs + “Login” spinner logic.
    """
    # 3.1. Logo (centered)
    cols = st.columns([1.3, 1, 1])
    with cols[1]:
        st.image("Data/barclays-icon.svg", width=200)

    # 3.2. “CAARmatic” with hover effect
    cols = st.columns([1.25, 1, 1])
    with cols[1]:
        st.markdown(
            """
            <style>
            .caar-text {
                font-size: 48px;
                font-weight: bold;
                color: #262730;
                display: inline-block;
                cursor: default;
            }
            .caar-text:hover {
                color: #1f77b4;
            }
            </style>
            <div class="caar-text">KYC Accelerate</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    if st.session_state.role == "KYC":
        align = st.columns([0.5,1])
        with align[1]:
            st.markdown("### Thanks for using KYC Accelerate")
        align = st.columns([0.65,1])
        with align[1]:
            st.write("Redirecting to Home Page...")
        time.sleep(3)
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.company_name = None    
        st.session_state.end_button = False    
        st.rerun()

    if st.session_state.role == "RD":
        align = st.columns([0.5,1])
        with align[1]:
            st.markdown("### Thanks for using KYC Accelerate")
        align = st.columns([0.65,1])
        with align[1]:
            st.write("Redirecting to Home Page...")
        time.sleep(3)
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.company_name = None    
        st.session_state.end_button = False    
        st.rerun()

    if st.session_state.the_end:
        align = st.columns([0.55,1])
        with align[1]:
            st.markdown("### Thanks for using KYC Accelerate")
        # align = st.columns([0.65,1])
        # with align[1]:
        #     st.write("Redirecting to Home Page...")
        time.sleep(30)
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.company_name = None    
        st.session_state.end_button = False    
        st.rerun()


        
def show_kyc_second_view():
    st.markdown("### RD response to Shopping List")
    sl_filled = pd.read_excel("Data/shopping_list_filled.xlsx")
    st.dataframe(sl_filled)
    
    st.markdown("---")

    bd, od,odi, am = st.tabs(["Basic Details", "Ownership Details (Entity)","Ownership Details (Individual)", "Adverse Media"])
    with bd:
        if st.session_state.integrate:
            bd_filled = pd.read_excel("Data/bd_filled_completed.xlsx")
            st.dataframe(bd_filled)
        
        else:
            bd_filled = pd.read_excel("Data/bd_filled.xlsx")
            st.dataframe(bd_filled)

    with od:
        od_filled = pd.read_excel("Data/od_filled.xlsx")
        st.dataframe(od_filled)

    with odi:
        od_filled_i= pd.read_excel("Data/od_filled_i.xlsx")
        st.dataframe(od_filled_i)

    with am:
        image_path = "Data/news.png"
        # image = Image.open(image_path)
        st.image(image_path)
        

    cols = st.columns([0.15, 0.15,1])
    with cols[0]:
        if st.button("Integrate RD Response", key = "irr", use_container_width=True):
            st.session_state.integrate = True
            st.rerun()

    with cols[1]:
        if st.button("Submit", key = "sub", use_container_width=True):
            st.session_state.generate_report_kyc2 = True

    
    if st.button("Escalate Case", key = "ec", use_container_width=False):
        pass
    
    if st.session_state.generate_report_kyc2:
        st.markdown("---")
        if st.button("Generate Final Report", key = "gfr", use_container_width=True):
            st.session_state.generate_report_kyc2_act = True

        if st.session_state.generate_report_kyc2_act:
            col = st.columns([1,1])
            with col[0]:
                st.button("Evidence", key = "ev", use_container_width=True)
                ev_path = r"Data\Evidence.pdf"
                try:
                    with open(ev_path, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="650" height="600" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error("PDF file not found. Please check the path.")

            with col[1]:
                st.button("CAAR", key = "ca", use_container_width=True)
                ca_path = r"Data\CAAR.pdf"
                try:
                    with open(ca_path, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="650" height="600" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error("PDF file not found. Please check the path.")
                

            if st.button("Send to QC Team", key = "qt", use_container_width=True):
                st.session_state.send_qc = True
                st.rerun()
                



        




    

    




def show_kyc_first_view():
    st.title(f"KYC Assistant - {st.session_state.company_name}")
    st.markdown("---")
    cd = pd.read_excel("Data/company_data.xlsx")
    st.dataframe(cd)
    st.download_button(label="📥 Download Company Data", data = to_excel(cd),
            file_name=f'Company Data - {st.session_state.company_name}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    


    if st.button("Compare Differences", use_container_width=True):
        st.session_state.compare_difference = True

    if st.session_state.compare_difference == True:
        bd, od,odi, am, tr = st.tabs(["Basic Details", "Ownership Details (Entity)", "Ownership Details (Individual)","Adverse Media", "Trigger to RD"])

        with bd:
            al = st.columns([1, 0.14])
            with al[0]:
                basic_details = pd.read_excel("Data/Basic_Details.xlsx")

                basic_details_col = list(basic_details.columns)
                # basic_details_col.remove("Issue Criticality")

                bd_cn = basic_details[["Value", "Materiality Change"]]

                # basic_details = basic_details[basic_details_col]
                basic_details["Comments"] = ""
                basic_details["Ask Client?"] = False
                basic_details["Complete"] = False
                basic_details_styled = basic_details.style.apply(color_by_criticality, axis=1)

                basic_details_edit = st.data_editor(basic_details_styled, row_height = 55, height = 430,
                                                    column_config = {
                                                        "Comments": st.column_config.TextColumn("Comments"),
                                                        "Ask Client?": st.column_config.CheckboxColumn("Ask Client?", default = False),
                                                        "Complete": st.column_config.CheckboxColumn("Complete?", default = False)
                                                    },
                                                    hide_index = True,
                                                    disabled = basic_details_col)
                
                basic_details_edit.to_excel("Data/bd_filled.xlsx", index = False)
                with al[1]:
                    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
                    with st.popover("Upload Evidence"):
                        evidence_1 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "evidence_1")

                    with st.popover("Upload Evidence"):
                        evidence_2 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "evidence_2")

                    with st.popover("Upload Evidence"):
                        evidence_3 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "evidence_3")

                    with st.popover("Upload Evidence"):
                        evidence_4 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "evidence_4")

                    with st.popover("Upload Evidence"):
                        evidence_5 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "evidence_5")

                    with st.popover("Upload Evidence"):
                        evidence_6 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "evidence_6")

                    with st.popover("Upload Evidence"):
                        evidence_7 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "evidence_7")




                    

                #     evidence_list = {}
                #     for i in list(basic_details.Value):
                #         st.write(i)
                #         evidence_list[f'ev_i'] = i

                # st.write(evidence_list.keys())



            cols = st.columns([0.15, 0.15, 1])
            with cols[0]: 
                         

                if st.button("Escalate Case", use_container_width=True, key = "bd_ec"):
                    pass




        with od:

            cl = st.columns([1, 0.14])
            with cl[0]:
                owner_details = pd.read_excel("Data/Ownership_details.xlsx")

                owner_details_col = list(owner_details.columns)
                # basic_details_col.remove("Issue Criticality")

                od_cn = owner_details[["Value", "Materiality Change"]]

                # basic_details = basic_details[basic_details_col]
                owner_details["Comments"] = ""
                owner_details["Ask Client?"] = False
                owner_details["Complete"] = False
                owner_details_styled = owner_details.style.apply(color_by_criticality, axis=1)

                owner_details_edit = st.data_editor(owner_details_styled, row_height = 56, height = 205,
                                                    column_config = {
                                                        "Comments": st.column_config.TextColumn("Comments"),
                                                        "Ask Client?": st.column_config.CheckboxColumn("Ask Client?", default = False),
                                                        "Complete": st.column_config.CheckboxColumn("Complete?", default = False)
                                                    },
                                                    hide_index = True,
                                                    disabled = owner_details_col)
                
                owner_details_edit.to_excel("Data/od_filled.xlsx", index= False)
                with cl[1]:
                    st.markdown("<div style='height:41px'></div>", unsafe_allow_html=True)
                    with st.popover("Upload Evidence"):
                        od_evidence_1 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "od_evidence_1")

                    with st.popover("Upload Evidence"):
                        od_evidence_2 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "od_evidence_2")

                    with st.popover("Upload Evidence"):
                        od_evidence_3 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "od_evidence_3")





            ################### Table

            cols = st.columns([0.15, 0.15, 1])
            
            with cols[0]:           
                

                if st.button("Escalate Case", use_container_width=True, key = "od_ec"):
                    pass




        

        with odi:
    

            cl = st.columns([1, 0.14])
            with cl[0]:
                owner_details_i = pd.read_excel("Data/Ownership_details_Individuals.xlsx")

                owner_details_col_i = list(owner_details_i.columns)
                # basic_details_col.remove("Issue Criticality")

                od_cn_i = owner_details_i[["Value", "Materiality Change"]]

                # basic_details = basic_details[basic_details_col]
                owner_details_i["Comments"] = ""
                owner_details_i["Ask Client?"] = False
                owner_details_i["Complete"] = False
                owner_details_styled_i = owner_details_i.style.apply(color_by_criticality, axis=1)

                owner_details_edit_i = st.data_editor(owner_details_styled_i, row_height = 56, height = 152,
                                                    column_config = {
                                                        "Comments": st.column_config.TextColumn("Comments"),
                                                        "Ask Client?": st.column_config.CheckboxColumn("Ask Client?", default = False),
                                                        "Complete": st.column_config.CheckboxColumn("Complete?", default = False)
                                                    },
                                                    hide_index = True,
                                                    disabled = owner_details_col)
                
                owner_details_edit_i.to_excel("Data/od_filled_i.xlsx", index= False)
                with cl[1]:
                    st.markdown("<div style='height:41px'></div>", unsafe_allow_html=True)
                    with st.popover("Upload Evidence"):
                        od_evidence_1 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "od_evidence_12")

                    with st.popover("Upload Evidence"):
                        od_evidence_2 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "od_evidence_22")







            ################### Table

            cols = st.columns([0.15, 0.15, 1])
            
            with cols[0]:           
               

                if st.button("Escalate Case", use_container_width=True, key = "od_ec_i"):
                    pass





        with am:
            # st.markdown(f"### News about {st.session_state.company_name}")
            # st.markdown(""":orange-badge[your text here]""")
            with st.spinner("Fetching News..."):
                time.sleep(1)
            image_path = "Data/news.png"
            # image = Image.open(image_path)
            st.image(image_path)



            if st.button(" Escalate Case ", use_container_width=False, key = "am_ec"):
                    pass
            
        with tr:
            final_list = ["Transaction to Sanction Countries"] + basic_details_edit[basic_details_edit["Ask Client?"] == True].Value.tolist() + owner_details_edit[owner_details_edit["Ask Client?"] == True].Value.tolist()
            ###### HANDLE list Existence
            df_tr = pd.DataFrame({"RD Requirements": final_list,
                                  "Raise Request": [True]*len(final_list)})
            
            
            df_tr_edit = st.data_editor(df_tr,
                                    column_config = {
                                        "Raise Request": st.column_config.CheckboxColumn("Ask RD?", default = False)
                                    },
                                    hide_index = True,
                                    disabled = ["RD Requirements"])
            
            df_tr_edit.to_excel("Data/shopping_list.xlsx", index = False)
            

            
            

            



            if st.button("Send to RD", use_container_width=True, key = "tr_se"):
                st.session_state.end_button = True
                st.rerun()



            













    # cols = st.columns([0.75, 1])
    # with cols[0]:
    #     pdf_file = st.file_uploader("Upload Full Serve Images PDF", type="pdf", key = "pdf")#, label_visibility = "hidden" )
    #     if pdf_file is not None:
    #         show_pdf(pdf_file)

    #         st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    #         if st.button("Click to Extract Relevant Text"):
    #             st.session_state.text_extract_from_pdf = True
    
    # if st.session_state.text_extract_from_pdf:
    #     with cols[0]:

    #         ########
    #         ####GEN AI Output Come Here
    #         ########

    #         data = {
    #                     "Name": "ABC Company",
    #                     "Trading Name": "ABC Trade",
    #                     "Ownership": "Private Limited",
    #                     "Date of incorporation": "13 May 1984",
    #                     "Registered Address": "13/6 Kingscross, London",
    #                     "Country of Incorporation": "United Kingdom"
    #                 }
            
    #         full_serve_data = pd.DataFrame(list(data.items()), columns=["Categories", "Values"])
    #         st.markdown("<div style='height:55px'></div>", unsafe_allow_html=True)
    #         st.markdown("Full Serve Data")
    #         st.dataframe(full_serve_data, use_container_width=False)

    #         st.download_button(label="📥 Download Excel", data = to_excel(full_serve_data),
    #                             file_name=f'Full Serve Data - {st.session_state.company_name}.xlsx',
    #                             mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    #     with cols[1]:
    #         st.markdown("<div style='height:882px'></div>", unsafe_allow_html=True)
                        
    #         external_data_file = st.file_uploader("Upload Data from external source", type="xlsx",accept_multiple_files = True,
    #                             key = "external_data")#, label_visibility = "hidden" )
            

    #         if len(external_data_file) == 1:
    #             st.write(f"{external_data_file[0].name[:-5]}")
    #             ext_file_0 = pd.read_excel(external_data_file[0])
    #             st.dataframe(ext_file_0)
    #             st.session_state.external_data_file = True

    #         elif len(external_data_file) == 2:
    #             sep = st.columns([1, 1])
    #             with sep[0]:
    #                 st.write(f"{external_data_file[0].name[:-5]}")
    #                 ext_file_0 = pd.read_excel(external_data_file[0])
    #                 st.dataframe(ext_file_0)

    #             with sep[1]:
    #                 st.write(f"{external_data_file[1].name[:-5]}")
    #                 ext_file_1 = pd.read_excel(external_data_file[1])
    #                 st.dataframe(ext_file_1)
    #                 st.session_state.external_data_file = True


    # if st.session_state.external_data_file == True:
    #     if st.button("Compare Differences", use_container_width=True):
    #         st.session_state.compare_difference = True

    # if st.session_state.compare_difference == True:
    #     kyc_difference = pd.read_excel("Data/KYC_Difference.xlsx")
        
    #     # Add a new column “Change/No Change” with a default value (e.g. all empty strings, or “No Change”)
    #     kyc_difference["Acknowledged"] = "False"  # you can default to "" or "No Change"
    #     kyc_difference = kyc_difference.style.apply(color_by_criticality, axis=1)
    #     #st.dataframe(kyc_difference.style.apply(color_by_criticality, axis=1))
    #     edited_df = st.data_editor(kyc_difference,
    #                                 column_config={"Acknowledged": st.column_config.CheckboxColumn("Acknowledged",
    #                                                                                                 help="Verify & makee the required changes.",
    #                                                                                                 default=False)},
    #                                 disabled=["Criticality Level","Categories","Full Serve","Company House",	"Difference with Company House","D&B",
    #                                             "Difference with D&B"],
    #                                 #num_rows="dynamic",              # let user add/remove rows if needed
    #                                 use_container_width=True,          # make it expand to the page width
    #                                 hide_index=True
    #                                 )
        
    #     st.download_button(label="📥 Download Excel", data = to_excel(edited_df),
    #                 file_name=f'KYC Data - {st.session_state.company_name}.xlsx',
    #                 mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
        
    #     if "False" in edited_df["Acknowledged"].values:
    #         st.button("Save Progress and exit", use_container_width=False)
        
    #     else:
    #         if st.button(f"Complete KYC for {st.session_state.company_name}", use_container_width=True):
    #             pass
                


@st.cache_data
def load_world():
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
    world = gpd.read_file("Data/SHP/ne_110m_admin_0_countries.shp")
    # def iso3_to_2(code):
    #     try:
    #         return pycountry.countries.get(alpha_3=code).alpha_2
    #     except:
    #         return None
    # world['iso2'] = world['id'].map(iso3_to_2)
    # proj = world.to_crs(epsg=3857)
    # ctr = gpd.GeoSeries(proj.geometry.centroid, crs='epsg:3857') \

    world = world.to_crs(epsg=4326)

    countries_to_highlight = [
    "Afghanistan", "Belarus", "Burma", "Cuba", "North Korea", "Iran", "Iraq", "Libya", "Russia", "South Sudan", "Sudan", "Syria", "Ukraine", "Venezuela", "Yemen"
]

    #Filter the dataset for the Sanctioned Countries.
    selected_countries = world[world["NAME"].isin(countries_to_highlight)]

    # world['centroid_lat'] = ctr.y
    # world['centroid_lon'] = ctr.x
    # lookup = world.dropna(subset=['iso2']) \
    #               .set_index('iso2')[['centroid_lat','centroid_lon']] \
    #               .to_dict('index')
    return world, selected_countries




def draw_transactions_on_map(
    m: folium.Map,
    transactions: pd.DataFrame,
) -> None:
    """
    Given a Folium map and a DataFrame of transactions,
    draw AntPath lines color‐coded by risk level.
    """
    risk_colors = {
        "High": "red",
        "Medium": "orange",
        "Low": "green"
    }

    for _, row in transactions.iterrows():
        color = risk_colors.get(row["Risk"], "gray")
        AntPath(
            locations=[(row.origin_lat, row.origin_lon),
                       (row.destination_lat, row.destination_lon)],
            color=color,
            weight=3,
            delay=1000,
            dash_array=[10, 20]
        ).add_to(m).add_child(
            folium.Tooltip(
                f"<b>{row['3rd_party_company']}</b><br>"
                f"Risk: {row.Risk}<br>"
                f"{row.Origin_country} → {row.Destination_country}<br>"
                f"Date: {row.Date.date()}<br>"
                f"Amount: ${row.Amount:,}",
                sticky=True
            )
        )


def get_transaction_dates(subset: pd.DataFrame) -> list[pd.Timestamp]:
    """
    Extract and sort unique transaction dates (as date objects) from subset.
    """
    return sorted(subset["Date"].dt.date.unique())


def handle_time_controls(
    subset: pd.DataFrame,
    start_date,
    end_date
) -> pd.Timestamp:
    """
    Render time slider plus Prev/Next/Play/Pause buttons.
    Updates st.session_state['play_date'] and 'playing'.
    Returns the finalized play_date.
    """
    transaction_dates = get_transaction_dates(subset)
    if not transaction_dates:
        return None  # no transactions at all

    # Calendar of all dates between start_date and end_date (inclusive)
    calendar_dates = [
        start_date + timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
    ]

    # Initialize or validate session_state.play_date
    if st.session_state.play_date not in calendar_dates:
        st.session_state.play_date = calendar_dates[0]

    # Date slider over the full calendar
    st.session_state.play_date = st.slider(
        "Time Slider:",
        min_value=start_date,
        max_value=end_date,
        value=st.session_state.play_date,
        format="YYYY-MM-DD",
        key="slider"
    )

    # Define callbacks for Prev/Next
    def go_previous():
        idx = bisect.bisect_left(transaction_dates, st.session_state.play_date) - 1
        if idx >= 0:
            st.session_state.play_date = transaction_dates[idx]

    def go_next():
        idx = bisect.bisect_right(transaction_dates, st.session_state.play_date)
        if idx < len(transaction_dates):
            st.session_state.play_date = transaction_dates[idx]

    def toggle_play():
        st.session_state.playing = not st.session_state.playing

    # Render buttons
    b0, b1, b2, b3 = st.columns([0.5,1.3, 1, 1])
    with b1:
        st.button("⏮️ Previous Transaction", on_click=go_previous)
    with b2:
        label = "⏸️ Pause" if st.session_state.playing else "▶️ Play"
        st.button(label, on_click=toggle_play)
    with b3:
        st.button("⏭️ Next Transaction", on_click=go_next)

    # Auto‐advance when playing
    if st.session_state.playing:
        idx = calendar_dates.index(st.session_state.play_date)
        if idx + 1 < len(calendar_dates):
            st.session_state.play_date = calendar_dates[idx + 1]
            time.sleep(0.5)
            # st.rerun()
        else:
            st.session_state.playing = False

    return st.session_state.play_date
        
def create_base_map(world: gpd.GeoDataFrame) -> folium.Map:
    """
    Initialize a Folium map with a light basemap and country boundaries.
    """
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles="CartoDB_Positron",
        world_copy_jump=True
    )

    folium.GeoJson(
        world.__geo_interface__,
        style_function=lambda f: {
            "fillColor": "#f2f2f2",
            "color": "#444",
            "weight": 0.5,
            "fillOpacity": 0.6
        }
    ).add_child(
        GeoJsonTooltip(fields=["name"], aliases=["Country:"], labels=True)
    ).add_to(m)

    return m


       
def add_coordinates(df: pd.DataFrame, lookup: dict) -> pd.DataFrame:
    """
    Add origin_iso, dest_iso, origin_lat/lon, dest_lat/lon columns to df.
    """
    df = df.copy()
    # map country names to ISO2
    df["origin_iso"] = df["Origin_country"].apply(lambda x: pycountry.countries.lookup(x).alpha_2)
    df["dest_iso"] = df["Destination_country"].apply(lambda x: pycountry.countries.lookup(x).alpha_2)

    for side, iso_col in [("origin", "origin_iso"), ("destination", "dest_iso")]:
        df[f"{side}_lat"] = df[iso_col].map(lambda c: lookup.get(c, {}).get("centroid_lat"))
        df[f"{side}_lon"] = df[iso_col].map(lambda c: lookup.get(c, {}).get("centroid_lon"))

    return df


def slider_filter_transactions(
    df: pd.DataFrame,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp
) -> pd.DataFrame:
    """
    Return subset of df that falls within [start_date, end_date]
    """
    mask = (
        (df["Date"].dt.date >= start_date)
        & (df["Date"].dt.date <= end_date)
    )
    return df[mask].copy()

def filter_transactions(
    df: pd.DataFrame,
    selected_companies: list[str],
    selected_risks: list[str]
) -> pd.DataFrame:
    """
    Return subset of df that falls within [start_date, end_date],
    matches company list, and matches risk levels.
    """
    mask = ((df["Other_Country"].isin(selected_companies))
        & (df["Risk"].isin(selected_risks))
    )
    return df[mask].copy()


def show_rd_view():
    st.title(f"{st.session_state.company_name}")
    st.markdown("---")

    sl, caar= st.tabs(["Shopping List", "CAAR"])

    with sl:
        st.write("Shopping list received from KYC Team")
        
        df_tr_edit = pd.read_excel("Data/shopping_list.xlsx")
        df_tr_edit = df_tr_edit[df_tr_edit["Raise Request"] == True]

        ####################
        al = st.columns([1, 0.14])
        with al[0]:
            df_tr_edit = df_tr_edit[["RD Requirements"]]
            # basic_details = basic_details[basic_details_col]
            df_tr_edit["Response"] = ""

            df_tr_edit = st.data_editor(df_tr_edit, row_height = 55, height = 210,
                                                column_config = {
                                                    "Response": st.column_config.TextColumn("Response")
                                                },
                                                hide_index = True,
                                                disabled = ["RD Requirements"])
            with al[1]:
                st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
                with st.popover("Upload Evidence"):
                    sl_evidence_1 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "sl_evidence_1")

                with st.popover("Upload Evidence"):
                    sl_evidence_2 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "sl_evidence_2")

                with st.popover("Upload Evidence"):
                    sl_evidence_3 = st.file_uploader("Upload Evidence", type="JPEG",accept_multiple_files = True,key = "sl_evidence_3")




        ##################



        cols = st.columns([0.25, 0.25, 0.25, 1])
        # with cols[0]:
            
            
        with cols[0]:    
            if st.button("Send to KYC Team", key = "rd_kt", use_container_width=True):
                df_tr_edit.to_excel("Data/shopping_list_filled.xlsx", index = False)
                pass



    with caar:
        if st.button("Fetch Transaction Data", use_container_width=True, key = 'td'):
            st.session_state.fetch_transaction_data = True

        
                    
            # progress_text = "Fetching Data in progress. Please wait..."
            # my_bar = st.progress(0, text=progress_text)

            # for percent_complete in range(100):
            #     time.sleep(0.05)
            #     my_bar.progress(percent_complete + 1, text=progress_text)
            # time.sleep(1)
            # my_bar.empty()

            # st.success('Data Fetched Successfully!', icon="✅")

            with st.status("Transaction data", expanded = True):
                st.write("✅ Searching for data...")
                time.sleep(0.5)
                st.write("✅ Fetching Data...")
                time.sleep(0.5)
                st.write("✅ Summarizing data...")
                time.sleep(0.5)

        if st.session_state.fetch_transaction_data == True:
            st.markdown("### Data Summary")
            st.markdown("""Rockfire Investment Finance Limited consists of total of 24 transactions, with a total transaction amounting to Euro 134,742.51. The transactions are categorized into receipts totaling Euro 60,321.91 and payments amounting to Euro 74,420.60. This indicates a net outflow of Euro 14,098.69, suggesting a higher volume of payments compared to receipts, which might reflect operational expenses or strategic investments.The transactions are further categorized by financial crime risk levels: 
                        1) **High Risk** : Euro 28,266.64 across 4 transactions. 2) **Medium Risk** : Euro 24,239.04 across 5 transactions. 3) **Low Risk** : Euro 82,236.84 across 15 transactions.""")
   

            if st.button("Visualize Data", use_container_width=True, key = 'visual_data'):
                st.session_state.visualize_data = True

            if st.session_state.visualize_data == True:

                df_transaction = pd.read_excel("Data/synthetic_transactions_complete.xlsx")
                df_transaction['Date'] = pd.to_datetime(df_transaction['Date'])
                df_transaction = df_transaction.sort_values('Date')
                df_transaction['Other_Country'] = df_transaction.apply(
                    lambda row: row['Origin_country'] if row['Receipt/Payment'] == 'Receipt' else row['Destination_country'], axis = 1)

                ####Slider
                min_date = df_transaction['Date'].dt.date.min()
                max_date = df_transaction['Date'].dt.date.max()
                start_date, end_date = st.sidebar.slider("Select Date Range:", min_value=min_date, max_value=max_date,
                value=(min_date, max_date),format="YYYY-MM-DD")

                date_filtered_trans = slider_filter_transactions(df_transaction, start_date, end_date)

                align = st.columns([1, 1])
                

                with align[1]:
                    # Risk multiselect
                    st.sidebar.markdown("## Filter by Risk Level:")
                    risk_levels  = date_filtered_trans["Risk"].unique().tolist() #["High", "Medium", "Low"]
                    order = {"Low": 0, "Medium": 1, "High": 2}

                    def aggregate_risk(risks):
                        max_val = risks.map(order).max()
                        for key,value in order.items():
                            if value == max_val:
                                return key

                    #Aggregate transactions byu external country and Receipt/Payment type, summing amounts and aggregating risk.
                    agg_df = date_filtered_trans.groupby(['Other_Country','Receipt/Payment']).agg({'Amount':'sum', 'Risk': aggregate_risk}).reset_index()

                    risk_levels = sorted(risk_levels, key=lambda x: order.get(x, 99))

                    selected_risks: list[str] = []

                    # By default, if there is no session key yet, assume all risk‐boxes are checked
                    for risk in risk_levels:
                        if f"cb_risk_{risk}" not in st.session_state:
                            st.session_state[f"cb_risk_{risk}"] = True

                    for risk in risk_levels:
                        checked = st.sidebar.checkbox(
                            label=risk,
                            key=f"cb_risk_{risk}"
                        )

                        if checked:
                            selected_risks.append(risk)

                with align[0]:
                    
                    #### Company Filter
                    st.sidebar.markdown("## Filter by Country:")

                    # Master "All companies" checkbox
                    company_list = agg_df["Other_Country"].unique().tolist()
                    company_list.sort()

                    def _toggle_all():
                        for c in company_list:
                            st.session_state[f"cb_{c}"] = st.session_state["all_companies"]

                    st.sidebar.checkbox(
                        "All countries",
                        key="all_companies",
                        value=True,
                        on_change=_toggle_all
                    )

                    selected_companies: list[str] = []
                    for company in company_list:
                        def _unset_master(c=company):
                            if not st.session_state[f"cb_{c}"]:
                                st.session_state["all_companies"] = False

                        checked = st.sidebar.checkbox(
                            label=company,
                            key=f"cb_{company}",
                            value=True,
                            on_change=_unset_master
                        )
                        if checked:
                            selected_companies.append(company)


                
                agg_df_filt = filter_transactions(agg_df, selected_companies, selected_risks)
                
                if agg_df_filt.empty:
                    st.warning("No transactions in the selected filters.")

                else:                    

                    st.dataframe(agg_df_filt)
                    st.download_button(label="📥 Download Excel", data = to_excel(agg_df_filt),
                                        file_name=f'Transaction Data - {selected_companies} and {selected_risks}.xlsx',
                                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        
                    

                    world, selected_countries = load_world()
                    # df = add_coordinates(agg_df_filt, lookup)

                    country_centroids = {}
                    for idx, row in world.iterrows():
                        centroid = row["geometry"].centroid
                        country_centroids[row["NAME"]] = (centroid.y, centroid.x)

                    #DEtermine hub location: Company Location
                    hub = None
                    for key in country_centroids.keys():
                        if key in ["United Kingdom", "UK"]:
                            hub = country_centroids[key]
                            break
                    #Fallback Location if not found
                    if hub is None:
                        hub = (51.5072, -0.1276)


                    




                    
                    # Create base Folium map with countries
                    # m = create_base_map(world)
                    #Create Folium map. Zoom_start that is used before
                    m = folium.Map(location=hub, zoom_start=2)

                    #Add GeoJson layer to highlight sanctioned countries in red.
                    folium.GeoJson(
                        selected_countries, 
                        style_function=lambda feature:{
                            "fillColor": "red",
                            "color": "black",
                            "weight": 1.5,
                            "fillOpacity": 0.3,
                        },
                        tooltip = folium.features.GeoJsonTooltip(fields=["NAME"], aliases=["Country:"])
                    ).add_to(m)

                    #Mark the hub (company) with blue pin
                    folium.Marker(
                        location=hub,
                        popup="Viva Solutions Ltd. (UK)",
                        icon=folium.Icon(color="black",icon="info-sign")
                    ).add_to(m)





                    # # 7. Handle time controls (slider + buttons)
                    # play_date = handle_time_controls(df, start_date, end_date)
                    # if play_date is None:
                    #     st.warning("No transaction dates available.")

                    # else:
                    #     # 8. Draw cumulative transactions on or before play_date
                    #     cumulative = df[df["Date"].dt.date <= play_date]
                        # draw_transactions_on_map(m, cumulative)

                    color_mapping = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}


                    #We group aggregated transactions by partner country(Other_Country).
                    # if both type exist for a partner, we add a curve by offsetting the midpoint
                    for other_country, group in agg_df_filt.groupby('Other_Country'):
                        partner_coords = None
                        for country,coord in country_centroids.items():
                            if country.lower() == other_country.lower():
                                partner_coords = coord
                                break
                        if partner_coords is None:
                            continue # skip if no country found
                        
                        hub_lat, hub_lon = hub
                        partner_lat, partner_lon = partner_coords

                        # Vector from hub to partner and its distance
                        dx = partner_lat - hub_lat
                        dy = partner_lon - hub_lon
                        distance = sqrt(dx**2 + dy**2)
                        # If group has more than one transaction type, we assign offset
                        use_offset = len(group) >1

                        # For eachtransaction type for the particular partner country.
                        for idx,row in group.iterrows():
                            #Default: straight line if no offset to be applied.
                            if not use_offset or distance == 0:
                                line_coords = [hub, partner_coords]
                            else:
                                #Calculate offset magnitude as 10% of the distance
                                offset_magnitude = distance*0.1
                                #Calculate a perpendicular vector (-dy, dx)
                                norm = sqrt(dy**2 + dx**2)
                                v_perp = (-dy/norm, dx/norm) if norm!= 0 else (0,0)
                                #Use sign: +1 for Receipt, -1 for Payment
                                sign = 1 if row["Receipt/Payment"] == "Receipt" else -1
                                #Compute the midpoint by scaled perpendicula vector
                                mid_lat = (hub_lat + partner_lat)/2
                                mid_lon = (hub_lon + partner_lon)/2
                                offset_mid = (mid_lat + sign * v_perp[0] * offset_magnitude, 
                                            mid_lon + sign * v_perp[1] * offset_magnitude)
                                # Create a curved polyline using hub, offset midpoint and partner.
                                line_coords = bezier_curve(hub, offset_mid, partner_coords)

                                #Choose Linestyle: solid for Receipt, dotted for payment.
                                dash_pattern = None if row["Receipt/Payment"] == "Receipt" else "5,10"
                                #Get risk based color
                                line_color = color_mapping.get(row["Risk"],"blue")
                                #Build tooltip text with basic transaction details
                                tooltip_text = (
                                    f"Type: {row['Receipt/Payment']}<br>"
                                    f"Amount: {row['Amount']:.2f}<br>"
                                    f"Risk: {row['Risk']}"
                                )

                                #Draw the polyline on map
                                folium.PolyLine(
                                    locations=line_coords, 
                                    color=line_color, 
                                    weight=3, 
                                    dash_array=dash_pattern, 
                                    tooltip=tooltip_text
                                ).add_to(m)



                    # 9. Display map
                    st_folium(m, width=1400, height=600)

                    if st.button("Add to Evidence", use_container_width=False, key = "map" ):
                        pass

                if st.button("Populate CAAR", use_container_width=True, key = "CAAR"):
                    st.session_state.populate_caar = True

                if st.session_state.populate_caar == True:
                    a = st.columns([0.2, 1,0.2])
                    with a[1]:
                        st.markdown("### Client Account Activity Review")
                        st.markdown("""The account activity review is the mechanism by which business assesses and confirms the customer’s actual business activity is consistent with the nature of its business, the purpose of the business relationship, the expected activity as described at onboarding or at the last periodic refresh and the risk rating remains appropriate.
    It is important to review the account activity on an ongoing basis to support the financial crime agenda to ensure the level of potential risk exposure remains within Barclays appetite and the clients risk rating is appropriate.
    See FinCrime red flags for further guidance on expectations and what to look out for.
    Using a risk based approach and your client knowledge to review the actual account activity vs expected activity to ensure this remains consistent with the Banks knowledge since the last review.
    All comments, including any identified issues that require further investigation plus any required actions, should be provided by the RD in the comments section and undertaken by the RD.
    See supporting information here.
    How to fill in this form\n
    •	In the case of selection fields, please select from the list
    •	Please tick boxes that apply.
    •	Leave boxes blank if they do not apply to you
    •	Mandatory details are marked with an *
    """)
                        st.markdown("""

""")
                        st.text_input("Client Name*", "Rockfire Investment Finance Limited", key = "vhava")
                        st.text_input("Client Registration ID*", "41533251", key = "vhavas")
                        st.markdown("##### Nature of Business")
                        st.text_input("Describe the entity nature of Business and expected banking activities/relationship with Barclays (i.e. product, trade, account purpose) *", "The transactions span various industries, with notable concentrations in the automobile sector ($41,107.02 across 8 transactions) and pharmaceuticals ($23,885.55 across 4 transactions). These sectors are traditionally high-value and could be targets for fraudulent activities, such as mis-invoicing or illicit trade practices.", key = "vhavai")
                        st.text_input("What trading activity and geographic payment flows do you expect through the Barclays accounts? *", "Trading activity predominantly In UK and Netherlands for both receipt and payment.", key = "vhavaie")
                        
                        st.markdown("Does your client have any exposure to Sanctioned/Restricted country according to the RAM? *")
                        col1, col2, col3 = st.columns([0.25, 0.25, 1])  
  
# Place the checkboxes in the first two columns  
                        with col1:  
                            checkbox1 = st.checkbox("Yes", key="bv")  
                        
                        with col2:  
                            checkbox2 = st.checkbox("No", key="nb", value = True) 
                        # if st.button("Finalize CAAR", use_container_width=False, key = "Fianl_CAAR"):
                        #     pass
                        st.markdown("##### Payment Review")
                        st.markdown("Upon reviewing your clients accounts have you identifies anything that is not aligned to the nature of business or expected flows?")
                        col1, col2, col3 = st.columns([0.25, 0.25, 1])  
  
# Place the checkboxes in the first two columns  
                        with col1:  
                            checkbox1 = st.checkbox("Yes",key="nbb" )  
                        
                        with col2:  
                            checkbox2 = st.checkbox("No",key="ntb",value = True) 
                        st.markdown("##### Account Turnover")
                        # st.markdown("What are the total debits and credits through the Barclays accounts? *")
                        # st.text_input("WIs this in line with what you expect to see go through the Barclays account? *",formatted_text,key = "vhavakll")
                        
                        # Combine the inputs into a formatted string  
                        formatted_text = f"""Total receipts £10,200,400.78 and total payment £1000,400,210.23.||Payment OUT--3124 payments to United Kingdom, 210 payments to Netherlands.||Payment IN--4000 payments to United Kingdom, 2 payments to Netherlands."""  
                        # st.text_input("Is this in line with what you expect to see go through the Barclays account? *",formatted_text,key = "vhavakll")
                        # Display the formatted text using Markdown  
                        st.text_input("What are the total debits and credits through the Barclays accounts? *",formatted_text, key="prmg")
                        st.markdown("Is this in line with what you expect to see go through the Barclays account? *")
                        col1, col2, col3 = st.columns([0.25, 0.25, 1])  
  
# Place the checkboxes in the first two columns  
                        with col1:  
                            checkbox1 = st.checkbox("Yes", key="bvl",value = True)  
                        
                        with col2:  
                            checkbox2 = st.checkbox("No", key="nob") 
                            
                        st.text_input("Please add any further supporting commentary","The account transaction flow appears as expected by the coverage team. There are no concerns.", key = "vhavaklpp")
                        

                        
                        # if st.button("Finalize CAAR", use_container_width=False, key = "Fianl_CAAR"):
                        #     pass

                        attest = st.checkbox("Attest CAAR Document")
                        if attest:
                            if st.button("Send to KYC TEAM", use_container_width=True, key = "send_CAAR"):
                                st.session_state.end_button_2 = True
                                st.rerun()



    # with att:
    #     st.markdown("""Template
    #                 .
    #                 .
    #                 .
    #                 .
    #                 """)
        
    #     attest = st.checkbox("Attest CAAR Document")
    #     if attest:
    #         if st.button("Send to KYC TEAM", use_container_width=True, key = "send_CAAR"):
    #             st.session_state.end_button_2 = True
    #             st.rerun()


                    



            

            
            




        

            




    # st.markdown("---")
    # cols = st.columns([1, 1])

    # with cols[0]:
    #     transaction_file = st.file_uploader(f"Upload {st.session_state.company_name} transactions data", type="xlsx", key = "Transaction")
    #     if transaction_file is not None:
    #         df_transaction = pd.read_excel(transaction_file)
    #         df_transaction['Date'] = pd.to_datetime(df_transaction['Date'])
    #         df_transaction = df_transaction.sort_values('Date')
    #         st.dataframe(df_transaction)

    #         with cols[1]:
    #             sanction_file = st.file_uploader(f"Upload Sanction countries data", type="xlsx", key = "Sanction")
    #             if sanction_file is not None:
    #                 df_sanction = pd.read_excel(sanction_file)
    #                 st.dataframe(df_sanction)

    
    # if transaction_file is not None:
    #     if sanction_file is not None:
    #         if st.button(f"Analyze Transactions of {st.session_state.company_name}", use_container_width=True):
    #             st.session_state.analyze_transaction = True

    # if st.session_state.analyze_transaction == True:

    #     ####Slider
    #     min_date = df_transaction['Date'].dt.date.min()
    #     max_date = df_transaction['Date'].dt.date.max()
    #     start_date, end_date = st.slider("Select Date Range:", min_value=min_date, max_value=max_date,
    #     value=(min_date, max_date),format="YYYY-MM-DD")

    #     date_filtered_trans = slider_filter_transactions(df_transaction, start_date, end_date)

    #     align = st.columns([1, 1])
    #     with align[0]:
            
    #         #### Company Filter
    #         st.markdown("#### Filter by Company:")

    #         # Master "All companies" checkbox
    #         company_list = date_filtered_trans["3rd_party_company"].unique().tolist()
    #         company_list.sort()

    #         def _toggle_all():
    #             for c in company_list:
    #                 st.session_state[f"cb_{c}"] = st.session_state["all_companies"]

    #         st.checkbox(
    #             "All companies",
    #             key="all_companies",
    #             value=True,
    #             on_change=_toggle_all
    #         )

    #         selected_companies: list[str] = []
    #         for company in company_list:
    #             def _unset_master(c=company):
    #                 if not st.session_state[f"cb_{c}"]:
    #                     st.session_state["all_companies"] = False

    #             checked = st.checkbox(
    #                 label=company,
    #                 key=f"cb_{company}",
    #                 value=True,
    #                 on_change=_unset_master
    #             )
    #             if checked:
    #                 selected_companies.append(company)


    #     with align[1]:
    #         # Risk multiselect
    #         st.markdown("#### Filter by Risk Level:")
    #         risk_levels  = date_filtered_trans["Risk"].unique().tolist() #["High", "Medium", "Low"]
    #         order = {"Low": 0, "Medium": 1, "High": 2}
    #         risk_levels = sorted(risk_levels, key=lambda x: order.get(x, 99))

    #         selected_risks: list[str] = []

    #         # By default, if there is no session key yet, assume all risk‐boxes are checked
    #         for risk in risk_levels:
    #             if f"cb_risk_{risk}" not in st.session_state:
    #                 st.session_state[f"cb_risk_{risk}"] = True

    #         for risk in risk_levels:
    #             checked = st.checkbox(
    #                 label=risk,
    #                 key=f"cb_risk_{risk}"
    #             )

    #             if checked:
    #                 selected_risks.append(risk)

        
    #     date_filtered_trans = filter_transactions(date_filtered_trans, selected_companies, selected_risks)
        

    #     if date_filtered_trans.empty:
    #         st.warning("No transactions in the selected filters.")

    #     else:
    #         st.dataframe(date_filtered_trans)
        

    #         st.download_button(label="📥 Download Excel", data = to_excel(date_filtered_trans),
    #             file_name=f'Transaction Data - {selected_companies} and {selected_risks}.xlsx',
    #             mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            
    #         if st.button(f"View Network Graph", use_container_width=True):
    #             st.session_state.network_graph = True

    #         if st.session_state.network_graph == True:
    #             world, lookup = load_world()
    #             df = add_coordinates(date_filtered_trans, lookup)
                
    #             # Create base Folium map with countries
    #             m = create_base_map(world)

    #             # 7. Handle time controls (slider + buttons)
    #             play_date = handle_time_controls(df, start_date, end_date)
    #             if play_date is None:
    #                 st.warning("No transaction dates available.")

    #             else:
    #                 # 8. Draw cumulative transactions on or before play_date
    #                 cumulative = df[df["Date"].dt.date <= play_date]
    #                 draw_transactions_on_map(m, cumulative)

    #             # 9. Display map
    #             st_folium(m, width=1400, height=600)

    #             if st.session_state.playing:
    #                 st.rerun()




def show_qc_view():
    st.title("QC Assistant")
    st.markdown("---")

    al = st.columns([1,1,1])
    with al[0]:
        st.button("Evidence File", key = "ef",use_container_width=True )
        ev_path = r"Data\Evidence.pdf"

        try:
            with open(ev_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="440" height="600" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("PDF file not found. Please check the path.")

    with al[1]:
        st.button("CAAR Document", key = "cd",use_container_width=True)
        # show_pdf("Data/CAAR.pdf")
        c_path = r"Data\CAAR.pdf"

        try:
            with open(c_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="440" height="600" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("PDF file not found. Please check the path.")

    with al[2]:
        st.button("Full Serve Data", key = "fsd",use_container_width=True)
        d = pd.read_excel("Data/fullserve_final.xlsx")
        st.dataframe(d)

    st.markdown("---")

    df_qc = pd.read_excel("Data/QC CHecklist.xlsx")

    df_qc["QC Comments"] = ""
    df_qc_edit = st.data_editor(df_qc,column_config = {
                                                        "QC Comments": st.column_config.TextColumn("QC Comments"),
                                                        "Verification": st.column_config.CheckboxColumn("Verification", default = False),
                                                    },
                                                    hide_index = True,
                                                    disabled = ["Category", "Task", "Commentary", "KYC Checkbox", "QC - Pass/Fail", "Reason"])
    
    if st.button("Resend to KYC Team for changes", key = "ra"):
        pass

    if st.button("Attest and close case", key = "aclose"):
        st.session_state.the_end = True
        st.rerun()






def bezier_curve(p0, p1, p2, num_points=20):
    return [
        (
            (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0],
            (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        )
        for t in [i / num_points for i in range(num_points + 1)]
    ]

def show_pdf(pdf_file):
    """
    Reads the uploaded PDF file and embeds it in an <iframe> using base64 encoding.
    """
    # Read PDF bytes
    pdf_bytes = pdf_file.read()
    # Encode to base64
    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    # Build an HTML iframe that points to the base64-encoded PDF
    pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" 
                width="570" 
                height="700" 
                type="application/pdf">
        </iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

# 2. Define a function that returns a list of CSS styles for each cell in a row
def color_by_criticality(row):
    """
    Return a list of CSS style strings (one per column) 
    to color the entire row based on row['risk'].
    """
    if row["Materiality Change"] == "Critical":
        return ["background-color: rgba(255,80,80,1.0)"] * len(row)
    elif row["Materiality Change"] == "Moderate":
        return ["background-color: rgba(244,176,132,1.0)"] * len(row)
    elif row["Materiality Change"] == "Minor":
        return ["background-color: rgba(255,217,102,1.0)"] * len(row)
    else:  # e.g., Low or anything else
        return ["background-color: rgba(146, 208,80,1.0)"] * len(row)  # no special background

# ------------------------------------------------------------------
# 4. MAIN SCRIPT (EXECUTE)
# ------------------------------------------------------------------

st.set_page_config(layout="wide")

if st.session_state.logged_in:
    if st.session_state.company_name is not None:
        if st.session_state.role == "KYC":
            if st.session_state.end_button == True:
                show_end_page()
            elif st.session_state.send_qc:
                show_end_page()
            elif st.session_state.end_button_2 == True:
                show_kyc_second_view()
            else:
                show_kyc_first_view()
        elif st.session_state.role == "RD":
            if st.session_state.end_button_2 == True:
                show_end_page()
            else:
                show_rd_view()
        elif st.session_state.the_end:
            show_end_page()
        else:
            show_qc_view()
    else:
        show_dashboard()
else:
    # Otherwise, show the login page
    show_login_page()



# if st.session_state.logged_in:
#     if st.session_state.company_name is not None:
#         if st.session_state.role == "KYC":
#             if st.session_state.end_button == True:
#                 show_end_page()
#             elif st.session_state.send_qc:
#                 show_end_page()
#             elif st.session_state.end_button_2 == True:
#                 show_kyc_second_view()
#             else:
#                 show_kyc_first_view()
#         elif st.session_state.role == "RD":
#             if st.session_state.end_button_2 == True:
#                 show_end_page()
#             else:
#                 show_rd_view()
#         else:
#             show_qc_view()
#     else:
#         show_dashboard()
# else:
#     # Otherwise, show the login page
#     show_login_page()

# if st.session_state.logged_in:
#     if st.session_state.company_name is not None:
#         if st.session_state.role == "KYC":
#             if st.session_state.end_button == True:
#                 show_end_page()
#             else:
#                 show_kyc_first_view()
#         elif st.session_state.role == "RD":
#             if st.session_state.end_button_2 == True:
#                 show_end_page()
#             else:
#                 show_rd_view()
#         else:
#             show_qc_view()
#     else:
#         show_dashboard()
# else:
#     # Otherwise, show the login page
#     show_login_page()