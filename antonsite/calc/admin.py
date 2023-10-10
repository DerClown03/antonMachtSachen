from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.ItemModel)
admin.site.register(models.MachineModel)
admin.site.register(models.RecipeModel)
admin.site.register(models.InputModel)
admin.site.register(models.OutputModel)