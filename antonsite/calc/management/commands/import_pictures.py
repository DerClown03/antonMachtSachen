from typing import Any
from calc import models
from django.core.management.base import BaseCommand
from pathlib import Path
from os import listdir
from django.core.files import File

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        categorys_path = Path(__file__).parent.parent.parent / 'old_database/items'
        categorys = listdir(categorys_path)
        for category in categorys:
            item_image_path = Path(__file__).parent.parent.parent / f"old_database/items/{category}"
            items = listdir(item_image_path)
            for item in items:
                item = str(item).replace(".png", "")
                image = File(open(f"{item_image_path}/{item}.png", 'rb'), name=f"{item}.png")
                models.ItemModel.objects.create(category=category, item_name=item, item_img=image)
