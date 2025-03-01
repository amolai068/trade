import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import os

# File to store the PID of the supertrend process
PID_FILE = "algo_pid.txt"

# Start the algorithm
def start_algorithm():
    if os.path.exists(PID_FILE):
        st.error("Algorithm is already running!")
        return

    # Start the supertrend script in the background
    process = subprocess.Popen(
        ["python", r"C:\Users\Administrator\Desktop\VS\supertrend.py"], 
        
      
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
st.title("Option Trading Algorithm_1")

st.write("Use this app to start or stop the algorithm.")

if st.button("Start Algorithm"):
    start_algorithm()

if st.button("Stop Algorithm"):
    stop_algorithm()


if st.button('Check logs'):
  
        # Parse the log file

        import pandas as pd
        import re
        log_file = 'log_output.log'
        
        
        
        # Regex to extract timestamp and message
        log_pattern = re.compile(r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - (?P<message>.+)")
        
        with open(log_file, "r") as file:
            times=[]
            messages=[]
            for line in file:
                match = log_pattern.search(line)
                # print(match)
                if match:
                    
                    timestamp = match.group("timestamp")
                    message = match.group("message")
                    times.append(timestamp)
                    messages.append(message)
        
            df=pd.DataFrame(messages,times)
            df.rename(columns={0:'message'},inplace=True)
        
            # st.dataframe(df.head())
            st.dataframe(df.tail())




input_date = st.date_input("Select the date", help="Choose a date from the calendar")
if st.button('check_pnl'):
  
    # Input from the user
    
    
    # Check if input is provided
    if input_date:
        # Generate the expected file name
        file_name = f"{input_date} mtm_history.csv"
        file_path = os.path.join(file_name)
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Read the file into a Pandas DataFrame
            try:
                df = pd.read_csv(file_path)
                st.success(f"File '{file_name}' found!")

              # Display the DataFrame
                st.dataframe(df.tail(1))



                
                import datetime
                data=df
          
                
                # Load the data

                data['percentage'] = (data['pnl'] / 200000) * 100
                data.rename(columns={'time': 'x', 'percentage': 'y'}, inplace=True)
                data.reset_index(inplace=True)
                data['timestamps'] = pd.to_datetime(data['x'])
                
                # Set the timestamps as the index
                data.set_index('timestamps', inplace=True)
                
                # Resample data into intervals
                resampled_data = data.resample('1T').first()
                resampled_data2 = data.resample('15T').first()
                
                # Reset index to make the result user-friendly
                resampled_data.reset_index(inplace=True)
                rs = pd.DataFrame(resampled_data)
                rs2 = pd.DataFrame(resampled_data2)
                
                # Create the hours list for the secondary x-axis
                hours = [datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M") for d in rs2['x']]
                
                # Drop NaN values from resampled data
                rs.dropna(inplace=True)
                
                # Create the figure and primary x-axis plot
                fig, ax1 = plt.subplots(figsize=(15, 10))
                ax1.set_xticks(range(len(hours)))  # Independent tick positions
                ax1.set_xticklabels(hours)        # Labels from the hours list
                ax1.set_xlabel('Time')
                
                ax2 = ax1.twiny()
                
                # Convert x and y to numpy arrays
                x = rs['x'].values
                y = rs['y'].values
                
                # Loop through consecutive points and plot segments
                for i in range(len(x) - 1):
                    # Define the color based on the sign of the current y value
                    color = 'blue' if y[i] > 0 else 'purple'
                    ax2.plot(x[i:i+2], y[i:i+2], color=color, linewidth=2)
                ax2.axhline(0, color='black', linewidth=1, linestyle='--')
                ax2.xaxis.set_visible(False)
                
                # Add labels and title for the plot
                ax2.set_ylabel('percent(%)')
                ax2.set_title('Option Trading')
                
                # Display the plot in Streamlit
                st.pyplot(fig)   
            except Exception as e:
                st.error(f"Error reading the file: {e}")
        else:
            st.error(f"File '{file_name}' not found in the directory.")







    



