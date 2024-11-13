# Generated by Django 5.1.2 on 2024-11-13 10:45

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("is_allergen", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Dish",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                ("photo", models.ImageField(upload_to="menus/dishes/%Y/%m/%d/")),
                ("is_available", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "sub_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dishes",
                        to="menu.subcategory",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Dishes",
                "ordering": ["order", "name"],
            },
        ),
        migrations.CreateModel(
            name="DishIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_optional", models.BooleanField(default=False)),
                (
                    "dish",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dish_ingredients",
                        to="meal.dish",
                    ),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="dish_ingredients",
                        to="meal.ingredient",
                    ),
                ),
            ],
            options={
                "unique_together": {("dish", "ingredient")},
            },
        ),
        migrations.AddField(
            model_name="dish",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="dishes",
                through="meal.DishIngredient",
                to="meal.ingredient",
            ),
        ),
    ]
