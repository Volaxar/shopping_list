from django.core.urlresolvers import reverse
from bs4 import BeautifulSoup
from shoplist.tests.fixtures import *


class TestUrlsRedirect:

    @pytest.mark.parametrize('url', ['', '/'])
    def test_global(self, django_app, url):
        response = django_app.get(url)

        assert response.status_code == 302
        assert response.location == reverse('purchase-list')

    @pytest.mark.parametrize('model_name', all_model_list)
    @pytest.mark.parametrize('url', ['', '/1', '/1/'])
    def test_list(self, django_app, model_name, url):
        response = django_app.get('/%s/list%s' % (model_name, url))

        assert response.status_code == 302
        assert response.location == reverse('%s-list' % model_name)

    @pytest.mark.parametrize('model_name', all_model_list)
    def test_detail_empty_not_xhr(self, django_app, model_name):
        response = django_app.get('/%s/' % model_name)

        assert response.status_code == 302
        assert response.location == reverse('%s-list' % model_name)

    @pytest.mark.parametrize('model_name', all_model_list)
    @pytest.mark.parametrize('url', ['', '/1', '/1/'])
    def test_detail_not_xhr(self, django_app, model_name, url):
        response = django_app.get('/%s/%s' % (model_name, url))

        assert response.status_code == 302
        assert response.location == reverse('%s-list' % model_name)

    @pytest.mark.parametrize('xhr', [False, True])
    def test_404(self, django_app, xhr):
        response = django_app.get('/abrakadabra/', xhr=xhr)

        assert response.status_code == 302
        assert response.location == reverse('purchase-list')


@pytest.mark.django_db
class TestUrlsOk:

    @pytest.mark.usefixtures('three_purchases')
    @pytest.mark.parametrize('model_name', all_model_list)
    @pytest.mark.parametrize('xhr', [False, True])
    def test_list(self, django_app, model_name, xhr):
        response = django_app.get(reverse('%s-list' % model_name), xhr=xhr)

        assert response.status_code == 200

    @pytest.mark.usefixtures('three_purchases')
    @pytest.mark.parametrize('model_name', all_model_list)
    def test_detail_empty_xhr(self, django_app, model_name):
        response = django_app.get('/%s/' % model_name, xhr=True)

        assert response.status_code == 200

    @pytest.mark.usefixtures('three_purchases')
    @pytest.mark.parametrize('model_name', all_model_list)
    def test_detail_xhr(self, django_app, model_name):
        model = getattr(models, model_name.capitalize())
        model_id = model.objects.first().id

        response = django_app.get('/%s/%s/' % (model_name, model_id), xhr=True)

        assert response.status_code == 200


@pytest.mark.django_db
class TestTemplatesList:

    @pytest.mark.usefixtures('three_purchases')
    def test_purchase_used(self, django_app):
        response = django_app.get(reverse('purchase-list'))

        used_templates = set([x.name for x in response.templates])

        for template in purchase_template_list | base_template_list:
            assert template in used_templates

    @pytest.mark.usefixtures('db_data')
    @pytest.mark.parametrize('model_name', dict_model_list)
    def test_dict_used(self, django_app, model_name):
        response = django_app.get(reverse('%s-list' % model_name))

        used_templates = set([x.name for x in response.templates])

        for template in dict_template_list | base_template_list:
            assert template in used_templates

    @pytest.mark.usefixtures('three_purchases')
    def test_purchase_used_xhr(self, django_app):
        response = django_app.get(reverse('purchase-list'), xhr=True)

        used_templates = set([x.name for x in response.templates])

        for template in xhr_purchase_template_list | xhr_base_template_list:
            assert template in used_templates

        for template in purchase_template_list - xhr_purchase_template_list:
            assert template not in used_templates

    @pytest.mark.usefixtures('db_data')
    @pytest.mark.parametrize('model_name', dict_model_list)
    def test_dict_used_xhr(self, django_app, model_name):
        response = django_app.get(reverse('%s-list' % model_name), xhr=True)

        used_templates = set([x.name for x in response.templates])

        for template in xhr_dict_template_list | xhr_base_template_list:
            assert template in used_templates

        for template in dict_template_list - xhr_dict_template_list:
            assert template not in used_templates


@pytest.mark.django_db
class TestList:

    @pytest.mark.parametrize('model_name', dict_model_list)
    def test_context_dict(self, django_app, model_name):
        response = django_app.get(reverse('%s-list' % model_name))
        context = response.context

        assert 'fields' in context
        assert 'model_name' in context
        assert 'model_verbose_name' in context

        assert context['fields'] == ['name']
        assert context['model_name'] == model_name
        assert context['model_verbose_name'] == get_model(model_name)._meta.verbose_name_plural

    def test_context_purchase(self, django_app):
        response = django_app.get(reverse('purchase-list'))
        context = response.context

        assert 'filter' in context
        assert 'order_by' in context
        assert 'order_direction' in context

    def test_filter_value(self, django_app):
        url = reverse('purchase-list')

        response = django_app.get(url)
        assert response.context['filter'] == '', 'Значение фильтра по умолчанию'

        response = django_app.get(url, params={'filter': 'test'})
        assert response.context['filter'] == 'test', 'Значение фильтра из GET запроса'

        response = django_app.get(url)
        assert response.context['filter'] == 'test', 'Значение фильтра из сессии'

    @pytest.mark.usefixtures('three_purchases')
    def test_filter_queryset(self, django_app):
        url = reverse('purchase-list')

        soup = django_app.get(url).html
        lines = soup.findAll('tr', 'dict-line')
        assert len(lines) == 3

        soup = django_app.get(url, params={'filter': '2'}).html
        lines = soup.findAll('tr', 'dict-line')
        assert len(lines) == 1
        assert lines[0].td.text == 'Тест_2'

    def test_order_value(self, django_app):
        url = reverse('purchase-list')

        response = django_app.get(url)
        assert response.context['order_by'] == 'name', 'Значение сортировки по умолчанию'
        assert response.context['order_direction'] == '', 'Направление сортировки по умолчанию'

        response = django_app.get(url, params={'order_by': 'name'})
        assert response.context['order_by'] == 'name', 'Значение сортировки после смены направления сортировки'
        assert response.context['order_direction'] == '-', 'Направление сортировки после смены направления сортировки'

        response = django_app.get(url, params={'order_by': 'amount'})
        assert response.context['order_by'] == 'amount', 'Значение сортировки после смены поля сортировки'
        assert response.context['order_direction'] == '', 'Направление сортировки после смены поля сортировки'

        response = django_app.get(url, params={'order_by': 'amount'})
        assert response.context['order_by'] == 'amount', 'Значение сортировки после смены направления сортировки'
        assert response.context['order_direction'] == '-', 'Направление сортировки после смены направления сортировки'

        response = django_app.get(url)
        assert response.context['order_by'] == 'amount', 'Значение сортировки из сессии'
        assert response.context['order_direction'] == '-', 'Направление сортировки из сессии'

    @pytest.mark.usefixtures('three_purchases')
    def test_order_queryset(self, django_app):
        url = reverse('purchase-list')

        soup = django_app.get(url).html
        lines = soup.findAll('tr', 'dict-line')
        assert lines[0].td.text == 'Тест_1' and lines[2].td.text == 'Тест_3'

        soup = django_app.get(url, params={'order_by': 'name'}).html
        lines = soup.findAll('tr', 'dict-line')
        assert lines[0].td.text == 'Тест_3' and lines[2].td.text == 'Тест_1'

        soup = django_app.get(url, params={'order_by': 'amount'}).html
        lines = soup.findAll('tr', 'dict-line')
        assert lines[0].td.text == 'Тест_2' and lines[2].td.text == 'Тест_1'

        soup = django_app.get(url, params={'order_by': 'amount'}).html
        lines = soup.findAll('tr', 'dict-line')
        assert lines[0].td.text == 'Тест_1' and lines[2].td.text == 'Тест_2'


@pytest.mark.django_db
class TestDetail:

    @pytest.mark.usefixtures('three_purchases')
    @pytest.mark.parametrize('model_name', all_model_list)
    def test_get_empty(self, django_app, model_name):
        soup = django_app.get('/%s/' % model_name, xhr=True).html

        line = soup.find('tr', 'dict-new-line')
        assert line

        id_id = line.find('input', id='id_id')
        assert not id_id

    @pytest.mark.usefixtures('three_purchases')
    @pytest.mark.parametrize('model_name', all_model_list)
    def test_get_filled(self, django_app, model_name):
        pk = get_model(model_name).objects.first().id
        soup = django_app.get('/%s/%s/' % (model_name, pk), xhr=True).html

        line = soup.find('tr', 'dict-new-line')
        assert line

        id_id = line.find('input', id='id_id')
        assert id_id['value'] == str(pk)

    def test_post_create_valid_purchase(self, django_app_factory, new_purchase):
        app = django_app_factory(csrf_checks=False, extra_environ={})

        soup = app.get('/purchase/list/').html
        field = soup.find('td', text='Тест')
        assert not field

        response = app.post('/purchase/', params={
            'name': new_purchase.name,
            'amount': new_purchase.amount,
            'unit': new_purchase.unit_id,
            'category': new_purchase.category_id,
            'priority': new_purchase.priority_id
        }, xhr=True)

        assert response.status_code == 302
        assert response.location == '/purchase/list/'

        soup = app.get(response.location).html
        field = soup.find('td', text='Тест')
        assert field

    @pytest.mark.parametrize('model_name', dict_model_list)
    def test_post_create_valid_dict(self, django_app_factory, model_name):
        app = django_app_factory(csrf_checks=False, extra_environ={})

        soup = app.get('/%s/list/' % model_name).html
        field = soup.find('td', text='Тест')
        assert not field

        response = app.post('/%s/' % model_name, params={'name': 'Тест'}, xhr=True)
        assert response.status_code == 302
        assert response.location == '/%s/list/' % model_name

        soup = app.get(response.location).html
        field = soup.find('td', text='Тест')
        assert field

    @pytest.mark.parametrize('model_name', all_model_list)
    def test_post_create_invalid(self, django_app_factory, model_name):
        app = django_app_factory(csrf_checks=False, extra_environ={})

        response = app.post('/%s/' % model_name, xhr=True)

        assert response.status_code == 200
        assert getattr(response, 'json', '') and 'response' in response.json

    @pytest.mark.usefixtures('three_purchases')
    def test_post_update_valid_purchase(self, django_app_factory):
        app = django_app_factory(csrf_checks=False, extra_environ={})

        soup = app.get('/purchase/list/').html
        field = soup.find('td', text='Тест')
        assert not field

        purchase = Purchase.objects.first()

        response = app.post('/purchase/%s/' % purchase.id, params={
            'id': purchase.id,
            'name': 'Тест',
            'amount': purchase.amount,
            'unit': purchase.unit_id,
            'category': purchase.category_id,
            'priority': purchase.priority_id
        }, xhr=True)

        assert response.status_code == 302
        assert response.location == '/purchase/list/'

        soup = app.get(response.location).html
        line = soup.find('td', text='Тест').parent
        line_id = line['data-pid']

        assert str(purchase.id) == line_id

    @pytest.mark.usefixtures('db_data')
    @pytest.mark.parametrize('model_name', dict_model_list)
    def test_post_update_valid_dict(self, django_app_factory, model_name):
        app = django_app_factory(csrf_checks=False, extra_environ={})

        soup = app.get('/%s/list/' % model_name).html
        field = soup.find('td', text='Тест')
        assert not field

        model_instance = get_model(model_name).objects.first()

        response = app.post('/%s/%s/' % (model_name, model_instance.id), params={
            'id': model_instance.id,
            'name': 'Тест'
        }, xhr=True)

        assert response.status_code == 302
        assert response.location == '/%s/list/' % model_name

        soup = app.get(response.location).html
        line = soup.find('td', text='Тест').parent
        line_id = line['data-pid']

        assert str(model_instance.id) == line_id

    @pytest.mark.usefixtures('three_purchases')
    @pytest.mark.parametrize('model_name', all_model_list)
    def test_post_update_invalid(self, django_app_factory, model_name):
        app = django_app_factory(csrf_checks=False, extra_environ={})

        model_instance = get_model(model_name).objects.first()

        response = app.post('/%s/%s/' % (model_name, model_instance.id), params={
            'id': model_instance.id
        }, xhr=True)

        assert response.status_code == 200
        assert getattr(response, 'json', '') and 'response' in response.json

    @pytest.mark.usefixtures('three_purchases')
    @pytest.mark.parametrize('model_name', all_model_list)
    def test_delete(self, django_app_factory, model_name):
        app = django_app_factory(csrf_checks=False, extra_environ={})

        model_instance = get_model(model_name).objects.first()

        soup = app.get('/%s/list/' % model_name).html
        line = soup.find('tr', attrs={'data-pid': model_instance.id})
        assert line

        response = app.delete('/%s/%s/' % (model_name, model_instance.id))
        assert response.status_code == 302
        assert response.location == '/%s/list/' % model_name

        soup = app.get(response.location).html
        line = soup.find('tr', attrs={'data-pid': model_instance.id})
        assert not line

    @pytest.mark.usefixtures('three_purchases')
    def test_patch(self, django_app_factory):
        app = django_app_factory(csrf_checks=False, extra_environ={})

        purchase = Purchase.objects.first()
        status = purchase.status

        response = app.patch('/purchase/%s/' % purchase.id)
        assert response.status_code == 302
        assert response.location == '/purchase/list/'

        purchase = Purchase.objects.get(id=purchase.id)

        assert status != purchase.status


@pytest.mark.django_db
class TestForm:

    @pytest.mark.parametrize('model_name', all_model_list)
    def test_class_control(self, django_app, model_name):
        soup = django_app.get('/%s/' % model_name, xhr=True).html

        td_list = soup.findAll('td')
        name_field_list = [x['class'][0][3:] for x in td_list if 'fn-' in x['class'][0]]

        for name_field in name_field_list:
            tag = soup.find(id='id_%s' % name_field)
            assert 'form-control' in tag['class']

    @pytest.mark.parametrize('model_name', all_model_list)
    def test_class_error(self, django_app_factory, model_name):
        app = django_app_factory(csrf_checks=False, extra_environ={})

        response = app.post('/%s/' % model_name, xhr=True)
        soup = BeautifulSoup(response.json['response'], "html.parser")
        error_field = soup.find(id='id_name')

        assert 'error-field' in error_field['class']
