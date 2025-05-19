import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

st.set_page_config(page_title="Training Dashboard Uploader", layout="centered")
st.title("📊 Training Dashboard Uploader")

# Initial dashboard data (March, April, May) - replace with actual backend storage if needed
def get_initial_dashboard():
    return pd.DataFrame([
        {'Month': '2025-03', 'Total Trainings': 8, 'DXFleet': 2, 'Phoenix SQL Lite': 6, 'Cancellations': 0, 'No-Shows': 0, 'Pacific': 0, 'Mountain': 1, 'Central': 3, 'Eastern': 3},
        {'Month': '2025-04', 'Total Trainings': 14, 'DXFleet': 6, 'Phoenix SQL Lite': 8, 'Cancellations': 2, 'No-Shows': 0, 'Pacific': 1, 'Mountain': 1, 'Central': 9, 'Eastern': 3},
        {'Month': '2025-05', 'Total Trainings': 1, 'DXFleet': 1, 'Phoenix SQL Lite': 0, 'Cancellations': 0, 'No-Shows': 0, 'Pacific': 0, 'Mountain': 0, 'Central': 0, 'Eastern': 1}
    ])

dashboard_df = get_initial_dashboard()
st.subheader("Current Dashboard")
st.dataframe(dashboard_df)

st.markdown("---")
uploaded_file = st.file_uploader("Upload a monthly training report (CSV)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df['Start Date & Time'] = pd.to_datetime(df['Start Date & Time'], errors='coerce')
        df['Month'] = df['Start Date & Time'].dt.to_period('M').astype(str)

        if df['Month'].nunique() != 1:
            st.error("The file must contain data from only one month.")
        else:
            target_month = df['Month'].iloc[0]
            if target_month in dashboard_df['Month'].values:
                st.error(f"Data from {target_month} is already in the dashboard.")
            else:
                num_dxfleet = df['Event Type Name'].str.contains('DXFleet', case=False, na=False).sum()
                num_phoenix = df['Event Type Name'].str.contains('Phoenix SQL Lite', case=False, na=False).sum()
                num_cancellations = (df['Canceled'] == True).sum() if 'Canceled' in df.columns else 0
                num_noshows = (df['Marked as No-Show'].str.lower() == 'yes').sum()
                tz_counts = df['Invitee Time Zone'].value_counts()
                tz_pacific = tz_counts.get('Pacific Time - US & Canada', 0)
                tz_mountain = tz_counts.get('Mountain Time - US & Canada', 0)
                tz_central = tz_counts.get('Central Time - US & Canada', 0)
                tz_eastern = tz_counts.get('Eastern Time - US & Canada', 0)

                new_row = {
                    'Month': target_month,
                    'Total Trainings': len(df),
                    'DXFleet': num_dxfleet,
                    'Phoenix SQL Lite': num_phoenix,
                    'Cancellations': num_cancellations,
                    'No-Shows': num_noshows,
                    'Pacific': tz_pacific,
                    'Mountain': tz_mountain,
                    'Central': tz_central,
                    'Eastern': tz_eastern
                }

                dashboard_df = pd.concat([dashboard_df, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Data for {target_month} added successfully!")
                st.dataframe(pd.DataFrame([new_row]))

                # Download updated dashboard
                output = BytesIO()
                dashboard_df.to_excel(output, index=False, engine='openpyxl')
                st.download_button("Download Updated Dashboard", output.getvalue(), file_name="Updated_Training_Dashboard.xlsx")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
