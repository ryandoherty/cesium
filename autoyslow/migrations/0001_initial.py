
from south.db import db
from django.db import models
from cesium.autoyslow.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Site'
        db.create_table('autoyslow_site', (
            ('id', orm['autoyslow.Site:id']),
            ('base_url', orm['autoyslow.Site:base_url']),
            ('last_testrun', orm['autoyslow.Site:last_testrun']),
        ))
        db.send_create_signal('autoyslow', ['Site'])
        
        # Adding model 'Page'
        db.create_table('autoyslow_page', (
            ('id', orm['autoyslow.Page:id']),
            ('url', orm['autoyslow.Page:url']),
            ('site', orm['autoyslow.Page:site']),
            ('last_testrun', orm['autoyslow.Page:last_testrun']),
        ))
        db.send_create_signal('autoyslow', ['Page'])
        
        # Adding model 'UserProfile'
        db.create_table('autoyslow_userprofile', (
            ('id', orm['autoyslow.UserProfile:id']),
            ('user', orm['autoyslow.UserProfile:user']),
        ))
        db.send_create_signal('autoyslow', ['UserProfile'])
        
        # Adding model 'Test'
        db.create_table('autoyslow_test', (
            ('id', orm['autoyslow.Test:id']),
            ('score', orm['autoyslow.Test:score']),
            ('weight', orm['autoyslow.Test:weight']),
            ('requests', orm['autoyslow.Test:requests']),
            ('time', orm['autoyslow.Test:time']),
            ('page', orm['autoyslow.Test:page']),
        ))
        db.send_create_signal('autoyslow', ['Test'])
        
        # Adding ManyToManyField 'UserProfile.sites'
        db.create_table('autoyslow_userprofile_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm.UserProfile, null=False)),
            ('site', models.ForeignKey(orm.Site, null=False))
        ))
        
        # Adding ManyToManyField 'UserProfile.pages'
        db.create_table('autoyslow_userprofile_pages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm.UserProfile, null=False)),
            ('page', models.ForeignKey(orm.Page, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Site'
        db.delete_table('autoyslow_site')
        
        # Deleting model 'Page'
        db.delete_table('autoyslow_page')
        
        # Deleting model 'UserProfile'
        db.delete_table('autoyslow_userprofile')
        
        # Deleting model 'Test'
        db.delete_table('autoyslow_test')
        
        # Dropping ManyToManyField 'UserProfile.sites'
        db.delete_table('autoyslow_userprofile_sites')
        
        # Dropping ManyToManyField 'UserProfile.pages'
        db.delete_table('autoyslow_userprofile_pages')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'autoyslow.page': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_testrun': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autoyslow.Site']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '900'})
        },
        'autoyslow.site': {
            'base_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_testrun': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'autoyslow.test': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autoyslow.Page']"}),
            'requests': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        'autoyslow.userprofile': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['autoyslow.Page']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['autoyslow.Site']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['autoyslow']
