"""
File: recipesite/recipes/tests.py 
Purpose: unit test....
Last revised: 23 Feb 2011 
"""

from django.test import TestCase
from recipes.models import Instruction, Ingredient, Recipe


class RecipeTest(TestCase):
    
    def setUp(self):
        """
        Set up for testing the recipe models.
        """
        # set up recipe 1
        self.recipe = Recipe.objects.create(title='Mint Iced Tea',source='Big Book of Iced Tea Ideas',servings=8)
        self.recipe.ingredient_set.create(order=5,amount=8,units='N',name='mint sprigs')
        self.recipe.ingredient_set.create(order=3,amount=4,units='T',name='sugar (more to taste)')
        self.recipe.ingredient_set.create(order=1,amount=8,units='N',name='tea bags')
        self.recipe.ingredient_set.create(order=4,amount=3,units='C',name='crushed ice')
        self.recipe.ingredient_set.create(order=2,amount=5,units='C',name='boiling water')
        self.recipe.instruction_set.create(order=2,summary='Sweeten',detail='Add the sugar and sweeten to taste.')
        self.recipe.instruction_set.create(order=4,summary='Garnish and Serve',detail='Pour the tea into tall glasses, garnish each with a mint sprig, and serve.')
        self.recipe.instruction_set.create(order=3,summary='Cool',detail='Allow the tea to cool for 15 minutes, then add the ice.')
        self.recipe.instruction_set.create(order=1,summary='Brew Tea',detail='Brew the tea bags in the boiling water for 3 minutes, then discard tea bags.')
        
    def testRecipe(self):
        self.assertEqual(self.recipe.title,'Mint Iced Tea')    
        self.assertEqual(self.recipe.source,'Big Book of Iced Tea Ideas')    
        self.assertEqual(self.recipe.servings,8)    
        self.assertEqual(self.recipe.ingredient_set.all().count(), 5)    
        #self.assertEqual(self.recipe.ingredient??number1.name,'tea bags')    
        self.assertEqual(self.recipe.instruction_set.all().count(), 4)
        #self.assertEqual(self.recipe.instruction??number1.summary,'Brew Tea')


