from django import forms

from iris.base import ModelPluginForm, PluginForm
from iris.base import ItemTypePlugin

from swtopics.models import SubjectChange, Message
from teams.models import Team


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
        if not topic.has_participant(team):
            return topic.add_participant(
                creator=user,
                obj=team,
            )


class ParticipantAddTeamPlugin(ItemTypePlugin):

    label = u'participating team'
    name = 'iris.participantjoin.add.team'
    form_class = ParticipantAddTeamForm

    def user_has_perm(self, user, topic):
        if user.is_superuser:
            return True
        # If a topic is in any team that is not private, allow adding
        # other teams to the topic.
        # If a topic is ONLY in private teams, disallow adding other
        # teams to the topic.
        teams = set(p.content for p in topic.participants_of_type(Team))
        return any(not team.is_private for team in teams)

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
