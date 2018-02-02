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
def is_flag_on(flag, value, default=''):
    return value if flag else default
