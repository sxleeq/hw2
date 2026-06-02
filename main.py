class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient({self.name!r}, {self.quantity}, {self.unit!r})"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self.ingredients = []
        for ing in ingredients:
            self.add_ingredient(ing)

    def add_ingredient(self, ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        new_ingredients = [Ingredient(ing.name, ing.quantity * ratio, ing.unit) for ing in self.ingredients]
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        lines = [self.title]
        for ing in self.ingredients:
            lines.append(f"- {ing}")
        return "\n".join(lines)

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ingredient in scaled.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title):
        self._items = [(ing, rec_title) for (ing, rec_title) in self._items if rec_title != title]

    def get_list(self):
        totals = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in totals:
                totals[key] += ingredient.quantity
            else:
                totals[key] = ingredient.quantity
        result = [Ingredient(name, quantity, unit) for (name, unit), quantity in totals.items()]
        result.sort(key=lambda ing: ing.name)
        return result

    def __add__(self, other):
        combined = ShoppingList()
        combined._items = self._items + other._items
        return combined