import os
import pytest
import shutil
from dotenv import load_dotenv
from create_app import crear_app
from testcontainers.postgres import PostgresContainer
from model_db.class_singlen import instancia_conexion
load_dotenv()

postgres = PostgresContainer("postgres:17-alpine")
base = os.path.dirname(os.path.abspath(__file__))
sql_ruta = os.path.join(base, "..", "cromasdb.sql")
folder_ruta = os.path.join(base, "..", "base_test_images")

@pytest.fixture()
def app_test():
    app_test = crear_app("testing")
    app_test.config.update({ 
        "TEST": True,
        "SECRET_KEY": os.getenv("SECRET_KEY"),
        "UPLOAD_FOLDER": folder_ruta
    })

    yield app_test

@pytest.fixture(scope="session", autouse=True)
def test_folder():
    sub_folder_product = os.path.join(folder_ruta, "productos")
    sub_folder_perfil = os.path.join(folder_ruta, "perfil")
    # Create the folder images test
    os.mkdir(folder_ruta)
    os.mkdir(sub_folder_product)
    os.mkdir(sub_folder_perfil)

    yield

    # delete the folder
    shutil.rmtree(folder_ruta)

@pytest.fixture(scope="session", autouse=True)
def postgres_db_test():
    postgres.start()

    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USERNAME"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname

    with open(sql_ruta, "r") as file:
        sql = file.read()

    pool, cursor = instancia_conexion.iniciar_conexion()
    cursor.execute(sql)
    instancia_conexion.ejecutar_cambio(pool)
    instancia_conexion.cerrar_conexion(cursor, pool)

    yield

    postgres.stop()

@pytest.fixture()
def client(app_test):
    return app_test.test_client()

@pytest.fixture()
def create_jwt(client):
    credentials = ["admin", "123"]

    client.post("/login", data={
        "usuario": credentials[0],
        "clave": credentials[1],
    })

    return client

@pytest.fixture()
def create_jwt_worker(client):
    credentials = ["worker", "123"]

    client.post("/login", data={
        "usuario": credentials[0],
        "clave": credentials[1],
    })

    return client
