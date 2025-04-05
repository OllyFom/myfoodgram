from django.shortcuts import redirect, get_object_or_404

from .models import Recipe


def redirect_short_link(request, recipe_id):
    """Redirects to the recipe"""
    get_object_or_404(Recipe, id=recipe_id)
    return redirect(f"/api/recipes/{recipe_id}/")
