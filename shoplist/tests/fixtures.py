import pytest
from django.core.management import call_command

import shoplist.models as models
from shoplist.models import Purchase, Unit, Category, Priority

dict_model_list = ['unit', 'category', 'priority']
all_model_list = ['purchase'] + dict_model_list

base_template_list = {
    'shoplist/base.html',
    'shoplist/base_list.html',
    'shoplist/base_table_list.html',
    'shoplist/_btn_menu.html'
}

purchase_template_list = {
    'shoplist/purchase_list.html',
    'shoplist/_purchase_header.html',
}

dict_template_list = {
    'shoplist/dict_list.html',
    'shoplist/_dict_header.html',
}

xhr_base_template_list = {
    'shoplist/_btn_menu.html',
    'shoplist/base_table_list.html'
}

xhr_purchase_template_list = {
    'shoplist/_purchase_header.html',
}

xhr_dict_template_list = {
    'shoplist/_dict_header.html',
}


@pytest.fixture(name='db_data')
def fixture_db_data(django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'shoplist_data.json')


@pytest.fixture(name='new_purchase')
def fixture_new_purchase(db_data):
    yield Purchase(
        name='Тест',
        amount=10,
        unit=Unit.objects.first(),
        category=Category.objects.first(),
        priority=Priority.objects.first(),
        status=False
    )


@pytest.fixture(name='three_purchases')
def fixture_three_purchases(db_data):
    amounts = [3, 1, 2]
    for x in range(1, 4):
        Purchase(
            name='Тест_%s' % x,
            amount=amounts[x - 1],
            unit=Unit.objects.first(),
            category=Category.objects.first(),
            priority=Priority.objects.first(),
            status=False
        ).save()

    yield


def get_model(model_name):
    return getattr(models, model_name.capitalize())
