from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag(takes_context=True)
def get_sort(context, order_by):
    if context['order_by'] == order_by:
        return mark_safe('&uarr;') if context.get('order_direction', '-') else mark_safe('&darr;')
    else:
        return ''


@register.simple_tag
def get_field_name(model, field):
    return model._meta.get_field(field).verbose_name


@register.simple_tag
def get_form_field_name(form, field):
    return get_field_name(form._meta.model, field)


@register.simple_tag
def get_field(obj, field_name):
    return obj.__getattribute__(field_name)
