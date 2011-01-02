from teams.templatetags.team_tags import iscoordinatorofteam


def event_edit(request, event):
    return iscoordinatorofteam(request.user, request.group)

event_delete = event_edit
