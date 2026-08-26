# We are bringing in special tools that help us check if our code works correctly.
import pytest
# We bring in a tool that creates random, unique ID numbers for things.
from uuid import uuid4
# We bring in a tool that lets us pretend to be a user clicking on our app, without opening a browser!
from fastapi.testclient import TestClient
# We bring in tools to talk to our database (where we store information).
from sqlmodel import Session, SQLModel, create_engine
# We bring in a tool that helps our pretend database stay open during our tests.
from sqlmodel.pool import StaticPool

# We bring in our main app so we can test it.
from app.main import app
# We bring in our real database engine, but we won't actually use it here!
from app.database import engine
# We bring in a tool that hands out database connections when the app asks for them.
from app.dependencies import get_session
# We bring in our Category list (like Breakfast, Lunch, Dinner).
from app.models.category import Category
# We bring in the blueprint for what a User looks like.
from app.models.user import User
# We bring in the blueprint for what a Recipe looks like.
from app.models.recipe import Recipe
# We bring in the helper that does the hard work of saving recipes.
from app.services.recipe_services import RecipeService

# We create a fake, temporary database that only exists in the computer's memory! 
# (It will disappear like a dream when we are done.)
sqlite_url = "sqlite:///:memory:"

# We start up the engine for our imaginary database.
test_engine = create_engine(
    sqlite_url, 
    # We tell it "Don't worry about sharing this database, it's just for us."
    connect_args={"check_same_thread": False}, 
    # We tell it "Keep the connection open for as long as we need it."
    poolclass=StaticPool
)

# We are creating a special helper (called a fixture) that gives us a fresh database connection.
@pytest.fixture(name="session")
def session_fixture():
    # We tell the database to create all the empty tables (like putting empty folders in a drawer).
    SQLModel.metadata.create_all(test_engine)
    # We open the drawer to start putting things inside...
    with Session(test_engine) as session:
        # We hand the open drawer to our test so it can play with it!
        yield session
    # When the test is done playing, we destroy all the tables (throw the folders in the trash) so it's clean for next time.
    SQLModel.metadata.drop_all(test_engine)

# We create another special helper to pretend to be the user clicking on the app.
@pytest.fixture(name="client")
def client_fixture(session: Session):
    # We make a little rule that says "When the app asks for the real database, give it our imaginary one instead!"
    def get_session_override():
        return session
    
    # We tell our app about this new rule.
    app.dependency_overrides[get_session] = get_session_override
    # We create our pretend user (the TestClient).
    client = TestClient(app)
    # We let the pretend user go play and test our app!
    yield client
    # When the test is over, we erase our little rule.
    app.dependency_overrides.clear()

# This is our very first test: "Can we create a recipe?"
def test_create_recipe(client: TestClient):
    # We write down the ingredients and instructions for yummy pancakes.
    recipe_data = {
        "name": "Pancakes",
        "description": "Delicious fluffy pancakes for breakfast",
        "ingredients": ["flour", "milk", "eggs", "sugar"],
        "instructions": ["Mix ingredients", "Cook on a pan"],
        "categories": Category.BREAKFAST, # We say this is for Breakfast!
        "prep_time": 15
    }
    
    # Our pretend user asks the app to save the pancake recipe!
    response = client.post("/recipes/", json=recipe_data)
    # We check if the app said "Okay, I did it!" (The number 200 means EVERYTHING IS OK).
    assert response.status_code == 200
    
    # We open up the answer the app gave us.
    data = response.json()
    # We check if the name of the recipe it saved is really "Pancakes".
    assert data["name"] == "Pancakes"
    # We check if the app gave our recipe a special ID badge.
    assert "id" in data
    # We check if it remembered that it takes 15 minutes to make.
    assert data["prep_time"] == 15

# This is our second test: "Can we see all the recipes?"
def test_get_recipes(client: TestClient):
    # We write down our pancake recipe again.
    recipe_data = {
        "name": "Pancakes",
        "description": "Delicious fluffy pancakes for breakfast",
        "ingredients": ["flour", "milk", "eggs", "sugar"],
        "instructions": ["Mix ingredients", "Cook on a pan"],
        "categories": Category.BREAKFAST,
        "prep_time": 15
    }
    # We tell our pretend user to save the pancake recipe to our imaginary database first.
    client.post("/recipes/", json=recipe_data)
    
    # Now, our pretend user asks the app to show us ALL the recipes it has!
    response = client.get("/recipes/")
    # We check if the app said "Okay, here they are!" (200 means OK).
    assert response.status_code == 200
    
    # We open up the list of recipes the app gave us.
    data = response.json()
    # We check to make sure the list isn't empty (there is at least 1 recipe inside).
    assert len(data) > 0
    # We check if the very first recipe on the list is our "Pancakes".
    assert data[0]["name"] == "Pancakes"
