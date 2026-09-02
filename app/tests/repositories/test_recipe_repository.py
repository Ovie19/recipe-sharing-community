import uuid
from uuid import uuid4
import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.models import user, category, recipe
from app.models.recipe import Recipe
from app.models.user import User
from app.repositories.recipe_repository import RecipeRepository


# Setup in-memory SQLite database for temporal testing

test_engine = create_engine(
url="sqlite:///:memory:",
connect_args={"check_same_thread": False, "timeout":5}
)

class TestRecipeRepository:
    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(test_engine)
        with Session(test_engine) as session:
            yield session
        SQLModel.metadata.drop_all(test_engine)

# Create recipe → give it to repository → repository saves it → get saved recipe back → test it.

    @pytest.fixture
    def recipe_repository(self, session: Session) -> RecipeRepository:
        return RecipeRepository(session=session)

    def test_saved_recipe(self, recipe_repository: RecipeRepository):
        recipe = Recipe(
            user_id=uuid.uuid4(),
            name="Oha soup",
            description="A delicious Nigerian soup dish",
            categories="DINNER"
            )
        recipe_repository.create(recipe)

        assert recipe_repository.count() == 1

    def test_saved_recipe_two(self, recipe_repository: RecipeRepository):
        recipe = Recipe(
            user_id=uuid.uuid4(),
            name="Oha soup",
            description="A delicious Nigerian soup dish",
            categories="DINNER"
            )

        recipe_two = Recipe(
        user_id=uuid.uuid4(),
        name="Egusi soup",
        description="Another amazing Nigerian soup dish",
        categories="DINNER"
            )
        recipe_repository.create(recipe)
        recipe_repository.create(recipe_two)

        assert recipe_repository.count() == 2


    def test_save_recipe(self , session):
        repo = RecipeRepository(session)
        Recipe(title="Oha soup",
               description="A delicious Nigerian soup dish")

        saved_recipe = repo.save(recipe)
        assert saved_recipe.title is not None
        assert saved_recipe.title == "Oha soup"

    def test_recipe_find_by_id(self,  recipe_repository: RecipeRepository):
        recipe = Recipe(
            user_id=uuid.uuid4(),
            name="Oha soup",
            description="A delicious Nigerian soup dish",
            categories="DINNER"
        )
        saved_recipe = recipe_repository.create(recipe)
        found_recipe = recipe_repository.get_recipe_by_id(saved_recipe.id)
        assert found_recipe is not None
        assert found_recipe.name == "Oha soup"
        assert found_recipe.description == "A delicious Nigerian soup dish"

    def test_find_by_id_returns_none_when_recipe_does_not_exist(self, recipe_repository: RecipeRepository):
        found_recipe = recipe_repository.get_recipe_by_id(uuid4())
        assert found_recipe is None

    def test_view_all_recipes(self, recipe_repository: RecipeRepository):
        recipe = Recipe(
            user_id=uuid.uuid4(),
            name="Oha soup",
            description="A delicious Nigerian soup dish",
            categories="DINNER"
        )
        recipe_repository.create(recipe)
        recipes = recipe_repository.view_all_recipes()
        assert len(recipes) == 1
        assert recipes[0].name == "Oha soup"


    def test_find_by_title(self,recipe_repository: RecipeRepository):
        recipe = Recipe(user_id=uuid.uuid4(), name="Oha soup", description="A delicious Nigerian soup dish", categories="DINNER" )
        saved_recipe = recipe_repository.create(recipe)
        all_recipes = recipe_repository.view_all_recipes()
        found_recipe = all_recipes[0]
        assert found_recipe is not None
        assert found_recipe.name == "Oha soup"
        assert found_recipe.user_id == saved_recipe.user_id

    def test_find_by_title_returns_none_when_recipe_does_not_exist(self, recipe_repository: RecipeRepository):
        all_recipes = recipe_repository.view_all_recipes()
        found_recipe = None
        for recipe_count  in  all_recipes:
            if recipe_count.name == "This dish is nonexistent":
                found_recipe = recipe_count
                break
        assert found_recipe is None


