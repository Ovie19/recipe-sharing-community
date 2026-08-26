import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import engine
from app.dependencies import get_session
from app.models.category import Category
from app.models.user import User
from app.models.recipe import Recipe
from app.services.recipe_services import RecipeService

# Setup in-memory SQLite database for testing
sqlite_url = "sqlite:///:memory:"
test_engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_recipe(client: TestClient):
    recipe_data = {
        "name": "Pancakes",
        "description": "Delicious fluffy pancakes for breakfast",
        "ingredients": ["flour", "milk", "eggs", "sugar"],
        "instructions": ["Mix ingredients", "Cook on a pan"],
        "categories": Category.BREAKFAST,
        "prep_time": 15
    }
    
    response = client.post("/recipes/", json=recipe_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Pancakes"
    assert "id" in data
    assert data["prep_time"] == 15

def test_get_recipes(client: TestClient):
    recipe_data = {
        "name": "Pancakes",
        "description": "Delicious fluffy pancakes for breakfast",
        "ingredients": ["flour", "milk", "eggs", "sugar"],
        "instructions": ["Mix ingredients", "Cook on a pan"],
        "categories": Category.BREAKFAST,
        "prep_time": 15
    }
    client.post("/recipes/", json=recipe_data)
    
    response = client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Pancakes"
