import pytest
from main import Ingredient, Recipe, ShoppingList

def test_ingredient_creation():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_equal_same_name_and_unit():
    a = Ingredient("Мука", 500, "г")
    b = Ingredient("Мука", 200, "г")
    assert a == b

def test_not_equal_different_name():
    a = Ingredient("Мука", 500, "г")
    b = Ingredient("Сахар", 500, "г")
    assert a != b

def test_not_equal_different_unit():
    a = Ingredient("Мука", 500, "г")
    b = Ingredient("Мука", 500, "кг")
    assert a != b

def test_recipe_creation():
    ings = [Ingredient("Мука", 500, "г"), Ingredient("Сыр", 200, "г")]
    recipe = Recipe("Пицца", ings)
    assert recipe.title == "Пицца"
    assert len(recipe.ingredients) == 2
    assert recipe.ingredients[0].name == "Мука"

def test_add_new_ingredient():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    recipe.add_ingredient(Ingredient("Сыр", 200, "г"))
    assert len(recipe.ingredients) == 2

def test_add_existing_ingredient_merges():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 800.0

def test_scale_returns_new_object():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    scaled = recipe.scale(2)
    assert isinstance(scaled, Recipe)
    assert scaled is not recipe
    assert recipe.ingredients[0].quantity == 500.0

def test_scale_multiplies_quantity():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г"), Ingredient("Сыр", 200, "г")])
    scaled = recipe.scale(3)
    assert scaled.ingredients[0].quantity == 1500.0
    assert scaled.ingredients[1].quantity == 600.0

def test_scale_invalid_ratio_raises():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    with pytest.raises(ValueError):
        recipe.scale(0)
    with pytest.raises(ValueError):
        recipe.scale(-5)

def test_recipe_len():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г"), Ingredient("Сыр", 200, "г")])
    recipe.add_ingredient(Ingredient("Мука", 100, "г"))
    assert len(recipe) == 2

def test_add_recipe():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    sl = ShoppingList()
    sl.add_recipe(recipe, 2)
    result = sl.get_list()
    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 1000.0

def test_add_recipe_invalid_portions_raises():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    sl = ShoppingList()
    with pytest.raises(ValueError):
        sl.add_recipe(recipe, 0)
    with pytest.raises(ValueError):
        sl.add_recipe(recipe, -3)

def test_remove_recipe():
    margarita = Recipe("Маргарита", [Ingredient("Мука", 500, "г"), Ingredient("Сыр", 200, "г")])
    quattro = Recipe("4 сыра", [Ingredient("Сыр", 400, "г")])
    sl = ShoppingList()
    sl.add_recipe(margarita, 1)
    sl.add_recipe(quattro, 1)
    sl.remove_recipe("Маргарита")
    result = sl.get_list()
    assert len(result) == 1
    assert result[0].name == "Сыр"

def test_remove_nonexistent_recipe():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    sl = ShoppingList()
    sl.add_recipe(recipe, 1)
    sl.remove_recipe("Несуществующий")
    assert len(sl.get_list()) == 1

def test_get_list_sums_ingredients():
    margarita = Recipe("Маргарита", [Ingredient("Мука", 500, "г")])
    quattro = Recipe("4 сыра", [Ingredient("Мука", 300, "г")])
    sl = ShoppingList()
    sl.add_recipe(margarita, 1)
    sl.add_recipe(quattro, 1)
    result = sl.get_list()
    assert len(result) == 1
    assert result[0].quantity == 800.0

def test_get_list_sorted():
    recipe = Recipe("Пицца", [
        Ingredient("Сыр", 200, "г"),
        Ingredient("Мука", 500, "г"),
        Ingredient("Базилик", 10, "г"),
    ])
    sl = ShoppingList()
    sl.add_recipe(recipe, 1)
    names = [ing.name for ing in sl.get_list()]
    assert names == ["Базилик", "Мука", "Сыр"]

def test_add_combines_lists():
    sl1 = ShoppingList()
    sl1.add_recipe(Recipe("Пицца", [Ingredient("Мука", 500, "г")]), 1)
    sl2 = ShoppingList()
    sl2.add_recipe(Recipe("Хлеб", [Ingredient("Мука", 300, "г")]), 1)
    combined = sl1 + sl2
    result = combined.get_list()
    assert len(result) == 1
    assert result[0].quantity == 800.0

def test_add_does_not_modify_originals():
    sl1 = ShoppingList()
    sl1.add_recipe(Recipe("Пицца", [Ingredient("Мука", 500, "г")]), 1)
    sl2 = ShoppingList()
    sl2.add_recipe(Recipe("Хлеб", [Ingredient("Мука", 300, "г")]), 1)
    assert sl1.get_list()[0].quantity == 500.0
    assert sl2.get_list()[0].quantity == 300.0