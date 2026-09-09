import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from collector import collect
from classifier import classify

st.set_page_config(
    page_title="CI Failure Triage Agent",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title {font-size: 2.2rem; font-weight: 700; color: #1E88E5;}
    .stMetric {background-color: #f8f9fa; padding: 15px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🔍 Autonomous CI/CD Failure Triage Agent</p>', unsafe_allow_html=True)
st.caption("Investigates real failure logs + code diff and decides the correct action")

st.divider()

# Sample selector
st.sidebar.header("Select Sample Case")
sample = st.sidebar.selectbox(
    "Choose a failure type",
    [
        "Genuine Regression",
        "Flaky Test",
        "Environment Issue",
        "Unclear"
    ]
)

sample_map = {
    "Genuine Regression": ("samples/genuine_failure.log", "samples/genuine_code.diff"),
    "Flaky Test": ("samples/flaky_failure.log", "samples/flaky_code.diff"),
    "Environment Issue": ("samples/environment_failure.log", "samples/environment_code.diff"),
    "Unclear": ("samples/unclear_failure.log", "samples/unclear_code.diff"),
}

log_path, diff_path = sample_map[sample]

if st.sidebar.button("Run Triage", type="primary", use_container_width=True):
    try:
        data = collect(log_path, diff_path)
        result = classify(data["logs"], data["diff"])

        # Result cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Classification", result["classification"])
        with col2:
            st.metric("Confidence", f"{result['confidence']*100:.0f}%")
        with col3:
            st.metric("Action", result["action"][:45] + "..." if len(result["action"]) > 45 else result["action"])

        st.divider()

        st.subheader("Reasons")
        for reason in result["reasons"]:
            st.success(f"• {reason}")

        st.subheader("Evidence Used")
        st.json(result["evidence"])

        with st.expander("View Failure Logs"):
            st.code(data["logs"], language="text")

        with st.expander("View Code Diff"):
            st.code(data["diff"], language="diff")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Select a sample case from the sidebar and click **Run Triage**")
