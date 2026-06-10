import pandas as pd
import streamlit as st
import time 
import os 

st.set_page_config(page_title="Decision Support Tool for Data Spaces Tethering", layout="wide")

#CSS für info i und multiselect
st.markdown("""
    <style>
    /* ===== MULTISELECT TAGS FULL TEXT ===== */
    [data-baseweb="tag"] {
        max-width: fit-content !important;
        width: fit-content !important;
        height: auto !important;
        padding: 2px 6px !important;
    }
    [data-baseweb="tag"] span {
        overflow: visible !important;
        text-overflow: unset !important;
        white-space: nowrap !important;
        max-width: none !important;
    }
    .stMultiSelect div[data-baseweb="select"] {
        min-height: 44px !important;
    }

    /* --- DEZENTER TOOLTIP STYLE --- */
    .info-container {
        display: inline-flex;
        align-items: center;
        position: relative;
        font-weight: bold;
    }
    .info-icon {
        display: inline-block;
        width: 16px;
        height: 16px;
        color: #888; 
        border: 1px solid #ccc; 
        border-radius: 50%;
        text-align: center;
        line-height: 14px;
        font-size: 10px;
        margin-left: 8px; 
        cursor: help;
        position: relative;
        transition: all 0.2s;
    }
    .info-icon:hover {
        color: #333;
        border-color: #333;
        background-color: #f9f9f9;
    }
    .info-icon .tooltiptext {
        visibility: hidden;
        width: 280px;
        background-color: #ffffff;
        color: #333;
        text-align: left;
        border-radius: 6px;
        padding: 12px;
        position: absolute;
        z-index: 9999;
        bottom: 130%; 
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-weight: normal;
        font-size: 13px;
        line-height: 1.4;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #eee;
    }
    .info-icon .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border-width: 6px;
        border-style: solid;
        border-color: #ffffff transparent;
    }
    .info-icon:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)

#Daten aus CSV laden
@st.cache_data
def load_data():
    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "DataSpace.csv")

        df = pd.read_csv(file_path, sep=";", encoding="utf-8")
        df = df.fillna("")
        return df

    except FileNotFoundError:
        st.error("Die Datei 'DataSpace.csv' wurde nicht gefunden.")
        return pd.DataFrame()

df = load_data()

#Auswahlmöglichkeiten sammeln
def get_unique_options(column_name):
    if column_name not in df.columns: 
        return []
    all_terms = set() 
    valid_entries = df[column_name].replace("", None).dropna().unique()
    for entry in valid_entries:
        parts = [p.strip() for p in str(entry).split(",")]
        for p in parts:
            if p: 
                all_terms.update([p])
    return sorted(list(all_terms))

#Tool start 
empty_l, col_main, empty_r = st.columns([1, 8, 1])

with col_main:
    st.title("Decision Support Tool for Data Spaces Tethering 🤖")
    
    st.markdown("""
        <div style="
            background-color: #e8f4f8; 
            padding: 16px; 
            border-radius: 6px; 
            border-left: 5px solid #29b5e8;
            color: #1f4e5b;
            margin-bottom: 25px;
        ">
            <h1 style="font-size:22px; text-align:center;">Welcome to the Decision Support Tool for Data Spaces Tethering! 🤖</strong></b></h1><br><br>
            Select and weight your requirements to the most suitable data space for your organization.<br><br>
            <b>How it works:</b> <br>A score is calculated by matching your requirements with each data space of our database, weighted by your selected preferences.
                You can also apply filters as hard constraints. A data space must fulfill them to be included.<br>
                Then the tool recommends the top three matching data spaces based on the highest score.<br>
                You can also ask our gemini-2.5-flash based AI Assistant for further insights and explanations. <br><br>
                <b>Let’s find the right data space!</b>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown('''
            <div class="info-container">
                <span style="font-size: 1.5rem;">Which sector does your organization operate in?</span>
                <div class="info-icon">i
                    <span class="tooltiptext">This is a hard constraint that a data space must fulfill.</span>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    user_domain = st.selectbox("", 
                               options=get_unique_options("Domain"),
                               index=None, placeholder="Select...", label_visibility="collapsed")

    st.markdown("---")

    # --- TABELLEN-HEADER ---
    LAYOUT_RATIO = [4.5, 2.5, 3] 
    h1, h2, h3 = st.columns(LAYOUT_RATIO, vertical_alignment="center")

    with h1:
        st.markdown('''
            <div class="info-container">
                <span style="font-size: 1.2rem;">Requirements</span>
                <div class="info-icon">i
                    <span class="tooltiptext">Choose specific characteristics your data space should have.</span>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    with h2:
        st.markdown('''
            <div style="display: flex; justify-content: center; width: 100%;">
                <div class="info-container">
                    <span style="font-size: 1.2rem; font-weight: bold;">Logic</span>
                    <div class="info-icon">i
                        <span class="tooltiptext">
                            Defines the matching logic of each requirement.<br><br>
                            <b>OR:</b> at least one characteristic must fit.<br>
                            <b>AND:</b> all characteristics must fit.<br>
                            <b>FILTER:</b> hard constraint.
                        </span>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    with h3:
        st.markdown('''
            <div style="display: flex; justify-content: center; width: 90%; margin: 0 auto;">
                <div class="info-container">
                    <span style="font-size: 1.2rem; font-weight: bold;">Weight</span>
                    <div class="info-icon">i
                        <span class="tooltiptext">Decide how important this characteristic is for you (0.0 - 1.0). The sum must be 1</span>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 35px;'></div>", unsafe_allow_html=True)

    def input_row(label, col_name, default_w, help_text):
        st.markdown(f'''
            <div class="info-container" style="margin-bottom: 5px;">
                <span>{label}</span>
                <div class="info-icon">i
                    <span class="tooltiptext">{help_text}</span>
                </div>
            </div>
        ''', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(LAYOUT_RATIO, vertical_alignment="center")
        with c1:
            choice = st.multiselect(label, options=get_unique_options(col_name), 
                                    placeholder="Select...", label_visibility="collapsed", key=f"sel_{col_name}")
        with c2:
            st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
            logic = st.radio(label, ["OR", "AND", "FILTER"], horizontal=True, 
                             label_visibility="collapsed", key=f"log_{col_name}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            if logic != "FILTER":
                weight = st.slider(label, 0.0, 1.0, default_w, step=0.05, 
                                   label_visibility="collapsed", key=f"w_{col_name}")
            else:
                st.markdown('<p style="color: #888; font-size: 0.8rem; margin: 0; padding: 0; text-align: center;">🔒 K.O. Criterion</p>', unsafe_allow_html=True)
                weight = 0.0
                    
        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
        return choice, logic, weight

    
    u_stage, l_stage, w_stage = input_row("Stage", "Stage", 0.2, """Phase of Development.<br><br> 
                                          <b>Exploratory:</b> Initiative starts, this may include collecting requirements.<br>
                                          <b>Implementation:</b> Detailed plan, pilot development.<br>
                                          <b>Operational:</b> Validated implementation, first use cases become operational. """)
    u_geo, l_geo, w_geo = input_row("Geographical Focus", "Geo", 0.2, "Geographical Focus.")
    u_inter, l_inter, w_inter = input_row("Interoperability", "Interoperability", 0.2, """Ability to exchange, understand and trace data across different systems and organizations.<br><br> 
                                          <b>Data Exchange:</b> Shares data between participants.<br>
                                          <b>Data Models and Formats:</b> Ensures that data is structured in a consistent way so all participants can understand and use it correctly.<br>
                                          <b>Provenance and Traceability:</b> Tracks data origin and usage across the entire lifecycle """)
    u_sov, l_sov, w_sov = input_row("Sovereignty & Trust", "Data Sovereignity and Trust", 0.2, """Ensures that participants maintain control over their data while enabling secure and trusted interactions.<br><br> 
                                          <b>Access and usage policies and control:</b> Defines who can access which data under which conditions.<br>
                                          <b>Identity Management:</b> Ensures that all participants are identified and authenticated.<br>
                                          <b>Trust:</b> Builds confidence between participants through transparency and compliance.""")
    u_val, l_val, w_val = input_row("Value Creation", "Value Creation", 0.2,"""How data spaces enable participants to share, discover and monetize services and offerings.<br><br> 
                                          <b>Data and Service and Offerings descriptions:</b> Describes data, service and offerings available.<br>
                                          <b>Marketplaces and usage accounting:</b> Ensures fair value distribution.<br>
                                          <b>Publication and Discovery:</b> Allows data and services to be published and discovered. """)

    #Scoring logic
    active_sliders = sum([1 for l in [l_stage, l_geo, l_inter, l_sov, l_val] if l != "FILTER"])
    total_w = round(w_stage + w_geo + w_inter + w_sov + w_val, 5)
    st.markdown("---")

    #score Berechnung
    # score Berechnung
    def calculate_score_and_details(row):
        if user_domain and user_domain.lower() not in str(row.get("Domain", "")).lower():
            return 0.0, [], []
            
        criteria = {
            "Stage": (u_stage, w_stage, l_stage), 
            "Geographical Focus": (u_geo, w_geo, l_geo), 
            "Interoperability": (u_inter, w_inter, l_inter), 
            "Sovereignty & Trust": (u_sov, w_sov, l_sov), 
            "Value Creation": (u_val, w_val, l_val)
        }
        
        col_mapping = {
            "Stage": "Stage", "Geographical Focus": "Geo", "Interoperability": "Interoperability",
            "Sovereignty & Trust": "Data Sovereignity and Trust", "Value Creation": "Value Creation"
        }
        
        score = 0.0
        matching_details = []
        missing_details = []
        
        for label, (choices, weight, mode) in criteria.items():
            db_col = col_mapping[label]
            if choices:
                val = str(row.get(db_col, "")).lower()
                passed_choices = [c for c in choices if str(c).lower().strip() in val]
                failed_choices = [c for c in choices if str(c).lower().strip() not in val]
                
                any_m = len(passed_choices) > 0
                all_m = len(failed_choices) == 0
                
                if mode == "FILTER": 
                    if not all_m: return 0.0, [], []
                    matching_details.append(f"**{label}**: {', '.join(passed_choices)}")
                elif mode == "AND":
                    if all_m: 
                        score += weight
                        matching_details.append(f"**{label}**: {', '.join(passed_choices)}")
                    else:
                        if passed_choices: matching_details.append(f"**{label} (Partial)**: {', '.join(passed_choices)}")
                        missing_details.append(f"**{label}**:  {', '.join(failed_choices)}")
                elif mode == "OR":
                    if any_m: 
                        score += weight
                        matching_details.append(f"**{label}**: {', '.join(passed_choices)}")
                        if failed_choices: missing_details.append(f"**{label}**:  {', '.join(failed_choices)}")
                    else:
                        missing_details.append(f"**{label}**:  all selected ({', '.join(failed_choices)})")
                        
        return score * 100, matching_details, missing_details

    # === WICHTIG: Korrekte Einrückung auf Hauptebene von col_main ===
    # Überprüfen, ob die Gewichte 1 ergeben
    weights_valid = (active_sliders == 0 and total_w == 0.0) or total_w == 1.0

    if weights_valid:
        st.success(f"Configuration valid! Active weight sum: {total_w}")
        
        # Match Start -> disabled=True entfernt & eindeutigen key vergeben
        if st.button("Find match", use_container_width=True, key="enabled_find_match"):
            if not user_domain:
                st.error("Please select a domain first.")
            else:
                results = []
                for _, row in df.iterrows():
                    score, passed, failed = calculate_score_and_details(row)
                    if score > 0:
                        row_dict = row.to_dict()
                        row_dict["match_score"] = score
                        row_dict["passed_criteria"] = passed
                        row_dict["failed_criteria"] = failed
                        results.append(row_dict)
                
                # Sortieren und Top 3 filtern
                results = sorted(results, key=lambda x: x["match_score"], reverse=True)[:3]
                
                st.session_state["stored_matches"] = results
                st.session_state["search_performed"] = True
                st.session_state["user_inputs"] = {
                    "domain": user_domain,
                    "stage": u_stage, "geo": u_geo,
                    "interoperability": u_inter,
                    "sovereignty": u_sov, 
                    "value_creation": u_val
                }
    else:
        st.warning(f"The active weight sliders sum up to {total_w}. Please adjust them to equal 1.0 to enable matching!")
        # Hier wird der deaktivierte Button mit einem eindeutigen key versehen
        st.button("Find match", use_container_width=True, disabled=True, key="disabled_find_match")
        
        # Wenn Nutzer das Gewicht ungültig macht, alte Suchen ausblenden
        if "search_performed" in st.session_state:
            st.session_state["search_performed"] = False

    # Ergebnis Anzeige
    if st.session_state.get("search_performed", False):
        st.subheader("Recommendations:")
        matches = st.session_state.get("stored_matches", [])
        if matches:
            for row in matches:
                with st.container(border=True):
                    c_l, c_r = st.columns([5, 1], vertical_alignment="center")
                    with c_l:
                        st.markdown(f"### {row['Name']}")
                        st.metric("Match", f"{int(row['match_score'])}%")
                    #    st.write(f"**Domain:** {row['Domain']} | **Stage:** {row['Stage']}")
                        
                        # Neue Gegenüberstellung der Merkmale
                        col_p, col_f = st.columns(2)
                        with col_p:
                            st.markdown("##### ✅ Matching Requirements:")
                            if row.get("passed_criteria"):
                                for item in row["passed_criteria"]: st.markdown(f"- {item}")
                            else: st.caption("No specific sub-requirements matched.")
                                
                        with col_f:
                            st.markdown("##### ❌ Missing Requirements:")
                            if row.get("failed_criteria"):
                                for item in row["failed_criteria"]: st.markdown(f"- {item}")
                            else: st.caption("None! All selected requirements are met.")
                        
                        # Der saubere Link am Ende
                        space_url = row.get("URL", "").strip()
                        if space_url:
                            st.write("")
                            st.page_link(space_url, label="Visit Website", icon="🔗")
                            
                  #  with c_r:
                   #     st.metric("Match", f"{int(row['match_score'])}%")
        else:
            st.warning("No matches found for the selected criteria.")
            
        # Chatbot
        st.markdown("---")
        st.subheader("🤖 Ask questions about your results")
        st.caption("Our gemini-2.5-flash based AI Assistant can help you understand why these Data Spaces match your requirements and answers further questions.")

        # Chat-Verlauf initialisieren
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Bisherigen Chatverlauf anzeigen
        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Neuer User-Input
        if user_query := st.chat_input("E.g., Why did the first option get a higher score than the second?"):
            # User-Nachricht sofort anzeigen
            with st.chat_message("user"):
                st.markdown(user_query)
            
            # 4. System-Prompt
            context_prompt = f"""
            You are an expert advisor for Data Spaces. The user has used a Decision Support Tool.
            Here is the context of their search:
            - Selected Domain: {st.session_state.get('user_inputs', {}).get('domain', 'N/A')}
            - User Requirements: {st.session_state.get('user_inputs', {})}
            
            The top recommended Data Spaces found in the database are:
            {st.session_state.get('stored_matches', [])}
            
            Answer the user's question accurately based on this context and general knowledge about Data Spaces. 
            Keep it concise and professional.
            """

            # KI Antwort 
            with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    
                    max_retries = 3
                    success = False
                    
                    for attempt in range(max_retries):
                        try:
                            from google import genai
                            from google.genai import types
                            
                            api_key = st.secrets["GEMINI_API_KEY"]
                            client = genai.Client(api_key=api_key)
                            
                            # Verlauf aufbauen
                            gemini_contents = []
                            for h in st.session_state["chat_history"]:
                                role = "model" if h["role"] == "assistant" else "user"
                                gemini_contents.append(types.Content(role=role, parts=[types.Part.from_text(text=h["content"])]))
                            gemini_contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_query)]))
                            
                            # API Aufruf
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=gemini_contents,
                                config=types.GenerateContentConfig(
                                    system_instruction=context_prompt,
                                    temperature=0.4,
                                    tools=[{"google_search": {}}]
                                )
                            )
                            
                            assistant_response = response.text
                            message_placeholder.markdown(assistant_response)
                            
                            # Speichern
                            st.session_state["chat_history"].append({"role": "user", "content": user_query})
                            st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})
                            success = True
                        
                            break 
                            
                        except Exception as e:
                            if "503" in str(e) or "UNAVAILABLE" in str(e):
                                if attempt < max_retries - 1:
                                    message_placeholder.info(f"Server busy (Attempt {attempt+1}/{max_retries}). Retrying in 2 seconds...")
                                    time.sleep(2)
                                    continue
                                else:
                                    st.error("The AI server is still overloaded. Please try again in a few minutes.")
                            else:
                                st.error(f"Error: {e}")
                                break
                            