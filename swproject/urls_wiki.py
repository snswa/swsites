from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from wakawaka.urls import urlpatterns

from teams.api import user_has_team_role


team, role = settings.WAKAWAKA_REQUIRE_TEAM_ROLE


user_is_on_wiki_team = user_passes_test(
    lambda user: user_has_team_role(user, team, role),
)


for waka_url in urlpatterns:
    callback = waka_url.callback
    waka_url._callback = user_is_on_wiki_team(callback)
