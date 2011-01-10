# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SubjectChange'
        db.create_table('swtopics_subjectchange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('new_subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('swtopics', ['SubjectChange'])


    def backwards(self, orm):
        
        # Deleting model 'SubjectChange'
        db.delete_table('swtopics_subjectchange')


    models = {
        'swtopics.message': {
            'Meta': {'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'swtopics.subjectchange': {
            'Meta': {'object_name': 'SubjectChange'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['swtopics']
