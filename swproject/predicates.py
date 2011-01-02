from groups.templatetags.group_tags import ismemberofgroup
from teams.templatetags.team_tags import iscoordinatorofteam


def event_edit(request, event):
    group = request.group
    user = request.user
    if iscoordinatorofteam(user, group):
        return True
    if getattr(group, 'is_private', False) and ismemberofgroup(user, group):
        return True
    return False

event_delete = event_edit
