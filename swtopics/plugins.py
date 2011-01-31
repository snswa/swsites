from django.db.models import Q
from django import forms

from iris.base import ModelPluginForm, PluginForm
from iris.base import ItemTypePlugin

from swtopics.models import SubjectChange, Message
from teams.models import Member, Team
from teams.templatetags.team_tags import iscoordinatorofteam


# ---


class MessageForm(ModelPluginForm):

    class Meta:
        model = Message


class MessageAddPlugin(ItemTypePlugin):

    label = u'message'
    name = u'swtopics.message.add'
    form_class = MessageForm


# ---


class ParticipantAddTeamForm(PluginForm):

    team = forms.ModelChoiceField(queryset=Team.objects)

    def save(self):
        user = self._request.user
        topic = self._topic
        team = self.cleaned_data['team']
        participant = topic.get_participant(team)
        if participant is None:
            # New join.
            return topic.add_participant(
                creator=user,
                obj=team,
            )
        elif not participant.is_active:
            # Re-join.
            participant.is_active = True
            participant.save()
            from iris.models import ParticipantJoin
            join = ParticipantJoin(
                participant=participant,
            )
            join.save()
            return topic.add_item(
                creator=user,
                obj=join,
            )


class ParticipantAddTeamPlugin(ItemTypePlugin):

    label = u'participating team'
    name = 'iris.participantjoin.add.team'
    form_class = ParticipantAddTeamForm

    def user_has_perm(self, user, topic):
        if user.is_superuser or user.is_staff:
            return True
        # If a topic is in any team that is not private, allow adding
        # other teams to the topic.
        # If a topic is ONLY in private teams, disallow adding other
        # teams to the topic.
        teams = set(p.content for p in topic.participants_of_type(Team))
        return any(not team.is_private for team in teams)


# ---


class ParticipantRemoveTeamForm(PluginForm):

    team = forms.ModelChoiceField(queryset=Team.objects)

    def __init__(self, *args, **kwargs):
        super(ParticipantRemoveTeamForm, self).__init__(*args, **kwargs)
        user = self._request.user
        # Build a query that selects teams that are participants of this
        # topic.
        team_participants = self._topic.participants_of_type(Team).filter(is_active=True)
        q = None
        for participant in team_participants:
            q2 = Q(id=participant.object_id)
            if q is not None:
                q |= q2
            else:
                q = q2
        if not (user.is_superuser or user.is_staff):
            # If not staff, restrict to only those teams for which the
            # user is a coordinator.
            q2 = Q(members=user) & Q(member__is_coordinator=True)
            if q is not None:
                q &= q2
            else:
                q = q2
        if q is not None:
            self.fields['team'].queryset = Team.objects.filter(q)
        else:
            self.fields['team'].queryset = Team.objects.none()

    def save(self):
        user = self._request.user
        topic = self._topic
        team = self.cleaned_data['team']
        participant = topic.get_participant(team)
        if participant is not None:
            participant.is_active = False
            participant.save()
            from iris.models import ParticipantLeave
            leave = ParticipantLeave(
                participant=participant,
            )
            leave.save()
            return topic.add_item(
                creator=user,
                obj=leave,
            )


class ParticipantRemoveTeamPlugin(ItemTypePlugin):

    label = u'team removal'
    name = 'iris.participantleave.remove.team'
    action_label = u'Remove a participating team'
    form_class = ParticipantRemoveTeamForm

    def user_has_perm(self, user, topic):
        if user.is_superuser or user.is_staff:
            return True
        # If the user is a coordinator of any of the teams that are active
        # participants, allow them to remove a participating team.
        teams = set(p.content for p in topic.participants_of_type(Team).filter(is_active=True))
        return any(iscoordinatorofteam(user, team) for team in teams)


# ---


class SubjectChangeForm(ModelPluginForm):

    class Meta:
        model = SubjectChange
        fields = ('new_subject',)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        # Initial value for new subject is the current subject.
        if 'new_subject' not in initial and 'topic' in kwargs:
            initial['new_subject'] = kwargs['topic'].subject
        kwargs['initial'] = initial
        super(SubjectChangeForm, self).__init__(*args, **kwargs)

    def clean_new_subject(self):
        new_subject = self.cleaned_data['new_subject'].strip()
        if new_subject == '':
            raise forms.ValidationError('Subject must not be empty.')
        if new_subject == self._topic.subject:
            raise forms.ValidationError('Please choose a new subject.')
        return new_subject

    def save(self):
        user = self._request.user
        topic = self._topic
        new_subject = self.cleaned_data['new_subject']
        subject_change = SubjectChange(
            old_subject=topic.subject,
            new_subject=new_subject,
        )
        subject_change.save()
        topic.subject = subject_change.new_subject
        topic.save()
        return topic.add_item(
            creator=user,
            obj=subject_change,
        )


class SubjectChangePlugin(ItemTypePlugin):

    label = u'subject change'
    name = 'swtopics.subjectchange.add'
    action_label = u'Change the subject'
    form_class = SubjectChangeForm
