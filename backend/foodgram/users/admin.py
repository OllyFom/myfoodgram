from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import User, Subscription


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
