import os

import pandas as pd
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Network Security - Phishing Detection",
    page_icon="🛡️",
    layout="wide",
)

# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🛡️ Network Security")
    st.caption("Phishing URL Detection System")
    st.divider()

    st.subheader("Train Model")
    st.write("Trigger a full training pipeline run.")
    if st.button("▶ Run Training Pipeline", use_container_width=True):
        with st.spinner("Training in progress — this may take a few minutes..."):
            try:
                resp = requests.get(f"{API_BASE}/train", timeout=600)
                if resp.status_code == 200:
                    st.success("Training completed successfully!")
                else:
                    st.error(f"Training failed: {resp.text}")
            except Exception as e:
                st.error(f"Could not reach API: {e}")

    st.divider()
    st.caption(f"API: `{API_BASE}`")

# ── main area ─────────────────────────────────────────────────────────────────
st.title("Phishing URL Detection")
st.write("Upload a CSV file to run batch predictions.")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help="CSV must contain the same feature columns used during training.",
)

if uploaded_file is not None:
    # preview
    preview_df = pd.read_csv(uploaded_file)
    uploaded_file.seek(0)  # reset after preview read

    st.subheader("Preview")
    st.dataframe(preview_df.head(5), use_container_width=True)
    st.caption(f"{len(preview_df)} rows · {len(preview_df.columns)} columns")

    if st.button("🔍 Run Predictions", type="primary", use_container_width=False):
        with st.spinner("Running predictions..."):
            try:
                resp = requests.post(
                    f"{API_BASE}/predict",
                    files={"file": (uploaded_file.name, uploaded_file, "text/csv")},
                    timeout=120,
                )

                if resp.status_code == 200:
                    result = resp.json()
                    result_df = pd.DataFrame(result["data"])

                    # ── summary metrics ───────────────────────────────
                    total = result["total_records"]
                    malicious = int((result_df["predicted_column"] == 1).sum())
                    benign = total - malicious

                    st.subheader("Results")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Records", total)
                    col2.metric("Malicious", malicious, delta=None)
                    col3.metric("Benign", benign, delta=None)

                    # ── results table ─────────────────────────────────
                    st.dataframe(
                        result_df,
                        use_container_width=True,
                        column_config={
                            "predicted_column": st.column_config.NumberColumn(
                                "Prediction",
                                help="1 = Malicious, -1 = Benign",
                            )
                        },
                    )

                    # ── download button ───────────────────────────────
                    csv_bytes = result_df.to_csv(index=False).encode()
                    st.download_button(
                        label="⬇ Download Results CSV",
                        data=csv_bytes,
                        file_name="predictions.csv",
                        mime="text/csv",
                    )

                else:
                    st.error(
                        f"Prediction failed (HTTP {resp.status_code}): {resp.text}"
                    )

            except Exception as e:
                st.error(f"Could not reach API: {e}")
