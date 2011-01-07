# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Message'
        db.create_table('swtopics_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('swtopics', ['Message'])


    def backwards(self, orm):
        
        # Deleting model 'Message'
        db.delete_table('swtopics_message')


    models = {
        'swtopics.message': {
            'Meta': {'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['swtopics']
