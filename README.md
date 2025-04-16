# Real-time Intrusion Detection

A powerful, machine-learning-driven tool to monitor network traffic and detect intrusions in real time using Streamlit.

## Prerequisites

- Python 3.7 or higher
- pip package manager

## Installation

1. Clone or download this repository.

2. Install the required Python packages:

```bash
pip install streamlit pandas joblib
```

## Running the Application

1. Ensure the following files are present in the project directory:

- `app2.py` (the main Streamlit app)
- `xgmodel.pkl` (pre-trained machine learning model)
- `xgca.pkl` (categorical columns for preprocessing)
- `xgfeatures.pkl` (saved features for preprocessing)

2. The app reads live network flow data from a CSV file located at:

```
/home/mca/Downloads/live_network_flows12.csv
```

Make sure this file exists and is being updated with network flow data.

3. Run the Streamlit app:

```bash
streamlit run app2.py
```

4. Open the URL provided by Streamlit (usually http://localhost:8501) in your web browser.

## Features

- Real-time monitoring of network flows
- Machine learning powered intrusion detection
- Simulate different types of attacks (DDOS, Reconnaissance, Theft) to test detection

## Simulating Attacks

Use the buttons in the app interface to simulate different attack types. These simulated flows will be appended to the live CSV file and detected by the model.

## File Descriptions

- `app2.py`: Main Streamlit application script
- `xgmodel.pkl`: Pre-trained XGBoost model for intrusion detection
- `xgca.pkl`: List of categorical columns used for one-hot encoding
- `xgfeatures.pkl`: List of features expected by the model
- `live_network_flows12.csv`: CSV file containing live network flow data (updated externally)

## Troubleshooting

- Ensure all required files are in place before running the app.
- If the app shows errors reading the CSV, verify the file path and permissions.
- If predictions fail, check that the model and preprocessing files are correctly loaded.

## License

This project is provided as-is without any warranty.
