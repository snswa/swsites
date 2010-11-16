# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ForwardedEmailAddress'
        db.create_table('emailfwd_forwardedemailaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('domain', self.gf('django.db.models.fields.CharField')(default='sensiblewashington.org', max_length=50)),
        ))
        db.send_create_signal('emailfwd', ['ForwardedEmailAddress'])

        # Adding model 'EmailDestination'
        db.create_table('emailfwd_emaildestination', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forwarded', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emailfwd.ForwardedEmailAddress'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('emailfwd', ['EmailDestination'])


    def backwards(self, orm):
        
        # Deleting model 'ForwardedEmailAddress'
        db.delete_table('emailfwd_forwardedemailaddress')

        # Deleting model 'EmailDestination'
        db.delete_table('emailfwd_emaildestination')


    models = {
        'emailfwd.emaildestination': {
            'Meta': {'object_name': 'EmailDestination'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'forwarded': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emailfwd.ForwardedEmailAddress']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'emailfwd.forwardedemailaddress': {
            'Meta': {'object_name': 'ForwardedEmailAddress'},
            'domain': ('django.db.models.fields.CharField', [], {'default': "'sensiblewashington.org'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['emailfwd']
