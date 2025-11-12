import streamlit as st
import pandas as pd
import plotly.express as px
import ast
import os
import io
import json

# Inject CSS to reduce sidebar width
# st.markdown(
#     """
#     <style>
#     /* Reduce sidebar width */
#     .css-1d391kg {
#         width: 200px;  /* default is about 280px, reduce to 200px or less */
#         min-width: 200px;
#     }
#     /* Also adjust main content margin so it fits well */
#     .css-1outpf7 {
#         margin-left: 200px; 
#     }
#     </style>
#     """, unsafe_allow_html=True
# )

# ------------------- AUTHENTICATION SECTION -------------------
USERNAME = os.environ.get("USERNAME", "admin")
PASSWORD = os.environ.get("PASSWORD", "admin123")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login Required")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username == USERNAME and password == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid username or password")

    st.stop()

def safe_eval(val):
    if pd.isnull(val):
        return None
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return None

# Load your dataframe once
@st.cache_data
def load_data():
    df = pd.read_csv("./data/health_bench_for_srh.csv")
    df['prompt'] = df['prompt'].apply(safe_eval)
    df['rubrics'] = df['rubrics'].apply(safe_eval)
    df['ideal_completions_data'] = df['ideal_completions_data'].apply(safe_eval)
    return df

df = load_data()
srh_df = df[df["label"] == "SRH-Related"]

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Raw Data"])

# Logout button in sidebar
if st.sidebar.button("🔓 Logout"):
    st.session_state.authenticated = False
    st.rerun()

# --------- Page 1: Dashboard ---------
if page == "Dashboard":
    st.title("🩺 HealthBench Dataset Explorer for SRH Conversations")

    st.markdown(
        f"""
        <div style='text-align: center; color: black; font-weight: bold; font-size: 18px;'>
            🔎 Total SRH-Related Samples: 
            <span style='color: darkred; font-weight: bold;'>637</span> 
            out of 5000 total conversations in HealthBench.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Theme Distribution
    st.subheader("📊 1. Theme Distribution")
    theme_counts = srh_df["theme"].value_counts().reset_index()
    theme_counts.columns = ["Theme", "Count"]
    fig1 = px.bar(theme_counts, x="Theme", y="Count", text="Count", title="Theme Distribution of SRH-Related Prompts")
    fig1.update_traces(textposition="outside")
    fig1.update_layout(xaxis_title="Theme", yaxis_title="Count", template="plotly_white", title_x=0.4)
    st.plotly_chart(fig1, use_container_width=True)

    # Conversation Turns Distribution
    st.subheader("💬 2. Conversation Turns Distribution")
    turn_counts = srh_df["conversation_turns"].value_counts().sort_index().reset_index()
    turn_counts.columns = ["Conversation Turns", "Count"]
    fig2 = px.bar(turn_counts, x="Conversation Turns", y="Count", text="Count", title="Distribution of Conversation Turns")
    fig2.update_traces(textposition="outside")
    fig2.update_layout(xaxis_title="Conversation Turns", yaxis_title="Count", template="plotly_white", title_x=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    # Filter by Conversation Turns
    st.subheader("🔎 3. Filter by Conversation Turns")
    selected_turn = st.selectbox("Select number of conversation turns:", sorted(srh_df["conversation_turns"].unique()))
    filtered_turn_df = srh_df[srh_df["conversation_turns"] == selected_turn]
    st.markdown(
        f"""
        <div style='text-align: center; color: #1f77b4; font-weight: bold; font-size: 18px;'>
            🔍 Total samples with {selected_turn} turn(s): {len(filtered_turn_df)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Prompt Details
    st.subheader("4. Prompt Details")
    selected_prompt_id = st.selectbox("Select a Prompt ID", filtered_turn_df["prompt_id"].unique())
    selected_row = srh_df[srh_df["prompt_id"] == selected_prompt_id].iloc[0]

    json_view = {
        "prompt_id": selected_row["prompt_id"],
        "theme": selected_row["theme"],
        "turn_type": "single-turn" if selected_row["conversation_turns"] == 1 else "multi-turn",
        "🗨️ Prompt": selected_row["prompt"],
        "📌 Ideal Completions Data": selected_row["ideal_completions_data"],
        "📋 Rubrics": selected_row["rubrics"]
    }

    st.markdown("**View as JSON:**")
    st.json(json_view)

# --------- Page 2: Raw Data ---------
elif page == "Raw Data":
    st.title("📋 Raw SRH Dataset")
    st.markdown("View the full SRH-related dataframe below. You can download it as an Excel or JSON file.")

    st.dataframe(srh_df, use_container_width=True)

    # Prepare Excel download
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        srh_df.to_excel(writer, index=False, sheet_name='SRH_Data')
    processed_data = output.getvalue()

    # Prepare JSON download
    json_data = srh_df.to_json(orient='records', indent=2)

    # Download buttons side by side
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="⬇️ Download Excel File",
            data=processed_data,
            file_name="healthbench_srh_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:
        st.download_button(
            label="⬇️ Download JSON File",
            data=json_data,
            file_name="healthbench_srh_data.json",
            mime="application/json"
        )