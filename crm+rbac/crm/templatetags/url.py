from django import template

register = template.Library()
from django.urls import reverse
from django.http import QueryDict


@register.simple_tag()
def reverse_url(request, name, *args, **kwargs):
    """

    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """

    base_url = reverse(name, args=args, kwargs=kwargs)

    param = request.GET.urlencode()

    url = "{}?{}".format(base_url, param)

    return url


@register.simple_tag()
def reverse_url(request, name, *args, **kwargs):
    base_url = reverse(name, args=args, kwargs=kwargs)
    # param = request.GET.urlencode()
    q = QueryDict(mutable=True)
    next = request.get_full_path()
    q['next'] = next
    url = "{}?{}".format(base_url, q.urlencode())
    return url
