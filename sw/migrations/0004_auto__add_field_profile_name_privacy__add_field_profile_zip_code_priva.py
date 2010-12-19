# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Profile.name_privacy'
        db.add_column('sw_profile', 'name_privacy', self.gf('django.db.models.fields.CharField')(default='C', max_length=1), keep_default=False)

        # Adding field 'Profile.zip_code_privacy'
        db.add_column('sw_profile', 'zip_code_privacy', self.gf('django.db.models.fields.CharField')(default='C', max_length=1), keep_default=False)

        # Adding field 'Profile.mailing_address_privacy'
        db.add_column('sw_profile', 'mailing_address_privacy', self.gf('django.db.models.fields.CharField')(default='C', max_length=1), keep_default=False)

        # Adding field 'Profile.email_privacy'
        db.add_column('sw_profile', 'email_privacy', self.gf('django.db.models.fields.CharField')(default='C', max_length=1), keep_default=False)

        # Adding field 'Profile.phone_number_accepts_texts'
        db.add_column('sw_profile', 'phone_number_accepts_texts', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Profile.phone_number_privacy'
        db.add_column('sw_profile', 'phone_number_privacy', self.gf('django.db.models.fields.CharField')(default='C', max_length=1), keep_default=False)

        # Adding field 'Profile.messaging_privacy'
        db.add_column('sw_profile', 'messaging_privacy', self.gf('django.db.models.fields.CharField')(default='C', max_length=1), keep_default=False)

        # Adding field 'Profile.preferred_contact_methods_privacy'
        db.add_column('sw_profile', 'preferred_contact_methods_privacy', self.gf('django.db.models.fields.CharField')(default='C', max_length=1), keep_default=False)

        # Adding field 'Profile.bio_privacy'
        db.add_column('sw_profile', 'bio_privacy', self.gf('django.db.models.fields.CharField')(default='C', max_length=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Profile.name_privacy'
        db.delete_column('sw_profile', 'name_privacy')

        # Deleting field 'Profile.zip_code_privacy'
        db.delete_column('sw_profile', 'zip_code_privacy')

        # Deleting field 'Profile.mailing_address_privacy'
        db.delete_column('sw_profile', 'mailing_address_privacy')

        # Deleting field 'Profile.email_privacy'
        db.delete_column('sw_profile', 'email_privacy')

        # Deleting field 'Profile.phone_number_accepts_texts'
        db.delete_column('sw_profile', 'phone_number_accepts_texts')

        # Deleting field 'Profile.phone_number_privacy'
        db.delete_column('sw_profile', 'phone_number_privacy')

        # Deleting field 'Profile.messaging_privacy'
        db.delete_column('sw_profile', 'messaging_privacy')

        # Deleting field 'Profile.preferred_contact_methods_privacy'
        db.delete_column('sw_profile', 'preferred_contact_methods_privacy')

        # Deleting field 'Profile.bio_privacy'
        db.delete_column('sw_profile', 'bio_privacy')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sw.profile': {
            'Meta': {'object_name': 'Profile'},
            'aim': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bio_privacy': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'email_privacy': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'mailing_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mailing_address_privacy': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'messaging_privacy': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'msn_messenger': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name_privacy': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'phone_number_accepts_texts': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number_privacy': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'preferred_contact_methods': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'preferred_contact_methods_privacy': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'preferred_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'yahoo_messenger': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'zip_code_privacy': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'})
        }
    }

    complete_apps = ['sw']
