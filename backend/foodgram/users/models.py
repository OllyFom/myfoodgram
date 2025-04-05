from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Foodgram user model"""

    email = models.EmailField("Электронная почта", unique=True, max_length=254)
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    avatar = models.ImageField(
        "Аватар", upload_to="avatars/", blank=True, null=True
    )
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=(r"^[\w.@+-]+$"),
                message=(
                    "Имя пользователя может содержать только буквы, "
                    "цифры и знаки @/./+/-/_"
                ),
                code="invalid_username",
            )
        ],
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Subscription(models.Model):
    """Foodgram subscription model"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authors",
        verbose_name="Автор",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name="Подписчик",
    )

    class Meta:
        ordering = ("user",)
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_subscription"
            )
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
