from typing import Any
from django.db import models

# Create your models here.
class ItemModel(models.Model):
    item_name = models.CharField(max_length=50)
    item_img = models.ImageField(upload_to="static/images/items")


class MachineModel(models.Model):
    machine_img = models.ImageField(upload_to="static/images/machines")
    machine_name = models.CharField(max_length=50)
    machine_name_readable = models.CharField(max_length=50)

class RecipeModel(models.Model):
    machine = models.ForeignKey(MachineModel, on_delete=models.CASCADE, related_name="recipes")
    input_amount = models.IntegerField()
    output_amount = models.IntegerField()
    normal_recipe = models.BooleanField()


class InputModel(models.Model):
    recipe = models.ForeignKey(RecipeModel, on_delete=models.CASCADE, related_name="recipe_input_items")
    item_name = models.CharField(max_length=50)
    item_name_readable = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=10, max_digits=20)


class OutputModel(models.Model):
    recipe = models.ForeignKey(RecipeModel, on_delete=models.CASCADE, related_name="recipe_output_items")
    item_name = models.CharField(max_length=50)
    item_name_readable = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=10, max_digits=20)