from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_load_the_correct_recipes(self):
        needed_title = 'This is a Detail Page - Loads one Recipe'

        # Need a recipe for these tests
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:recipe', kwargs={
            'id': 1,
        }))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Tests if recipe detail is_published false don't show
        """
        # Need a recipe for these tests
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:recipe', kwargs={
            'id': recipe.id,
        }))

        self.assertEqual(response.status_code, 404)