import streamlit as st
import pandas as pd
import joblib
import time
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Network Intrusion Detection System",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI-Based Network Intrusion Detection System")
st.markdown("### Real-Time Intrusion Detection Dashboard")
st.write("This dashboard simulates live network traffic using the NSL-KDD test dataset.")

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_artifacts():

    required_files = [
        "models/nids_model.pkl",
        "models/feature_encoders.pkl",
        "models/target_encoder.pkl"
    ]

    for file in required_files:
        if not os.path.exists(file):
            st.error(f"Missing file: {file}")
            st.info("Please run train_model.py first.")
            st.stop()

    model = joblib.load("models/nids_model.pkl")
    encoders = joblib.load("models/feature_encoders.pkl")
    target_encoder = joblib.load("models/target_encoder.pkl")

    return model, encoders, target_encoder

try:
    model, encoders, target_encoder = load_artifacts()
    st.sidebar.success("✅ Model Loaded")
except Exception as e:
    st.error(f"Error loading model:\n{e}")
    st.stop()

# -----------------------------
# DATASET
# -----------------------------
columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted",
    "num_root","num_file_creations","num_shells","num_access_files",
    "num_outbound_cmds","is_host_login","is_guest_login","count",
    "srv_count","serror_rate","srv_serror_rate","rerror_rate",
    "srv_rerror_rate","same_srv_rate","diff_srv_rate",
    "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
    "dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "attack","difficulty"
]

@st.cache_data
def load_data():

    if not os.path.exists("data/KDDTest+.txt"):
        st.error("❌ Dataset not found: data/KDDTest+.txt")
        st.info("Please place KDDTest+.txt inside the data folder.")
        st.stop()

    return pd.read_csv("data/KDDTest+.txt", names=columns)

df = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Simulation Settings")

speed = st.sidebar.slider(
    "Packet Speed (seconds)",
    0.1,
    2.0,
    0.4
)

packet_limit = st.sidebar.slider(
    "Packets to Simulate",
    50,
    1000,
    300
)

start = st.sidebar.button("▶ Start Simulation")

# -----------------------------
# METRICS
# -----------------------------
m1, m2, m3 = st.columns(3)

metric_packets = m1.empty()
metric_normal = m2.empty()
metric_attack = m3.empty()

st.markdown("---")

left, right = st.columns([2,1])

log_placeholder = left.empty()
chart_placeholder = right.empty()

alert_placeholder = st.empty()

# -----------------------------
# START
# -----------------------------
if start:

    scanned = 0
    normal = 0
    attack = 0

    logs = []

    # Progress bar
    progress = st.progress(0)

    for _, row in df.head(packet_limit).iterrows():

        scanned += 1

        # Update progress bar
        progress.progress(scanned / packet_limit)

        packet = row.copy()

        actual_attack = packet["attack"]

        features = packet.drop(labels=["attack", "difficulty"])

        features = pd.DataFrame([features])

        # Encode categorical columns
        for col in ["protocol_type", "service", "flag"]:
            le = encoders[col]
            features[col] = le.transform(features[col])

        # Prediction
        prediction = model.predict(features)[0]

        confidence = model.predict_proba(features).max() * 100

        label = target_encoder.inverse_transform([prediction])[0]

        if label == "attack":

            attack += 1

            status = "🚨 ATTACK"

            alert_placeholder.error(
                f"""
### 🚨 Intrusion Detected

Packet **#{scanned}**

Actual Dataset Label: **{actual_attack}**

AI Confidence: **{confidence:.2f}%**
"""
            )

        else:

            normal += 1

            status = "🟢 NORMAL"

            alert_placeholder.success(
                f"""
Packet #{scanned}

Traffic appears normal.

Confidence: **{confidence:.2f}%**
"""
            )

        # Metrics
        metric_packets.metric("Packets Scanned", scanned)
        metric_normal.metric("Normal Traffic", normal)
        metric_attack.metric("Threats", attack)

        # Packet Log
        logs.insert(
            0,
            {
                "Packet": scanned,
                "Protocol": row["protocol_type"],
                "Service": row["service"],
                "Source Bytes": row["src_bytes"],
                "Prediction": status,
                "Dataset Label": actual_attack
            }
        )

        log_placeholder.dataframe(
            pd.DataFrame(logs[:15]),
            use_container_width=True,
            height=500
        )

        chart_df = pd.DataFrame(
            {
                "Traffic": [normal, attack]
            },
            index=["Normal", "Attack"]
        )

        chart_placeholder.bar_chart(chart_df)

        time.sleep(speed)

    # Finish progress bar
    progress.empty()

    st.success("✅ Simulation Completed Successfully!")

    st.balloons()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Developed using Python • Scikit-Learn • Streamlit • NSL-KDD Dataset")