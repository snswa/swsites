# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CountyTeam'
        db.create_table('zipcodes_countyteam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('county', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zipcodes.County'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.Team'])),
        ))
        db.send_create_signal('zipcodes', ['CountyTeam'])

        # Adding unique constraint on 'CountyTeam', fields ['county', 'team']
        db.create_unique('zipcodes_countyteam', ['county_id', 'team_id'])

        # Adding model 'ZipCodeTeam'
        db.create_table('zipcodes_zipcodeteam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zipcodes.ZipCode'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.Team'])),
        ))
        db.send_create_signal('zipcodes', ['ZipCodeTeam'])

        # Adding unique constraint on 'ZipCodeTeam', fields ['zip_code', 'team']
        db.create_unique('zipcodes_zipcodeteam', ['zip_code_id', 'team_id'])

        # Removing M2M table for field teams on 'County'
        db.delete_table('zipcodes_county_teams')

        # Removing M2M table for field teams on 'ZipCode'
        db.delete_table('zipcodes_zipcode_teams')


    def backwards(self, orm):
        
        # Removing unique constraint on 'ZipCodeTeam', fields ['zip_code', 'team']
        db.delete_unique('zipcodes_zipcodeteam', ['zip_code_id', 'team_id'])

        # Removing unique constraint on 'CountyTeam', fields ['county', 'team']
        db.delete_unique('zipcodes_countyteam', ['county_id', 'team_id'])

        # Deleting model 'CountyTeam'
        db.delete_table('zipcodes_countyteam')

        # Deleting model 'ZipCodeTeam'
        db.delete_table('zipcodes_zipcodeteam')

        # Adding M2M table for field teams on 'County'
        db.create_table('zipcodes_county_teams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('county', models.ForeignKey(orm['zipcodes.county'], null=False)),
            ('team', models.ForeignKey(orm['teams.team'], null=False))
        ))
        db.create_unique('zipcodes_county_teams', ['county_id', 'team_id'])

        # Adding M2M table for field teams on 'ZipCode'
        db.create_table('zipcodes_zipcode_teams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('zipcode', models.ForeignKey(orm['zipcodes.zipcode'], null=False)),
            ('team', models.ForeignKey(orm['teams.team'], null=False))
        ))
        db.create_unique('zipcodes_zipcode_teams', ['zipcode_id', 'team_id'])


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
        'teams.member': {
            'Meta': {'object_name': 'Member'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_coordinator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'teams.team': {
            'Meta': {'ordering': "['name']", 'object_name': 'Team'},
            'auto_join': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['teams.Member']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'zipcodes.county': {
            'Meta': {'object_name': 'County'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'counties'", 'symmetrical': 'False', 'through': "orm['zipcodes.CountyTeam']", 'to': "orm['teams.Team']"})
        },
        'zipcodes.countyteam': {
            'Meta': {'unique_together': "(('county', 'team'),)", 'object_name': 'CountyTeam'},
            'county': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zipcodes.County']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']"})
        },
        'zipcodes.zipcode': {
            'Meta': {'ordering': "('county', 'city', 'zip_code')", 'object_name': 'ZipCode'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'county': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'long': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'zip_codes'", 'symmetrical': 'False', 'through': "orm['zipcodes.ZipCodeTeam']", 'to': "orm['teams.Team']"}),
            'zip_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5', 'db_index': 'True'})
        },
        'zipcodes.zipcodeteam': {
            'Meta': {'unique_together': "(('zip_code', 'team'),)", 'object_name': 'ZipCodeTeam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.Team']"}),
            'zip_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zipcodes.ZipCode']"})
        }
    }

    complete_apps = ['zipcodes']
