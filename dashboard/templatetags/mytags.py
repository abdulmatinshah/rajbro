import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch, resolve

register = template.Library()


# @register.simple_tag(takes_context=True)
# def active(context, pattern_or_urlname):
#     try:
#         pattern = '^' + reverse(pattern_or_urlname)
#     except NoReverseMatch:
#         pattern = pattern_or_urlname
#     path = context['request'].path
#     if re.search(pattern, path):
#         return 'active'
#     return ''

@register.simple_tag
def nav_active(request, url):
    """
    In template: {% nav_active request "url_name_here" %}
    """
    url_name = resolve(request.path).url_name
    if url_name == url:
        return "active"
    return ""

@register.simple_tag
def namespace_active(request, url):
    """
    In template: {% nav_active request "url_name_here" %}
    """
    namespace_name = resolve(request.path).namespace

    if namespace_name == url:
        return "active"
    return ""

@register.simple_tag
def dropdown_active(request, url):
    """
    In template: {% nav_active request "url_name_here" %}
    """
    retreived_path = (request.path).split('/')[1:3]
    formated_path = ':'.join(retreived_path)
    if formated_path == url:
        return "active"
    return ""
# nav_active() will check the web request url_name and compare it
# to the named url group within urls.py,
# setting the active class if they match.

# @register.filter()
# def to_boxes(value):
#
#     print(value.)
#     return value + 2000