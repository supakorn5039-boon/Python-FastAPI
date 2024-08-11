import pytest
import os
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.db_services import Get_Db
from Models.SqlModels import Base

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[Get_Db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_questions(setup_database):
    response = client.get('/questions/1')
    assert response.status_code == 200


def test_create_question(setup_database):
    question_data = {
        "question_text": "what is the best Python framework?",
        "choices": [
            {"choice_text": "Django", "is_correct": True},
            {"choice_text": "Flask", "is_correct": False}
        ]
    }
    response = client.post('questions', json=question_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Question and choices created successfully"}

