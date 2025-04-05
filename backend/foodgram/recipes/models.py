from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Recipe(models.Model):
    """Recipe model"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="автор",
    )
    name = models.CharField("название", max_length=256)
    text = models.TextField(verbose_name="описание")
    ingredients = models.ManyToManyField(
        "ingredient",
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name="ингредиенты",
    )
    cooking_time = models.PositiveIntegerField(
        "время приготовления (в минутах)",
        validators=[MinValueValidator(1)],
    )
    image = models.ImageField("изображение", upload_to="recipes/")

    class Meta:
        ordering = ("name",)
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model"""

    name = models.CharField(
        "название",
        max_length=256,
    )
    measurement_unit = models.CharField(
        "единица измерения",
        max_length=256,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique_ingredient",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.measurement_unit}"


class RecipeIngredient(models.Model):
    """Many to many relationship between Recipe and Ingredient"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name="рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name="ингредиент",
    )
    amount = models.PositiveIntegerField(
        "количество",
        validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = ("recipe", "ingredient")
        verbose_name = "ингредиент в рецепте"
        verbose_name_plural = "ингредиенты в рецепте"

    def __str__(self):
        return (
            f"{self.ingredient} - "
            f"{self.amount} {self.ingredient.measurement_unit}"
        )


class UserRecipeRelation(models.Model):
    """Model for user recipe relations"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="%(class)ss",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
        related_name="%(class)ss",
    )

    class Meta:
        abstract = True
        ordering = ("user", "recipe")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_%(class)s"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.recipe}"


class FavoriteRecipe(UserRecipeRelation):
    """Model for favorite recipes"""

    class Meta(UserRecipeRelation.Meta):
        verbose_name = "избранный рецепт"
        verbose_name_plural = "избранные рецепты"


class ShoppingCart(UserRecipeRelation):
    """Model for shopping cart items"""

    class Meta(UserRecipeRelation.Meta):
        verbose_name = "рецепт в списке покупок"
        verbose_name_plural = "рецепты в списке покупок"
