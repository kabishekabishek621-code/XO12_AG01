import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from collector import collect
from classifier import classify

st.set_page_config(page_title="CI Failure Triage Agent", page_icon="🔍", layout="wide")

st.title("🔍 Autonomous CI/CD Failure Triage Agent")
st.markdown("Investigates real failure logs + code diff and decides the correct action.")

st.divider()

st.sidebar.header("Input")
log_file = st.sidebar.text_input("Path to failure log", value="samples/failure.log")
diff_file = st.sidebar.text_input("Path to code diff", value="samples/code.diff")

if st.sidebar.button("Run Triage", type="primary"):
    try:
        data = collect(log_file, diff_file)
        result = classify(data["logs"], data["diff"])

        st.subheader("Classification Result")

        col1, col2, col3 = st.columns(3)
        col1.metric("Classification", result["classification"])
        col2.metric("Confidence", f"{result['confidence']*100:.0f}%")
        col3.metric("Action", result["action"][:50])

        st.divider()
        st.subheader("Reasons")
        for reason in result["reasons"]:
            st.write(f"• {reason}")

        st.subheader("Evidence Used")
        st.json(result["evidence"])

        with st.expander("View Raw Logs"):
            st.code(data["logs"][:2000])

        with st.expander("View Code Diff"):
            st.code(data["diff"][:1500])

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Click **Run Triage** on the left to start.")
