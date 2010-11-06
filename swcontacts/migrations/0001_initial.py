# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Person'
        db.create_table('swcontacts_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('given_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('last_contacted', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('swcontacts', ['Person'])

        # Adding M2M table for field interests on 'Person'
        db.create_table('swcontacts_person_interests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['swcontacts.person'], null=False)),
            ('interest', models.ForeignKey(orm['swcontacts.interest'], null=False))
        ))
        db.create_unique('swcontacts_person_interests', ['person_id', 'interest_id'])

        # Adding model 'Organization'
        db.create_table('swcontacts_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('last_contacted', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('swcontacts', ['Organization'])

        # Adding model 'Change'
        db.create_table('swcontacts_change', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('swcontacts', ['Change'])

        # Adding model 'Address'
        db.create_table('swcontacts_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('swcontacts', ['Address'])

        # Adding model 'Phone'
        db.create_table('swcontacts_phone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('validated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('swcontacts', ['Phone'])

        # Adding model 'Email'
        db.create_table('swcontacts_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('validated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('swcontacts', ['Email'])

        # Adding model 'Relationship'
        db.create_table('swcontacts_relationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('who_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_who_set', to=orm['contenttypes.ContentType'])),
            ('who_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('whom_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_whom_set', to=orm['contenttypes.ContentType'])),
            ('whom_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('swcontacts', ['Relationship'])

        # Adding model 'Interest'
        db.create_table('swcontacts_interest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('swcontacts', ['Interest'])


    def backwards(self, orm):
        
        # Deleting model 'Person'
        db.delete_table('swcontacts_person')

        # Removing M2M table for field interests on 'Person'
        db.delete_table('swcontacts_person_interests')

        # Deleting model 'Organization'
        db.delete_table('swcontacts_organization')

        # Deleting model 'Change'
        db.delete_table('swcontacts_change')

        # Deleting model 'Address'
        db.delete_table('swcontacts_address')

        # Deleting model 'Phone'
        db.delete_table('swcontacts_phone')

        # Deleting model 'Email'
        db.delete_table('swcontacts_email')

        # Deleting model 'Relationship'
        db.delete_table('swcontacts_relationship')

        # Deleting model 'Interest'
        db.delete_table('swcontacts_interest')


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
        'swcontacts.address': {
            'Meta': {'object_name': 'Address'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'})
        },
        'swcontacts.change': {
            'Meta': {'object_name': 'Change'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'swcontacts.email': {
            'Meta': {'object_name': 'Email'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'validated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'swcontacts.interest': {
            'Meta': {'object_name': 'Interest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'swcontacts.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_contacted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        'swcontacts.person': {
            'Meta': {'object_name': 'Person'},
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['swcontacts.Interest']", 'symmetrical': 'False'}),
            'last_contacted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'swcontacts.phone': {
            'Meta': {'object_name': 'Phone'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'validated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'swcontacts.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'who_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_who_set'", 'to': "orm['contenttypes.ContentType']"}),
            'who_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'whom_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_whom_set'", 'to': "orm['contenttypes.ContentType']"}),
            'whom_object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['swcontacts']
