from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import Min, Max
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Subscription,
    Ingredient,
    Recipe,
    RecipeIngredient,
    FavoriteRecipe,
    ShoppingCart,
)


class HasRecipesFilter(admin.SimpleListFilter):
    title = "наличие рецептов"
    parameter_name = "has_recipes"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Есть рецепты"),
            ("no", "Нет рецептов"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(recipes__isnull=False).distinct()
        if self.value() == "no":
            return queryset.filter(recipes__isnull=True)


class HasFollowersFilter(admin.SimpleListFilter):
    title = "наличие подписчиков"
    parameter_name = "has_followers"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Есть подписчики"),
            ("no", "Нет подписчиков"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(authors__isnull=False).distinct()
        if self.value() == "no":
            return queryset.filter(authors__isnull=True)


class HasSubscriptionsFilter(admin.SimpleListFilter):
    title = "наличие подписок"
    parameter_name = "has_subscriptions"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Есть подписки"),
            ("no", "Нет подписок"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(followers__isnull=False).distinct()
        if self.value() == "no":
            return queryset.filter(followers__isnull=True)


@admin.register(User)
class SiteUserAdmin(UserAdmin):
    """Custom user admin class"""

    list_display = (
        "id",
        "username",
        "get_full_name",
        "email",
        "get_avatar",
        "get_recipes_count",
        "get_number_of_following",
        "get_number_of_followers",
    )
    list_filter = (
        HasRecipesFilter,
        HasFollowersFilter,
        HasSubscriptionsFilter,
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("id",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {"fields": ("username", "first_name", "last_name", "avatar")},
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    @admin.display(description="ФИО")
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(description="Аватар")
    @mark_safe
    def get_avatar(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="50" height="50" />'
        return ""

    @admin.display(description="Рецепты")
    def get_recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description="подписчики")
    def get_number_of_followers(self, user_obj):
        return user_obj.authors.count()

    @admin.display(description="подписки")
    def get_number_of_following(self, user_obj):
        return user_obj.followers.count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Subscription admin class"""

    list_display = ("id", "author", "user")
    list_filter = ("author", "user")
    search_fields = ("author__username", "user__username")


class CookingTimeFilter(admin.SimpleListFilter):
    """Filter recipes by cooking time with dynamic thresholds"""

    title = "время приготовления"
    parameter_name = "cooking_time"

    def lookups(self, request, model_admin):
        stats = Recipe.objects.aggregate(
            min_time=Min("cooking_time"), max_time=Max("cooking_time")
        )

        if not stats["min_time"] or not stats["max_time"]:
            return []

        time_range = stats["max_time"] - stats["min_time"]
        threshold1 = stats["min_time"] + time_range // 3
        threshold2 = stats["min_time"] + (2 * time_range) // 3

        quick_count = Recipe.objects.filter(
            cooking_time__lte=threshold1
        ).count()
        medium_count = Recipe.objects.filter(
            cooking_time__gt=threshold1, cooking_time__lte=threshold2
        ).count()
        long_count = Recipe.objects.filter(cooking_time__gt=threshold2).count()

        return [
            ("quick", f"быстрее {threshold1} мин ({quick_count})"),
            ("medium", f"быстрее {threshold2} мин ({medium_count})"),
            ("long", f"дольше {threshold2} мин ({long_count})"),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        stats = Recipe.objects.aggregate(
            min_time=Min("cooking_time"), max_time=Max("cooking_time")
        )

        if not stats["min_time"] or not stats["max_time"]:
            return queryset

        time_range = stats["max_time"] - stats["min_time"]
        threshold1 = stats["min_time"] + time_range // 3
        threshold2 = stats["min_time"] + (2 * time_range) // 3

        if self.value() == "quick":
            return queryset.filter(cooking_time__lte=threshold1)
        if self.value() == "medium":
            return queryset.filter(
                cooking_time__gt=threshold1, cooking_time__lte=threshold2
            )
        if self.value() == "long":
            return queryset.filter(cooking_time__gt=threshold2)
        return queryset


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe admin model"""

    list_display = (
        "id",
        "name",
        "cooking_time",
        "author",
        "get_favorites_count",
        "get_ingredients",
        "get_image",
    )
    search_fields = (
        "name",
        "author__username",
        "author__first_name",
        "author__last_name",
    )
    # list_filter = ("name", "author")
    list_filter = (CookingTimeFilter,)
    inlines = (RecipeIngredientInline,)

    @admin.display(description="в избранном")
    def get_favorites_count(self, obj):
        return obj.favoriterecipes.count()

    @admin.display(description="ингредиенты")
    @mark_safe
    def get_ingredients(self, obj):
        ingredients = obj.recipe_ingredients.all()
        ingredients_list = [
            f"{item.ingredient.name} - "
            f"{item.amount} "
            f"{item.ingredient.measurement_unit}"
            for item in ingredients
        ]
        return "<br>".join(ingredients_list)

    @admin.display(description="изображение")
    @mark_safe
    def get_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100">'
        return "Нет изображения"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ingredient admin model"""

    list_display = ("name", "measurement_unit", "get_recipes_count")
    search_fields = ("name", "measurement_unit")
    list_filter = ("measurement_unit",)

    @admin.display(description="рецептов")
    def get_recipes_count(self, obj):
        return obj.recipes.count()


@admin.register(FavoriteRecipe, ShoppingCart)
class UserRecipeRelationAdmin(admin.ModelAdmin):
    """Admin model for user-recipe relations"""

    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")
    list_filter = ("user", "recipe")
