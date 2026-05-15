def test_import_app():
    from backend.app.main import app

    assert app.title == "YemenBiz Ledger AI"
