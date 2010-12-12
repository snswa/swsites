# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ZipCode'
        db.create_table('zipcodes_zipcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5, db_index=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('county', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=40, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, db_index=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True)),
            ('long', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True)),
        ))
        db.send_create_signal('zipcodes', ['ZipCode'])


    def backwards(self, orm):
        
        # Deleting model 'ZipCode'
        db.delete_table('zipcodes_zipcode')


    models = {
        'zipcodes.zipcode': {
            'Meta': {'ordering': "('zip_code',)", 'object_name': 'ZipCode'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'county': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'long': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5', 'db_index': 'True'})
        }
    }

    complete_apps = ['zipcodes']
