    # --- Load Excel ---
    @st.cache_data
    def load_data(sheet_name):
        df = pd.read_excel("Geospatial Data Repository (1).xlsx", sheet_name=sheet_name)
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.dropna(subset=[df.columns[0]])
        return df

    # Sidebar Navigation
    sheet_options = {
        "Data Sources": "Data Sources",
        "Tools": "Tools",
        "Free Tutorials": "Free Tutorials",
        "Python Codes (GEE)": "Google Earth EnginePython Codes",
        "Courses": "Courses",
    }

    selected_tab = st.sidebar.radio("Select Category", list(sheet_options.keys()))
    df = load_data(sheet_options[selected_tab])
    st.title(f"🌍 GeoAI Repository – {selected_tab}")

    if selected_tab == "Data Sources":
        type_filter = st.sidebar.multiselect("Filter by Type", df["Type"].dropna().unique())
        if type_filter:
            df = df[df["Type"].isin(type_filter)]

    for idx, row in df.iterrows():
        st.subheader(str(row.get("Data Source") or row.get("Tools") or row.get("Title") or row.get("Tutorials") or "Unnamed"))
        st.write(row.get("Description", ""))
        link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
        if pd.notna(link):
            st.markdown(f"[🔗 Access Link]({link})", unsafe_allow_html=True)
        if "Purpose" in row:
            st.markdown(f"**Purpose:** {row['Purpose']}")
        if "Year/Month of Data Availability" in row:
            st.markdown(f"**Year/Month:** {row['Year/Month of Data Availability']}")
        st.markdown("---")

# --- If login fails ---
elif authentication_status is False:
    st.error("Username or password is incorrect")

# --- If login not attempted yet ---
elif authentication_status is None:
    st.warning("Please enter your username and password")
