from django import forms

from iris.base import ModelPluginForm
from iris.base import ItemTypePlugin

from swtopics.models import Message


class MessageForm(ModelPluginForm):

    class Meta:
        model = Message


class MessageAddPlugin(ItemTypePlugin):

    label = u'message'
    name = u'swtopics.message.add'
    form_class = MessageForm
