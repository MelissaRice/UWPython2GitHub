'''
Created on Feb 23, 2011

@author: mlr
'''

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from recipes.models import Instruction, Ingredient, Recipe
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    return render_to_response('index.html')

