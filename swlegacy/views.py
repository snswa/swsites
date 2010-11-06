from django.http import HttpResponseRedirect
from django.views.defaults import page_not_found


INDIVIDUALS = [
    ('/donate/paypal', '/blog/donate/'),
    ]

BLOG_PAGES = [
    #
    # static
    'images',
    'wp-',
    #
    # posts
    'uncategorized',
    'feed',
    #
    # pages
    '2010-campaign',
    '2011-campaign',
    'about',
    'donate',
    'donate2',
    'media',
    'political-landscape',
    'volunteer',
    ]


def legacy_or_404(request):
    path = request.environ['PATH_INFO'] # /foo
    qs = request.environ['QUERY_STRING'] # ?bar  (without the ?)
    #
    for src, dest in INDIVIDUALS:
        if path.startswith(src):
            return HttpResponseRedirect(dest)
    #
    for prefix in BLOG_PAGES:
        prefix = '/' + prefix
        if path.startswith(prefix):
            newpath = '/blog' + path
            if qs:
                newpath += '?' + qs
            return HttpResponseRedirect(newpath)
    #
    # Fallback.
    return page_not_found(request)
