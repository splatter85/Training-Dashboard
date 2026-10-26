# Training Dashboard

This Streamlit app reads the shared monthly training summary from this repository. Upload a report to preview a new month's aggregate counts and download the updated dashboard as CSV or Excel. Uploads do not write to GitHub or change the shared dashboard.

The app calculates total trainings, DXFleet and Phoenix SQL Lite sessions, cancellations, no-shows, and U.S. time-zone counts. It rejects a month already present in the shared dashboard.

## Report format

Upload a CSV containing exactly one month's data and these columns:

- `Start Date & Time`
- `Event Type Name`
- `Canceled`
- `Marked as No-Show`
- `Invitee Time Zone`

## Run

Use a supported Python version:

```sh
pip install -r requirements.txt
streamlit run dashboardapp.py
```

For Streamlit Community Cloud, select `dashboardapp.py` as the entry point. This app requires no GitHub write token. Remove any obsolete `GITHUB_TOKEN` from the deployment's secrets and revoke its credential if it was dedicated to this app. Publishing a downloaded aggregate dashboard is a separate owner-reviewed repository change; do not commit individual training reports.

## Verify the read-only boundary

```sh
python -m unittest discover -s tests -v
```
