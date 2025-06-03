import streamlit as st
import pandas as pd
import time
import base64
from io import BytesIO


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
            st.markdown("---")
            st.markdown("### 📄 Pending Cases")
            st.markdown("---")
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
                                time.sleep(1)
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
                                time.sleep(1)
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
            st.markdown("---")
            st.markdown("### 📄 Pending Cases")
            st.markdown("---")
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
                                time.sleep(1)
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
            <div class="caar-text">CAARmatic</div>
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
                time.sleep(1)

                # In a real app, you’d verify username/password here.
                # For demonstration, we assume it’s always successful.
                placeholder.markdown(f"👤 Log In Successful!")
                time.sleep(1)

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
            <div class="caar-text">CAARmatic</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    if st.session_state.role == "KYC":
        align = st.columns([0.5,1])
        with align[1]:
            st.markdown("### Thanks for using KYC Assistant")
        align = st.columns([0.65,1])
        with align[1]:
            st.write("Redirecting to Home Page...")
        time.sleep(5)
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.company_name = None    
        st.session_state.end_button = False    
        st.rerun()

        


def show_kyc_first_view():
    st.title(f"KYC Assistant - {st.session_state.company_name}")
    st.markdown("---")
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("Fetch Full Serve Data"):
            with st.spinner("Fetching Data"):
                time.sleep(2)
            st.session_state.Fetch_Full_Serve_Data = True

        if st.session_state.Fetch_Full_Serve_Data == True:
            df_full_serve = pd.read_excel("Data/Full Serve.xlsx")
            st.dataframe(df_full_serve, use_container_width=True)

            st.download_button(label="📥 Download Full Serve Data", data = to_excel(df_full_serve),
                    file_name=f'Full Serve Data - {st.session_state.company_name}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            

    with cols[1]:
        if st.button("Fetch Company House Data"):
            with st.spinner("Fetching Data"):
                time.sleep(2)
            st.session_state.Fetch_Company_House_Data = True

        if st.session_state.Fetch_Company_House_Data == True:
            df_Company_House = pd.read_excel("Data/Company House.xlsx")
            st.dataframe(df_Company_House, use_container_width=True)

            st.download_button(label="📥 Download Company House Data", data = to_excel(df_Company_House),
                    file_name=f'Company House Data - {st.session_state.company_name}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    with cols[2]:
        if st.button("Fetch D&B Data"):
            with st.spinner("Fetching Data"):
                time.sleep(2)
            st.session_state.Fetch_D_B_Data = True

        if st.session_state.Fetch_D_B_Data == True:

            df_D_B = pd.read_excel("Data/D&B.xlsx")
            st.dataframe(df_D_B, use_container_width=True)

            st.download_button(label="📥 Download D&B Data", data = to_excel(df_D_B),
                    file_name=f'D&B Data - {st.session_state.company_name}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            

    if (st.session_state.Fetch_Full_Serve_Data) and (st.session_state.Fetch_Company_House_Data) and (st.session_state.Fetch_D_B_Data):
        if st.button("Compare Differences", use_container_width=True):
            st.session_state.compare_difference = True

    if st.session_state.compare_difference == True:
        bd, od, am, tr = st.tabs(["Basic Details", "Ownership Details", "Adverse Media", "Trigger to RD"])

        with bd:

            ################### Table

            cols = st.columns([0.15, 0.15, 1])
            with cols[0]:           
                if st.button("Save Progress", use_container_width=True, key = "bd_sp"):
                    pass

                if st.button("Escalate Case", use_container_width=True, key = "bd_ec"):
                    pass


            with cols[1]:        
                if st.button("Next", use_container_width=True, key = "bd_n"):
                    pass


        with od:

            ################### Table

            cols = st.columns([0.15, 0.15, 1])
            with cols[0]:           
                if st.button("Save Progress", use_container_width=True, key = "od_sp"):
                    pass

                if st.button("Escalate Case", use_container_width=True, key = "od_ec"):
                    pass


            with cols[1]:        
                if st.button("Next", use_container_width=True, key = "od_n"):
                    pass

        
        with am:
            st.markdown(f"### News about {st.session_state.company_name}")
            st.markdown(""":orange-badge[your text here]""")

            if st.button("Next", use_container_width=False, key = "am_n"):
                    pass
            
            if st.button(" Escalate Case ", use_container_width=False, key = "am_ec"):
                    pass
            
        with tr:


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
    world = gpd.read_file(url)
    def iso3_to_2(code):
        try:
            return pycountry.countries.get(alpha_3=code).alpha_2
        except:
            return None
    world['iso2'] = world['id'].map(iso3_to_2)
    proj = world.to_crs(epsg=3857)
    ctr = gpd.GeoSeries(proj.geometry.centroid, crs='epsg:3857') \
             .to_crs(epsg=4326)
    world['centroid_lat'] = ctr.y
    world['centroid_lon'] = ctr.x
    lookup = world.dropna(subset=['iso2']) \
                  .set_index('iso2')[['centroid_lat','centroid_lon']] \
                  .to_dict('index')
    return world, lookup




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
            time.sleep(1)
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
    mask = ((df["3rd_party_company"].isin(selected_companies))
        & (df["Risk"].isin(selected_risks))
    )
    return df[mask].copy()


def show_rd_view():
    st.title(f"Transaction Check - {st.session_state.company_name}")
    st.markdown("---")
    cols = st.columns([1, 1])

    with cols[0]:
        transaction_file = st.file_uploader(f"Upload {st.session_state.company_name} transactions data", type="xlsx", key = "Transaction")
        if transaction_file is not None:
            df_transaction = pd.read_excel(transaction_file)
            df_transaction['Date'] = pd.to_datetime(df_transaction['Date'])
            df_transaction = df_transaction.sort_values('Date')
            st.dataframe(df_transaction)

            with cols[1]:
                sanction_file = st.file_uploader(f"Upload Sanction countries data", type="xlsx", key = "Sanction")
                if sanction_file is not None:
                    df_sanction = pd.read_excel(sanction_file)
                    st.dataframe(df_sanction)

    
    if transaction_file is not None:
        if sanction_file is not None:
            if st.button(f"Analyze Transactions of {st.session_state.company_name}", use_container_width=True):
                st.session_state.analyze_transaction = True

    if st.session_state.analyze_transaction == True:

        ####Slider
        min_date = df_transaction['Date'].dt.date.min()
        max_date = df_transaction['Date'].dt.date.max()
        start_date, end_date = st.slider("Select Date Range:", min_value=min_date, max_value=max_date,
        value=(min_date, max_date),format="YYYY-MM-DD")

        date_filtered_trans = slider_filter_transactions(df_transaction, start_date, end_date)

        align = st.columns([1, 1])
        with align[0]:
            
            #### Company Filter
            st.markdown("#### Filter by Company:")

            # Master "All companies" checkbox
            company_list = date_filtered_trans["3rd_party_company"].unique().tolist()
            company_list.sort()

            def _toggle_all():
                for c in company_list:
                    st.session_state[f"cb_{c}"] = st.session_state["all_companies"]

            st.checkbox(
                "All companies",
                key="all_companies",
                value=True,
                on_change=_toggle_all
            )

            selected_companies: list[str] = []
            for company in company_list:
                def _unset_master(c=company):
                    if not st.session_state[f"cb_{c}"]:
                        st.session_state["all_companies"] = False

                checked = st.checkbox(
                    label=company,
                    key=f"cb_{company}",
                    value=True,
                    on_change=_unset_master
                )
                if checked:
                    selected_companies.append(company)


        with align[1]:
            # Risk multiselect
            st.markdown("#### Filter by Risk Level:")
            risk_levels  = date_filtered_trans["Risk"].unique().tolist() #["High", "Medium", "Low"]
            order = {"Low": 0, "Medium": 1, "High": 2}
            risk_levels = sorted(risk_levels, key=lambda x: order.get(x, 99))

            selected_risks: list[str] = []

            # By default, if there is no session key yet, assume all risk‐boxes are checked
            for risk in risk_levels:
                if f"cb_risk_{risk}" not in st.session_state:
                    st.session_state[f"cb_risk_{risk}"] = True

            for risk in risk_levels:
                checked = st.checkbox(
                    label=risk,
                    key=f"cb_risk_{risk}"
                )

                if checked:
                    selected_risks.append(risk)

        
        date_filtered_trans = filter_transactions(date_filtered_trans, selected_companies, selected_risks)
        

        if date_filtered_trans.empty:
            st.warning("No transactions in the selected filters.")

        else:
            st.dataframe(date_filtered_trans)
        

            st.download_button(label="📥 Download Excel", data = to_excel(date_filtered_trans),
                file_name=f'Transaction Data - {selected_companies} and {selected_risks}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            
            if st.button(f"View Network Graph", use_container_width=True):
                st.session_state.network_graph = True

            if st.session_state.network_graph == True:
                world, lookup = load_world()
                df = add_coordinates(date_filtered_trans, lookup)
                
                # Create base Folium map with countries
                m = create_base_map(world)

                # 7. Handle time controls (slider + buttons)
                play_date = handle_time_controls(df, start_date, end_date)
                if play_date is None:
                    st.warning("No transaction dates available.")

                else:
                    # 8. Draw cumulative transactions on or before play_date
                    cumulative = df[df["Date"].dt.date <= play_date]
                    draw_transactions_on_map(m, cumulative)

                # 9. Display map
                st_folium(m, width=1400, height=600)

                if st.session_state.playing:
                    st.rerun()




def show_qc_view():
    st.markdown("QC")



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
    if row["Criticality Level"] == "Critical Issues":
        return ["background-color: red"] * len(row)
    elif row["Criticality Level"] == "Recommendation":
        return ["background-color: orange"] * len(row)
    elif row["Criticality Level"] == "Minor changes":
        return ["background-color: yellow"] * len(row)
    else:  # e.g., Low or anything else
        return ["background-color: green"] * len(row)  # no special background

# ------------------------------------------------------------------
# 4. MAIN SCRIPT (EXECUTE)
# ------------------------------------------------------------------

st.set_page_config(layout="wide")

if st.session_state.logged_in:
    if st.session_state.company_name is not None:
        if st.session_state.role == "KYC":
            if st.session_state.end_button == True:
                show_end_page()
            else:
                show_kyc_first_view()
        elif st.session_state.role == "RD":
            show_rd_view()
        else:
            show_qc_view()
    else:
        show_dashboard()
else:
    # Otherwise, show the login page
    show_login_page()
