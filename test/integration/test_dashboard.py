def test_dashboard_vista(create_jwt):
    response = create_jwt.get("/principal")

    data_html = response.data.decode("utf-8")

    assert "Vista General" in data_html