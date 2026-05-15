from backend.app.services.report_service import dashboard_summary


def test_dashboard_summary_shape():
    assert callable(dashboard_summary)
