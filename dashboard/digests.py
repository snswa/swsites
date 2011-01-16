import datetime

from django.contrib.auth.models import User

from dregni.models import Event
from iris.models import Topic


def daily_context(user, start_date, end_date):
    # For each team the user is a member of, starting with their coordinator
    # teams and then the rest of the teams...
    teams = [member.team for member in user.member_set.filter(is_coordinator=True)]
    teams.extend(member.team for member in user.member_set.filter(is_coordinator=False))
    team_info_list = []
    for team in teams:
        new_members = User.objects.filter(
            member__team=team,
            member__joined__gte=start_date,
            member__joined__lte=end_date,
        )
        events = team.content_objects(Event).filter(
            start_date__gte=start_date.date() - datetime.timedelta(days=4),
            start_date__lte=end_date.date() + datetime.timedelta(days=14),
        )
        topics = Topic.objects.with_participant(team).filter(
            modified__gte=start_date,
            modified__lte=end_date,
        )
        has_activity = sum([new_members.count(), events.count(), topics.count()]) > 0
        team_info_list.append(dict(
            team=team,
            new_members=new_members,
            events=events,
            topics=topics,
            has_activity=has_activity,
        ))
    any_with_activity = any(team_info['has_activity'] for team_info in team_info_list)
    any_with_no_activity = any(not team_info['has_activity'] for team_info in team_info_list)
    return dict(
        user=user,
        start_date=start_date,
        end_date=end_date,
        team_info_list=team_info_list,
        any_with_activity=any_with_activity,
        any_with_no_activity=any_with_no_activity,
    )
