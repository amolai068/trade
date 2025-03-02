import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import os
import re
import datetime

# Define a base directory for file storage
BASE_DIR = "/home/ubuntu/algo_trading"  # Change this as needed
PID_FILE = os.path.join(BASE_DIR, "algo_pid.txt")
LOG_FILE = os.path.join(BASE_DIR, "log_output.log")

# Ensure base directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Start the algorithm
def start_algorithm():
    if os.path.exists(PID_FILE):
        st.error("Algorithm is already running!")
        return

    # Start the supertrend script in the background
    process = subprocess.Popen(
        ["python", os.path.join(BASE_DIR, "supertrend.py")],
        start_new_session=True
    )

    # Save the PID to a file
    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))
    st.success("Algorithm started successfully!")

# Stop the algorithm
def stop_algorithm():
    if not os.path.exists(PID_FILE):
        st.error("Algorithm is not running!")
        return

    # Read the PID from the file
    with open(PID_FILE, "r") as f:
        pid = int(f.read())

    # Terminate the process
    try:
        os.kill(pid, 15)  # 15 is SIGTERM
        st.success("Algorithm stopped successfully!")
        os.remove(PID_FILE)
    except ProcessLookupError:
        st.error("Process not found. Removing stale PID file.")
        os.remove(PID_FILE)

# Streamlit UI
st.title("Option Trading Algorithm")

st.write("Use this app to start or stop the algorithm.")

if st.button("Start Algorithm"):
    start_algorithm()

if st.button("Stop Algorithm"):
    stop_algorithm()

# Check logs
if st.button("Check Logs"):
    if not os.path.exists(LOG_FILE):
        st.error("Log file not found!")
    else:
        log_pattern = re.compile(r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - (?P<message>.+)")
        times, messages = [], []

        with open(LOG_FILE, "r") as file:
            for line in file:
                match = log_pattern.search(line)
                if match:
                    times.append(match.group("timestamp"))
                    messages.append(match.group("message"))

        if messages:
            df = pd.DataFrame(messages, index=times, columns=["Message"])
            st.dataframe(df.tail())  # Show latest logs
        else:
            st.error("No valid log entries found!")

# Check PnL
input_date = st.date_input("Select the date", help="Choose a date from the calendar")
if st.button("Check PnL"):
    if input_date:
        file_name = f"{input_date} mtm_history.csv"
        file_path = os.path.join(BASE_DIR, file_name)

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                st.success(f"File '{file_name}' found!")
                st.dataframe(df.tail(1))

                # Compute percentage and format data
                df["percentage"] = (df["pnl"] / 200000) * 100
                df.rename(columns={"time": "x", "percentage": "y"}, inplace=True)
                df["timestamps"] = pd.to_datetime(df["x"])
                df.set_index("timestamps", inplace=True)

                # Resampling
                resampled_data = df.resample("1T").first()
                resampled_data2 = df.resample("15T").first()
                resampled_data.dropna(inplace=True)

                # Create figure
                fig, ax1 = plt.subplots(figsize=(15, 10))
                hours = [ts.strftime("%H:%M") for ts in resampled_data2.index]
                ax1.set_xticks(range(len(hours)))
                ax1.set_xticklabels(hours)
                ax1.set_xlabel("Time")

                ax2 = ax1.twiny()
                x, y = resampled_data["x"].values, resampled_data["y"].values

                # Plot segments
                for i in range(len(x) - 1):
                    color = "blue" if y[i] > 0 else "purple"
                    ax2.plot(x[i:i+2], y[i:i+2], color=color, linewidth=2)

                ax2.axhline(0, color="black", linestyle="--")
                ax2.set_ylabel("Percentage (%)")
                ax2.set_title("Option Trading Performance")

                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error reading the file: {e}")
        else:
            st.error(f"File '{file_name}' not found in the directory.")
