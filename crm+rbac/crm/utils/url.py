from django.shortcuts import reverse


def rev_url(request, name):
    param = request.GET.urlencode()
    base_url = reverse(name)
    if param:
        url = "{}?{}".format(base_url, param)
        return url
    return base_url

def rev_url(request, name):
    next = request.GET.get('next')
    base_url = reverse(name)
    if next:
        return next
    return base_url
