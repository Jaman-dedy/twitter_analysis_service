import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import subprocess

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.db.base import Base
from app.main import app, init_db
from app.config import settings

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    subprocess.run(["python", f"{project_root}/create_test_db.py"], check=True)
    
    test_db_url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}_test"
    engine = create_engine(test_db_url)
    
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    Base.metadata.drop_all(bind=engine)
    conn = engine.connect()
    conn.execute("COMMIT")
    conn.execute(f"DROP DATABASE {settings.POSTGRES_DB}_test")
    conn.close()

@pytest.fixture(scope="function")
def db_session(create_test_database):
    Session = sessionmaker(bind=create_test_database)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope="module")
def client():
    return TestClient(app)