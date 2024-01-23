from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views

class RecipeUrlsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_category_home_url_is_correct(self):
        home_url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(home_url, '/recipes/category/1/')

    def test_recipe_detail_home_url_is_correct(self):
        home_url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(home_url, '/recipes/1/')


class RecipeViewTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)