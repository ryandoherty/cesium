
from south.db import db
from django.db import models
from cesium.autoyslow.models import *

class Migration:

    def forwards(self, orm):

        # Adding ManyToManyField 'Site.users'
        db.create_table('autoyslow_site_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('site', models.ForeignKey(orm.Site, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))

        # Adding ManyToManyField 'Page.users'
        db.create_table('autoyslow_page_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm.Page, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))

        # Deleting model 'userprofile' and related M2M tables.
        db.delete_table('autoyslow_userprofile_pages')
        db.delete_table('autoyslow_userprofile_sites')
        db.delete_table('autoyslow_userprofile')

        # Creating unique_together for [base_url] on Site.
        db.create_unique('autoyslow_site', ['base_url'])



    def backwards(self, orm):

        # Deleting unique_together for [base_url] on Site.
        db.delete_unique('autoyslow_site', ['base_url'])

        # Dropping ManyToManyField 'Site.users'
        db.delete_table('autoyslow_site_users')

        # Dropping ManyToManyField 'Page.users'
        db.delete_table('autoyslow_page_users')

        # Adding model 'userprofile'
        db.create_table('autoyslow_userprofile', (
            ('sites', orm['autoyslow.page:sites']),
            ('user', orm['autoyslow.page:user']),
            ('id', orm['autoyslow.page:id']),
            ('pages', orm['autoyslow.page:pages']),
        ))
        db.send_create_signal('autoyslow', ['userprofile'])



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
            'base_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_testrun': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"})
        },
        'autoyslow.test': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['autoyslow.Page']"}),
            'requests': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
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
