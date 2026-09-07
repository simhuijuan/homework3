def test_import_app():
    # Import should succeed without downloading model weights (lazy load)
    import importlib
    spec = importlib.util.spec_from_file_location("app", "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "create_app")
