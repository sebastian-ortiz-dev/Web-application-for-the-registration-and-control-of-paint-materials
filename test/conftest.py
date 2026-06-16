import os
import pytest
from create_app import crear_app
from testcontainers.postgres import PostgresContainer
from model_db.class_singlen import instancia_conexion
import time

postgres = PostgresContainer("postgres:17-alpine")
base = os.path.dirname(os.path.abspath(__file__))
sql_ruta = os.path.join(base, "..", "cromasdb.sql")

@pytest.fixture()
def app_start():
    app_test = crear_app("testing")
    app_test.config({ 
        "TEST": True,
    })

    yield app_test

@pytest.fixture(scope="session", autouse=True)
def postgres_db_test():
    postgres.start()

    with postgres as container:
        os.environ["DB_HOST"] = container.get_container_host_ip()
        os.environ["DB_PORT"] = str(container.get_exposed_port(5432))
        os.environ["DB_USERNAME"] = container.username
        os.environ["DB_PASSWORD"] = container.password
        os.environ["DB_NAME"] = container.dbname

    pool, cursor = instancia_conexion.iniciar_conexion()
    cursor.execute("DROP SCHEMA IF EXISTS public CASCADE;")

    with open(sql_ruta, "r") as file:
        sql = file.read()
            
    cursor.execute(sql)
    instancia_conexion.ejecutar_cambio(pool)
    instancia_conexion.cerrar_conexion(cursor, pool)

    yield

@pytest.fixture()
def client(app_test):
    return app_test.test_client()

@pytest.fixture()
def runner(app_test):
    return app_test.test_cli_runner()
