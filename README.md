# Training-Dashboard
This Streamlit web app allows you to maintain a monthly training summary dashboard by uploading individual training report CSVs. The app extracts key metrics from each uploaded report and appends a new row to the dashboard—only if that month’s data has not already been added.

🚀 Features
Drag-and-drop interface to upload monthly training reports

Automatically calculates:

Total trainings

Count of DXFleet and Phoenix SQL Lite sessions

Number of cancellations and no-shows

Distribution across U.S. time zones

Prevents duplicate entries with a clear error message

Displays the updated dashboard

Download the updated dashboard as an Excel file

📂 How It Works
Upload a .csv file containing training data for a single month.

The app reads the data, validates the month, and processes the following fields:

Start Date & Time (used to determine the reporting month)

Event Type Name

Canceled

Marked as No-Show

Invitee Time Zone

If the month does not already exist in the dashboard, a new row is added.

Download the updated dashboard with one click.

✅ CSV Format Requirements
Your uploaded file must:

Be a .csv file

Contain only one month's worth of data

Include the following columns (case-sensitive):

Start Date & Time

Event Type Name

Canceled

Marked as No-Show

Invitee Time Zone

🛠 Setup Instructions
Requirements
Python 3.8+

streamlit

pandas

openpyxl

Local Setup
bash
Copy
Edit
pip install -r requirements.txt
streamlit run app.py
Streamlit Cloud
To deploy online:

Push this repo to GitHub

Go to streamlit.io/cloud

Click “New app” and select this repo

Deploy and share the app link
