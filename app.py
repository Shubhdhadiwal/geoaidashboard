import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
@st.cache_resource
def connect_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("your_credentials.json", scope)
    client = gspread.authorize(creds)
    return client

client = connect_gsheet()
sheet = client.open("GeoAI_Repository")  # Name of your Google Sheet

# --- Sidebar Navigation ---
st.sidebar.header("🧭 GeoAI Repository")
tab_options = {
    "Data Sources": "Data Sources",
    "Tools": "Tools",
    "Free Tutorials": "Free Tutorials",
    "Python Codes (GEE)": "Google Earth EnginePython Codes",
    "Courses": "Courses",
    "Suggest Resource": "Suggestions"
}
selected_tab = st.sidebar.radio("Select Category", list(tab_options.keys()))

# --- Load data from sheet ---
@st.cache_data
def load_data(sheet_name):
    ws = sheet.worksheet(sheet_name)
    df = get_as_dataframe(ws, evaluate_formulas=True)
    df = df.dropna(how='all')  # Drop empty rows
    df.columns = df.iloc[0]    # Set first row as header
    df = df[1:]                # Remove header row
    return df

# --- Display repository data ---
if selected_tab != "Suggest Resource":
    df = load_data(tab_options[selected_tab])

    # Filter
    search = st.sidebar.text_input("🔍 Search")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    if selected_tab == "Data Sources":
        type_filter = st.sidebar.multiselect("📂 Filter by Type", df["Type"].dropna().unique())
        if type_filter:
            df = df[df["Type"].isin(type_filter)]

    st.title(f"🌍 GeoAI Repository – {selected_tab}")

    for idx, row in df.iterrows():
        title = row.get("Data Source") or row.get("Tools") or row.get("Title") or row.get("Tutorials") or "Unnamed"
        st.subheader(f"🔹 {title}")
        st.write(row.get("Description", ""))
        link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
        if pd.notna(link):
            st.markdown(f"[🔗 Access Link]({link})", unsafe_allow_html=True)
        if "Purpose" in row and pd.notna(row["Purpose"]):
            st.markdown(f"**🎯 Purpose:** {row['Purpose']}")
        if "Year/Month of Data Availability" in row and pd.notna(row["Year/Month of Data Availability"]):
            st.markdown(f"**📅 Year/Month:** {row['Year/Month of Data Availability']}")
        st.markdown("---")

# --- Submission Form ---
else:
    st.title("📬 Suggest a New Resource")

    with st.form("submit_resource", clear_on_submit=True):
        name = st.text_input("🔹 Name of the Resource")
        desc = st.text_area("📝 Description")
        link = st.text_input("🔗 Link (URL)")
        type_opt = st.selectbox("📂 Category", ["Data Source", "Tool", "Free Tutorial", "Course", "Python Code"])
        purpose = st.text_input("🎯 Purpose (Optional)")
        year_month = st.text_input("📅 Year/Month of Data Availability (Optional)")
        submitted = st.form_submit_button("Submit")

        if submitted and name and link:
            try:
                ws = sheet.worksheet("Suggestions")
                existing = get_as_dataframe(ws, evaluate_formulas=True)
                new_row = pd.DataFrame([{
                    "Title": name,
                    "Description": desc,
                    "Link": link,
                    "Category": type_opt,
                    "Purpose": purpose,
                    "Year/Month": year_month
                }])
                updated_df = pd.concat([existing, new_row], ignore_index=True)
                updated_df = updated_df.dropna(how='all')
                ws.clear()
                set_with_dataframe(ws, updated_df)
                st.success("✅ Resource submitted successfully!")
            except Exception as e:
                st.error(f"❌ Failed to submit. Error: {e}")
        elif submitted:
            st.warning("Please fill at least Name and Link fields.")
