from recipes.models import Tag, Instruction, Ingredient, Recipe
from django.contrib import admin

    
class IngredientsInline(admin.TabularInline):
    model = Ingredient
    fieldsets = [
        (None,               {'fields': ['order','amount','units','name','remark']}),
        ]
    extra = 3

class InstructionsInline(admin.TabularInline):
    model = Instruction
    extra = 3


class TagAdmin(admin.ModelAdmin):
    fields = ['name']

class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['source','servings']}),
        (None,               {'fields': ['tags']}),
        ]
    inlines = [IngredientsInline,InstructionsInline]
    list_filter = ['servings']
    
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
