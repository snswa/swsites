from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from wakawaka.urls import decorated_urlpatterns


user_can_view_wiki = user_passes_test(
    lambda user: user.has_perm("wakawaka.can_view"),
)


urlpatterns = decorated_urlpatterns(user_can_view_wiki)
