from calc import models
from django.core.management.base import BaseCommand
from django.core.files import File
from pathlib import Path
from PIL import Image


machines = ["assambler", "blender", "constructor", "foundry", "manufacturer", "packager", "particle_accelerator", "refinery", "smelter"]

class Command(BaseCommand):
    def is_normal_recipe(self, indicator: str):
        if indicator == "a":
            return False
        return True


    def make_string_readable(item_name: str):
        return item_name.replace('_', ' ').title()


    def handle(self, *args, **kwargs):
        recipe_path = Path(__file__).parent.parent.parent / 'recipes'
        image_path = Path(__file__).parent.parent.parent / 'old_database/machines'
        for machine in machines:
            image = File(open(f"{image_path}/{machine}.png", 'rb'), name=f"{machine}.png")
            machine_model = models.MachineModel.objects.create(machine_name=machine, machine_img=image)
            machine_file = recipe_path / f'{machine}.txt'
            with open(machine_file) as f:
                lines = f.readlines()

                for line in lines:
                    spliters = line.split(", ")
                    input_count = int(spliters[0])
                    output_count = int(spliters[1])
                    normal_recipe = self.is_normal_recipe(spliters[-1][0])
                    recipe_model = models.RecipeModel.objects.create(machine=machine_model, input_amount=input_count, output_amount=output_count, normal_recipe=normal_recipe)

                    for i in range(0, input_count * 2, 2):
                        item = spliters[i + 3]
                        item_readable = self.make_string_readable(spliters[i + 3])
                        amount = spliters[i + 4]
                        input_model = models.InputModel.objects.create(recipe=recipe_model, item_name=item, amount=amount, item_name_readable=item_readable)

                    for i in range(0, output_count * 2, 2):
                        item = spliters[i + (2 * input_count) + 4]
                        item_readable = self.make_string_readable(spliters[i + (2 * input_count) + 4])
                        amount = spliters[i + (2 * input_count) + 5]
                        output_model = models.OutputModel.objects.create(recipe=recipe_model, item_name=item, amount=amount, item_name_readable=item_readable)
 