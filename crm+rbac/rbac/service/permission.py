from django.conf import settings


def init_permisson(request, obj):
    """
    权限信息的初识化
    :param request:
    :param obj:
    :return:
    """
    # 查询权限信息： isnull=False  跨表  去重
    permission_list = obj.roles.all().filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__title',
        'permissions__name',
        'permissions__parent__name',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon',
        'permissions__menu__weight',
    ).distinct()

    # 构建数据结构
    # 权限的字典
    permission_dict = {}
    # 菜单的列表
    menu_list = []
    for i in permission_list:
        if i['permissions__menu_id']:
            menu_list.append({
                'url': i['permissions__url'],
                'title': i['permissions__title'],
                'name': i['permissions__name'],
                'menu_id': i['permissions__menu_id'],
                'menu_title': i['permissions__menu__title'],
                'menu_icon': i['permissions__menu__icon'],
                'menu_weight': i['permissions__menu__weight']
            })
        permission_dict[i['permissions__name']] = {'url': i['permissions__url'],
                                                   'parent_name': i['permissions__parent__name'],
                                                   'title': i['permissions__title'],
                                                   }

    menu_dict = {}

    for i in menu_list:
        menu_id = i.get('menu_id')
        if menu_id not in menu_dict:
            menu_dict[menu_id] = {
                'title': i['menu_title'],
                'icon': i['menu_icon'],
                'weight': i['menu_weight'],
                'children': [{'title': i['title'], 'url': i['url'], 'name': i['name']}]
            }
        else:
            menu_dict[menu_id]['children'].append({'title': i['title'], 'url': i['url'], 'name': i['name']})

    # 存入session
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
