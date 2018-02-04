from django.core.urlresolvers import reverse
from django.db import models


class Unit(models.Model):
    name = models.CharField('Название', max_length=15)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название', max_length=50)
    color = models.PositiveIntegerField('Цвет')

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField('Название', max_length=50)
    value = models.SmallIntegerField('Приоритет')

    def __str__(self):
        return self.name


class Purchase(models.Model):
    name = models.CharField('Название', max_length=250, help_text='Название товара')
    amount = models.IntegerField('Количество', help_text='Количество товара', default=1)
    unit = models.ForeignKey(Unit, verbose_name='Ед. изм.', help_text='Единица измерения')
    category = models.ForeignKey(Category, verbose_name='Категория', help_text='Категория товара')
    priority = models.ForeignKey(Priority, verbose_name='Приоритет', help_text='Приориет покупки товара')
    status = models.BooleanField('Статус', help_text='Товар куплен?')

    def get_absolute_url(self):
        return reverse('purchase-list')
