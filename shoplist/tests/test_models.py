from shoplist.tests.fixtures import *
from django.core.urlresolvers import reverse


class TestModels:

    @pytest.mark.parametrize(
        'model, model_name',
        [
            (Purchase, 'purchase'),
            (Unit, 'unit'),
            (Category, 'category'),
            (Priority, 'priority')
        ]
    )
    def test_get_model_name(self, model, model_name):
        assert model.get_model_name() == model_name

    @pytest.mark.parametrize(
        'model, model_verbose_name_plural',
        [
            (Purchase, 'Покупки'),
            (Unit, 'Ед. измерения'),
            (Category, 'Категории'),
            (Priority, 'Приоритеты')
        ]
    )
    def test_get_verbose_name_plural(self, model, model_verbose_name_plural):
        assert model.get_verbose_name_plural() == model_verbose_name_plural

    @pytest.mark.parametrize(
        'model, url_name',
        [
            (Purchase, 'purchase-list'),
            (Unit, 'unit-list'),
            (Category, 'category-list'),
            (Priority, 'priority-list')
        ]
    )
    def test_get_absolute_url(self, model, url_name):
        assert model.get_absolute_url() == reverse(url_name)

    @pytest.mark.django_db
    def test_change_status(self, new_purchase):
        purchase = new_purchase
        assert purchase.status is False

        purchase.change_status()
        assert purchase.status is True

        purchase.change_status()
        assert purchase.status is False

    @pytest.mark.django_db
    def test_instance_name(self, new_purchase):
        purchase = new_purchase

        assert str(purchase) == 'Тест'
