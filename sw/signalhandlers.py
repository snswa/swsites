from django.conf import settings
from django.db.models.signals import post_save

from django.contrib.auth.models import Group, User


def auto_join_user_to_groups(sender, instance=None, **kwargs):
    if instance is not None:
        for group_name in settings.AUTO_JOIN_GROUPS:
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                pass
            else:
                instance.groups.add(group)

post_save.connect(auto_join_user_to_groups, sender=User)
