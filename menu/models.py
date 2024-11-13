from django.db import models
from restaurant.models import Restaurant


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menus'
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['restaurant']),
        ]

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"


class MainCategory(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='main_categories'
    )
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Main categories'

    def __str__(self):
        return f"{self.name} - {self.menu.name}"


class SubCategory(models.Model):
    main_category = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name='sub_categories'
    )
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='menus/subcategories/%Y/%m/%d/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Sub categories'

    def __str__(self):
        return f"{self.name} - {self.main_category.name}"
