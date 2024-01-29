from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        #Check if apear the template 'no recipes'
        self.assertIn(
            '<h1>No recipes found at this time</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_load_recipes(self):
        # Need a recipe for these tests
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Tests if recipe is_published false don't show
        """
        # Need a recipe for these tests
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        # Check if one recipe exists
        self.assertIn(
            '<h1>No recipes found at this time</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse(
            'recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_load_recipes(self):
        needed_title = 'This is a Category Test'

        # Need a recipe for these tests
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Tests if recipe category is_published false don't show
        """
        # Need a recipe for these tests
        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': 1})
        )

        self.assertEqual(response.status_code, 404)

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