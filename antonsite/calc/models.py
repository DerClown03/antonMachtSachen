from typing import Any
from django.db import models

# Create your models here.
class ItemModel(models.Model):
    category = models.CharField(max_length=50)
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
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE, related_name="item_input_items")
    item_name = models.CharField(max_length=50)
    item_name_readable = models.CharField(max_length=50)
    amount = models.FloatField(max_length=20)


class OutputModel(models.Model):
    recipe = models.ForeignKey(RecipeModel, on_delete=models.CASCADE, related_name="recipe_output_items")
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE, related_name="item_output_items")
    item_name = models.CharField(max_length=50)
    item_name_readable = models.CharField(max_length=50)
    amount = models.FloatField(max_length=20)