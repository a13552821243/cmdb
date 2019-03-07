from django.conf.urls import url
from crm.views import home, depart, user, classes, account

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'login/', account.login, name='login'),
    url(r'index/', home.index, name='index'),
    url(r'depart/list/', depart.depart_list, name='depart_list'),
    url(r'depart/add/', depart.depart_add, name='depart_add'),
    url(r'depart/edit/(\d+)', depart.depart_edit, name='depart_edit'),
    url(r'depart/del/(\d+)', depart.depart_del, name='depart_del'),

    url(r'user/list/', user.user_list, name='user_list'),
    url(r'user/add/', user.user_add, name='user_add'),

    url(r'class/list/', classes.class_list, name='class_list'),
    url(r'class/add/', classes.classes, name='class_add'),
    url(r'class/edit/(\d+)/', classes.classes, name='class_edit'),

]
