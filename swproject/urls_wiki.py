from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from wakawaka.urls import urlpatterns


user_can_view_wiki = user_passes_test(
    lambda user: user.has_perm("wakawaka.can_view"),
)


for waka_url in urlpatterns:
    callback = waka_url.callback
    waka_url._callback = user_can_view_wiki(callback)
