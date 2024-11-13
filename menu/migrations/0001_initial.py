# Generated by Django 5.1.2 on 2024-11-13 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("restaurant", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Menu",
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
                ("is_active", models.BooleanField(default=True)),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menus",
                        to="restaurant.restaurant",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MainCategory",
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
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="main_categories",
                        to="menu.menu",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Main categories",
                "ordering": ["order", "name"],
            },
        ),
        migrations.CreateModel(
            name="SubCategory",
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
                ("photo", models.ImageField(upload_to="menus/subcategories/%Y/%m/%d/")),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "main_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_categories",
                        to="menu.maincategory",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Sub categories",
                "ordering": ["order", "name"],
            },
        ),
        migrations.AddIndex(
            model_name="menu",
            index=models.Index(
                fields=["restaurant"], name="menu_menu_restaur_5a7356_idx"
            ),
        ),
    ]
