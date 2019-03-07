from django import template
from collections import OrderedDict

register = template.Library()

from django.conf import settings
import re


@register.filter
def add_sd(value, arg):
    return "{}-{}".format(value, arg)


@register.simple_tag
def join(*args, **kwargs):
    return "{}-{}".format('-'.join(args), '*'.join(kwargs.values()))


@register.inclusion_tag('menu.html')
def menu(request):
    url = request.path_info
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    print(menu_dict)
    order_list = sorted(menu_dict, key=lambda x: -menu_dict[x]['weight'])  # 按照权重进行排序 [2,1]
    # 创建一个有序字典
    menu_dict_order = OrderedDict()

    for key in order_list:

        i = menu_dict[key]  # 每个菜单的字典
        menu_dict_order[key] = i

        i['class'] = 'hide'
        for child in i['children']:
            # if re.match(child['url'], url):
            if child['name'] == getattr(request, settings.RBAC_CURRENT_PARENT_NAME, None):
                i['class'] = ''
                child['class'] = 'active'

    # for i in menu_list:
    #     if re.match(i['url'],url):
    #         i['class'] = 'active'
    return {'menu_list': menu_dict_order.values()}


@register.filter()
def has_permission(request, name):
    permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
    if name in permission_dict:
        return True


@register.inclusion_tag('breadcrumb.html')
def breadcrumb(request):
    breadcrumb_list = getattr(request, settings.RBAC_BREADCRUMB)
    return {"breadcrumb_list":breadcrumb_list}