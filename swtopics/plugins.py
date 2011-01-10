from django import forms

from iris.base import ModelPluginForm
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


class ParticipantAddTeamForm(forms.Form):

    team = forms.ModelChoiceField(queryset=Team.objects)

    def save(self, request, topic):
        user = request.user
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


# ---


class SubjectChangeForm(ModelPluginForm):

    class Meta:
        model = SubjectChange
        fields = ('new_subject',)

    def save(self, request, topic):
        user = request.user
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
