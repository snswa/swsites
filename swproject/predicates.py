import datetime

from iris.models import Topic
from teams.models import Team
from teams.templatetags.team_tags import iscoordinatorofteam
from wakawaka.models import Revision, WikiPage


class TopicAccessBackend(object):

    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        #
        if perm == 'iris.add_topic':
            if user_obj.is_staff:
                return True
            # Authenticated users can add topics.
            if user_obj.is_authenticated():
                return True
            # Default: cannot add a topic.
            return False
        #
        if perm == 'iris.join_topic':
            # Default: cannot join a topic.
            return False
        #
        if perm == 'iris.view_topic' and isinstance(obj, Topic):
            if user_obj.is_staff:
                return True
            if user_obj.is_authenticated():
                # Find teams joined to the topic.
                # If the user is a member of any of the teams in the topic,
                # or none of the teams joined to the topic are private,
                # allow viewing.
                teams_joined = obj.participants_of_type(Team)
                any_private = False
                any_member = False
                for participant in teams_joined:
                    team = participant.content
                    if team.is_private:
                        any_private = True
                    if team.user_is_member(user_obj):
                        any_member = True
                        break
                if any_member or not any_private:
                    return True
            # Default: cannot view any topic.
            return False
        #
        if perm == 'iris.add_to_topic':
            if user_obj.is_staff:
                return True
            if user_obj.is_authenticated():
                # Find teams joined to the topic.
                # If the user is a member of any of the teams in the topic,
                # allow adding.
                teams_joined = obj.participants_of_type(Team)
                for participant in teams_joined:
                    team = participant.content
                    if team.user_is_member(user_obj):
                        return True
            # Default: cannot add any item.
            return False


class WikiAccessBackend(object):

    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        def has_permission_for_group(group):
            return user_obj.is_staff or (
                # Page has a group associated.
                group is not None
                and (
                    # User is coordinator of the group, or
                    iscoordinatorofteam(user_obj, group)
                    or (
                        # User is member and either the group is private
                        # or the user has been a member for more than 4 days.
                        group.user_is_member(user_obj)
                        and (
                            group.is_private
                            or (user_obj.date_joined < datetime.datetime.now() - datetime.timedelta(days=4))
                        )
                    )
                )
            )
        if isinstance(obj, WikiPage):
            # Allow coordinators to change wiki pages in public groups.
            # Allow any member to change wiki pages in private groups.
            if perm == 'wakawaka.change_wikipage' or perm == 'wakawaka.change_revision':
                return obj.group and has_permission_for_group(obj.group)
            # Allow coordinators to delete wiki pages in public groups.
            # Allow any member to delete wiki pages in private groups.
            if perm == 'wakawaka.delete_wikipage' or perm == 'wakawaka.delete_revision':
                return obj.group and has_permission_for_group(obj.group)
        elif isinstance(obj, Team):
            # Allow coordinators to add wiki pages in public groups.
            # Allow any member to add wiki pages in private groups.
            if perm == 'wakawaka.add_wikipage' or perm == 'wakawaka.add_revision':
                return has_permission_for_group(obj)
            # Allow coordinators to reset edit locks on wiki pages in public groups.
            # Allow any member to reset edit locks in private groups.
            if perm == 'wakawaka.reset_lock':
                return has_permission_for_group(obj)


# @@@ replace this with use of per-object restrictions

from groups.templatetags.group_tags import ismemberofgroup
from teams.templatetags.team_tags import iscoordinatorofteam


def event_edit(request, event):
    group = request.group
    user = request.user
    if user.is_staff:
        return True
    if iscoordinatorofteam(user, group):
        return True
    if getattr(group, 'is_private', False) and group.user_is_member(user):
        return True
    return False

event_delete = event_edit
