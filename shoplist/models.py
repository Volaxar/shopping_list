from django.db import models
from django.core.urlresolvers import reverse


class Unit(models.Model):
    name = models.CharField(max_length=15)


class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.PositiveIntegerField()


class Priority(models.Model):
    name = models.CharField(max_length=50)
    value = models.SmallIntegerField()


class Purchase(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    amount = models.IntegerField()
    unit = models.ForeignKey(Unit)
    category = models.ForeignKey(Category)
    priority = models.ForeignKey(Priority)
    purchased = models.BooleanField()

    def get_absolute_url(self):
        return reverse('purchase-list')
