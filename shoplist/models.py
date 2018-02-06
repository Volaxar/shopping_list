from django.core.urlresolvers import reverse
from django.db import models


class DictModel(models.Model):

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name

    @classmethod
    def get_verbose_name_plural(cls):
        return cls._meta.verbose_name_plural

    def __str__(self):
        return self.__getattribute__('name')

    class Meta:
        abstract = True


class Unit(DictModel):
    name = models.CharField('Название', max_length=15)

    class Meta(DictModel.Meta):
        verbose_name = 'Ед. измерения'
        verbose_name_plural = 'Ед. измерения'

    @staticmethod
    def get_absolute_url():
        return reverse('unit-list')


class Category(DictModel):
    name = models.CharField('Название', max_length=50)

    class Meta(DictModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    @staticmethod
    def get_absolute_url():
        return reverse('category-list')


class Priority(DictModel):
    name = models.CharField('Название', max_length=50)

    class Meta(DictModel.Meta):
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритет'

    @staticmethod
    def get_absolute_url():
        return reverse('priority-list')


class Purchase(DictModel):
    name = models.CharField('Название', max_length=250, help_text='Название товара', unique=True)
    amount = models.IntegerField('Количество', help_text='Количество товара', default=1)
    unit = models.ForeignKey(Unit, verbose_name='Ед. изм.', help_text='Единица измерения')
    category = models.ForeignKey(Category, verbose_name='Категория', help_text='Категория товара')
    priority = models.ForeignKey(Priority, verbose_name='Приоритет', help_text='Приориет покупки товара')
    status = models.BooleanField('Статус', help_text='Товар куплен?', default=False)

    class Meta(DictModel.Meta):
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    @staticmethod
    def get_absolute_url():
        return reverse('purchase-list')
