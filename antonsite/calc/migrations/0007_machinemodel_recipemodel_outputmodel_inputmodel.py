# Generated by Django 4.2.5 on 2023-09-21 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0006_remove_outputmodel_recipe_remove_recipemodel_machine_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_img', models.ImageField(upload_to='static/images/')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_amount', models.IntegerField()),
                ('output_amount', models.IntegerField()),
                ('normal_recipe', models.BooleanField()),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='calc.machinemodel')),
            ],
        ),
        migrations.CreateModel(
            name='OutputModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=10, max_digits=20)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_output_items', to='calc.recipemodel')),
            ],
        ),
        migrations.CreateModel(
            name='InputModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=10, max_digits=20)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_input_items', to='calc.recipemodel')),
            ],
        ),
    ]