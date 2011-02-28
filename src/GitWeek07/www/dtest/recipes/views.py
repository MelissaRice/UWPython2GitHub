from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from recipes.models import Instruction, Ingredient, Recipe, Tag
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings


def index(request):
    recipeList = Recipe.objects.all().order_by('title')[:]
    tagList = Tag.objects.all().order_by('name')[:]
    return render_to_response('recipes/index2.html', {'recipeList':recipeList,'tagList':tagList})

def detail(request, recipe_id):
    r = get_object_or_404(Recipe, pk=recipe_id)
    return render_to_response('recipes/detail3.html', {'recipe':r,'MEDIA_ROOT':settings.MEDIA_ROOT}, 
                               context_instance=RequestContext(request))

def ingredient(request, ingredient_name):
    ingredient_name = ingredient_name.replace("_"," ")
    recipes = Recipe.objects.filter(ingredient__name__contains=ingredient_name)
    return render_to_response('recipes/ingredient2.html', {'recipes':recipes,'ingredientName':ingredient_name}, context_instance=RequestContext(request))

def tagged(request, tag_name):
    recipes = Recipe.objects.filter(tags__name__contains=tag_name)
    return render_to_response('recipes/tagged2.html', {'recipes':recipes,'tagName':tag_name}, context_instance=RequestContext(request))

def tags(request):
    tagList = Tag.objects.all().order_by('name')[:]
    return render_to_response('recipes/tags.html', {'tagList':tagList})


