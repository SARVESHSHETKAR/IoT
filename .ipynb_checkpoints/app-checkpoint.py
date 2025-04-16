import streamlit as st
import pandas as pd
import joblib
import time

# Load model and preprocessing assets
model = joblib.load('xgmodel.pkl')
categorical_columns = joblib.load('xgca.pkl')
saved_features = joblib.load('xgfeatures.pkl')

# Path to continuously updating CSV
csv_file = '/home/mca/Downloads/live_network_flows12.csv'

# Initialize session state
if 'detecting' not in st.session_state:
    st.session_state.detecting = False

# Read latest network flows (last 10 rows)
def get_latest_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data.tail(10)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return pd.DataFrame()

# Convert StartTime for model compatibility
def convert_start_time(data):
    try:
        data['StartTime'] = pd.to_datetime(data['StartTime'], errors='coerce')
        data['StartTime'] = data['StartTime'].astype('int64') // 10**9
    except Exception as e:
        st.error(f"Error converting StartTime: {e}")
    return data

def preprocess_data(data):
    try:
        data = convert_start_time(data)
        data = data.fillna(0)

        # One-hot encode categorical columns
        data = pd.get_dummies(data, columns=categorical_columns)

        # Convert all numeric columns to float
        numeric_columns = ['Dur', 'SrcRate', 'DstRate', 'SrcPkts', 'DstPkts', 'SrcBytes', 'DstBytes', 'StdDev']
        for col in numeric_columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert, set errors to NaN

        # Use reindex to add missing columns efficiently
        data = data.reindex(columns=saved_features, fill_value=0)
        
        return data
    except Exception as e:
        st.error(f"Preprocessing error: {e}")
        return pd.DataFrame()



# Predict network flow as normal or attack
def predict_intrusions(data):
    try:
        processed_data = preprocess_data(data)
        predictions = model.predict(processed_data)
        data['Prediction'] = ['normal' if pred == 0 else 'attack' for pred in predictions]
        return data
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return pd.DataFrame()

# Simulate attack flow and append to CSV
def simulate_attack_flow(attack_type):
    attack_flows = {
        'DDOS': {
            'StartTime': time.time(),
            'Flgs': 'e',
            'Proto': 'udp',
            'SrcAddr': '192.168.100.150',
            'DstAddr': '192.168.100.3',
            'State': 'INT',
            'Dur': 14.19,
            'SrcRate': 0.493336,
            'DstRate': 0.0,
            'SrcPkts': 8,
            'DstPkts': 0,
            'SrcBytes': 480,
            'DstBytes': 0,
            'StdDev': 0.975617
        },
        'Reconnaissance': {
            'StartTime': time.time(),
            'Flgs': 'e',
            'Proto': 'tcp',
            'SrcAddr': '192.168.100.147',
            'DstAddr': '192.168.100.7',
            'State': 'RST',
            'Dur': 0.001259,
            'SrcRate': 0.0,
            'DstRate': 0.0,
            'SrcPkts': 1,
            'DstPkts': 1,
            'SrcBytes': 60,
            'DstBytes': 60,
            'StdDev': 0.0
        },
        'Theft': {
            'StartTime': time.time(),
            'Flgs': 'e',
            'Proto': 'tcp',
            'SrcAddr': '192.168.100.3',
            'DstAddr': '192.168.100.150',
            'State': 'RST',
            'Dur': 0.000129,
            'SrcRate': 0.0,
            'DstRate': 0.0,
            'SrcPkts': 1,
            'DstPkts': 1,
            'SrcBytes': 74,
            'DstBytes': 60,
            'StdDev': 0.0
        }
    }
    simulated_data = pd.DataFrame([attack_flows[attack_type]])
    simulated_data.to_csv(csv_file, mode='a', index=False, header=False)
    st.toast(f"{attack_type} Attack simulated!")

# 🚀 Home Page
st.title("🌐 Real-time Intrusion Detection System")
st.markdown("""
Monitor network flows in real-time and detect **intrusions** using AI.  
Click below to start live detection.
""")

# Show start button if detection hasn't begun
if not st.session_state.detecting:
    if st.button("Start Real-time Flow Detection"):
        st.session_state.detecting = True
        st.rerun()

# ✅ Real-time Detection Dashboard
if st.session_state.detecting:
    st.success("Real-time detection is active!")

    # Attack simulation buttons
    st.markdown("### 🚨 Simulate Attacks")
    col1, col2, col3 = st.columns(3)
    if col1.button("DDOS Attack"):
        simulate_attack_flow('DDOS')
    if col2.button("Reconnaissance Attack"):
        simulate_attack_flow('Reconnaissance')
    if col3.button("Theft Attack"):
        simulate_attack_flow('Theft')

    # Back to Home button
    if st.button("Back to Home"):
        st.session_state.detecting = False
        st.rerun()

    # Display network flows with real-time predictions
    placeholder = st.empty()
    
    # Real-time data loop (refreshes every 5 seconds)
    while True:
        latest_data = get_latest_data(csv_file)
        if not latest_data.empty:
            predictions = predict_intrusions(latest_data)
            styled_data = predictions.style.apply(
                lambda row: ['background-color: #FF4B4B' if row['Prediction'] == 'attack' else 'background-color: #90EE90'] * len(predictions.columns),
                axis=1
            )
            placeholder.dataframe(styled_data, height=400)
        time.sleep(5)
        st.rerun()
