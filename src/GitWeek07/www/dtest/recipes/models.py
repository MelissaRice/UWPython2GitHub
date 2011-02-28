from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=25)
    def __unicode__(self):
            return self.name    
    

class Ingredient(models.Model):
    UNIT_CHOICES = (
        ('C', 'Cups'),
        ('c', 'Cup'),
        ('B', 'Tbs'),
        ('S', 'tsp'),
        ('L', 'lbs'),    
        ('l', 'lb'), 
        ('O', 'oz'),   
        ('N', ' '),    
    )
    order   = models.PositiveSmallIntegerField()
    amount  = models.FloatField()
    units   = models.CharField(max_length=1, choices=UNIT_CHOICES)
    name    = models.CharField(max_length=30)
    remark  = models.CharField(max_length=80,blank=True)
    recipe  = models.ForeignKey('Recipe')
    def safeName(self):
        return self.name.replace(" ","_")
    def __unicode__(self):
            return self.name    

class Instruction(models.Model):
    order    = models.PositiveSmallIntegerField()
    summary  = models.CharField(max_length=25)
    detail   = models.CharField(max_length=500)
    recipe   = models.ForeignKey('Recipe')
    def __unicode__(self):
            return self.summary

class Recipe(models.Model):
    title    = models.CharField(max_length=80)
    source   = models.CharField(max_length=80)
    servings = models.PositiveSmallIntegerField()
    tags     = models.ManyToManyField(Tag)
    #prep_time = models.??timedelta??
    #total_time = models.??timedelta??
    def __unicode__(self):
            return self.title    



'''
Wed:   Basic recipe working with:
  
  Views:
           
          - title, source, number of servings, ingredients, instructions
         Ingredients table working with:
           - number, name, amount (initially as float), units (enum)
         Instructions working with:
           - number, summary, detail
         Unit tests
         See a list of all recipes
         Click on a recipe in list to see recipe detail


class Tag?s?(models.Model):
    name = models.CharField(max_length=80)
    ?? how to link to other objects (many-to-many example)

class MenuItem(models.Model):
    order = ??int??
    recipe title or text field??
    
class Menu?s?(models.Model):
    ?? ordered list of recipes ??
    
        

'''

