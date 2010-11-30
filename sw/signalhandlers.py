from django.conf import settings
from django.db.models.signals import post_save

from django.contrib.auth.models import Group, User

from actstream import action

from wakawaka.models import Revision


# ====================================================================
# Auto join users to groups specified in settings.AUTO_JOIN_GROUPS

def auto_join_user_to_groups(sender, instance, created, **kwargs):
    if created:
        for group_name in settings.AUTO_JOIN_GROUPS:
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                pass
            else:
                instance.groups.add(group)

post_save.connect(auto_join_user_to_groups, sender=User)


# ====================================================================
# Activity stream

def stream_wiki_revision(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.creator,
            verb='changed wiki page',
            action_object=instance,
            target=instance.page.group,
            timestamp=instance.modified,
            description=instance.message,
        )

post_save.connect(stream_wiki_revision, sender=Revision)
