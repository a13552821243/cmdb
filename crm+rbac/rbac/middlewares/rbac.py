from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import re
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url = request.path_info
        # 白名单校验
        # valid_list = [
        #     '/crm/login/',
        #     '/admin.*',
        # ]
        for i in settings.RBAC_VALID_LIST:
            if re.match(i, url):
                return
        # 权限的校验
        # 获取当前用户的权限信息
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return HttpResponse('没有权限信息，请登录')

        # 记录路径导航的信息
        breadcrumb_list = [{'url': '/crm/index/', 'title': '首页'}]

        # 进行权限信息的校验
        for name, v in permission_dict.items():
            reg_url = "{}$".format(v['url'])
            if re.match(reg_url, url):
                p_name = v.get('parent_name')
                if p_name:
                    # 表示当前访问的是子权限，让父级选中
                    # request.xxxxxx = p_name
                    p_dict = permission_dict[p_name]
                    breadcrumb_list.append({'url': p_dict['url'], 'title': p_dict['title']})
                    breadcrumb_list.append({'url': v['url'], 'title': v['title']})
                    setattr(request, settings.RBAC_CURRENT_PARENT_NAME, p_name)
                else:
                    # 表示当前访问的是父权限，让自己选中
                    # request.xxxxxx = name
                    breadcrumb_list.append({'url': v['url'], 'title': v['title']})
                    setattr(request, settings.RBAC_CURRENT_PARENT_NAME, name)
                setattr(request, settings.RBAC_BREADCRUMB, breadcrumb_list)
                return
        setattr(request, settings.RBAC_BREADCRUMB, breadcrumb_list)
        # 登录后不需要权限的地址
        for i in settings.RBAC_NO_PERMISSION_LIST:
            if re.match(i, url):
                return

        return HttpResponse('没有相关的权限')
