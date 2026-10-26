"""Keep anonymous report processing separate from repository credentials/writes."""

import ast
from io import StringIO
from pathlib import Path
import runpy
import types
import unittest
from unittest.mock import MagicMock, PropertyMock, patch

import pandas as pd


class ReadOnlyBoundaryTests(unittest.TestCase):
    def test_app_has_no_server_credentials_or_http_write_calls(self):
        source = Path(__file__).resolve().parents[1] / "dashboardapp.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                self.assertNotEqual(node.attr, "secrets", "Anonymous uploads must not use server credentials")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                self.assertNotIn(node.func.attr, {"put", "post", "patch", "delete"}, "Uploads must not make HTTP writes")

    def test_uploaded_month_is_downloadable_without_changing_shared_data(self):
        baseline = pd.DataFrame([{
            "Month": "2026-01", "Total Trainings": 1, "DXFleet": 1,
            "Phoenix SQL Lite": 0, "Cancellations": 0, "No-Shows": 0,
            "Pacific": 0, "Mountain": 0, "Central": 1, "Eastern": 0,
        }])
        original = baseline.copy(deep=True)
        upload = StringIO(
            "Start Date & Time,Event Type Name,Canceled,Marked as No-Show,Invitee Time Zone\n"
            "2026-02-01,DXFleet,False,no,Central Time - US & Canada\n"
        )
        streamlit = types.ModuleType("streamlit")
        for name in ("set_page_config", "title", "info", "subheader", "dataframe",
                     "download_button", "markdown", "error"):
            setattr(streamlit, name, MagicMock())
        streamlit.file_uploader = MagicMock(return_value=upload)
        read_csv = pd.read_csv

        def read_local_data(source, *args, **kwargs):
            if isinstance(source, str) and source.startswith("https://raw.githubusercontent.com/"):
                return baseline
            return read_csv(source, *args, **kwargs)

        app = Path(__file__).resolve().parents[1] / "dashboardapp.py"
        with patch.dict("sys.modules", {"streamlit": streamlit}), \
                patch.object(pd, "read_csv", side_effect=read_local_data), \
                patch.object(pd.DataFrame, "style", new_callable=PropertyMock, return_value=MagicMock()), \
                patch("socket.socket.connect", side_effect=AssertionError("Unexpected network access")):
            runpy.run_path(str(app))

        streamlit.error.assert_not_called()
        pd.testing.assert_frame_equal(baseline, original)
        downloads = {
            call.kwargs["file_name"]: call.kwargs["data"]
            for call in streamlit.download_button.call_args_list
        }
        updated = read_csv(StringIO(downloads["Training_Dashboard_updated.csv"]))
        self.assertEqual(updated["Month"].dropna().tolist(), ["2026-01", "2026-02", "TOTAL"])
        self.assertEqual(updated.loc[updated["Month"] == "TOTAL", "Total Trainings"].iloc[0], 2)
        self.assertTrue(downloads["Training_Dashboard_updated.xlsx"].startswith(b"PK"))


if __name__ == "__main__":
    unittest.main()
