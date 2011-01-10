from django import forms

from iris.base import ModelPluginForm
from iris.base import ItemTypePlugin

from swtopics.models import Message
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
