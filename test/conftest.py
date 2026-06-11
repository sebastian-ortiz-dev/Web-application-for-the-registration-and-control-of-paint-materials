import pytest

from create_app import crear_app

@pytest.fixture()
def app_start():
    app_test = crear_app("testing")
    app_test.config({ 
        "TEST": True,
    })

    yield app_test

@pytest.fixture()
def client(app_test):
    return app_test.test_client()

@pytest.fixture()
def runner(app_test):
    return app_test.test_cli_runner()
