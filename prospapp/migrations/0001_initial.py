# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'prospapp_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('organisation', self.gf('django.db.models.fields.CharField')(max_length=63, blank=True)),
        ))
        db.send_create_signal(u'prospapp', ['Account'])

        # Adding M2M table for field groups on 'Account'
        m2m_table_name = db.shorten_name(u'prospapp_account_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm[u'prospapp.account'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Account'
        m2m_table_name = db.shorten_name(u'prospapp_account_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm[u'prospapp.account'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'permission_id'])

        # Adding model 'BaseImage'
        db.create_table(u'prospapp_baseimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=31, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=127, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='images', null=True, to=orm['prospapp.BaseImage'])),
        ))
        db.send_create_signal(u'prospapp', ['BaseImage'])

        # Adding model 'TestImage'
        db.create_table(u'prospapp_testimage', (
            (u'baseimage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['prospapp.BaseImage'], unique=True, primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['prospapp.Account'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('instructions', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'prospapp', ['TestImage'])

        # Adding model 'Test'
        db.create_table(u'prospapp_test', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tests', to=orm['prospapp.TestImage'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tests', to=orm['prospapp.Account'])),
            ('instructions', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'prospapp', ['Test'])

        # Adding model 'TestInstance'
        db.create_table(u'prospapp_testinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['prospapp.Test'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['prospapp.Account'])),
        ))
        db.send_create_signal(u'prospapp', ['TestInstance'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'prospapp_account')

        # Removing M2M table for field groups on 'Account'
        db.delete_table(db.shorten_name(u'prospapp_account_groups'))

        # Removing M2M table for field user_permissions on 'Account'
        db.delete_table(db.shorten_name(u'prospapp_account_user_permissions'))

        # Deleting model 'BaseImage'
        db.delete_table(u'prospapp_baseimage')

        # Deleting model 'TestImage'
        db.delete_table(u'prospapp_testimage')

        # Deleting model 'Test'
        db.delete_table(u'prospapp_test')

        # Deleting model 'TestInstance'
        db.delete_table(u'prospapp_testinstance')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'prospapp.account': {
            'Meta': {'object_name': 'Account'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '63', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'prospapp.baseimage': {
            'Meta': {'object_name': 'BaseImage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'to': u"orm['prospapp.BaseImage']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '31', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'prospapp.test': {
            'Meta': {'object_name': 'Test'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tests'", 'to': u"orm['prospapp.TestImage']"}),
            'instructions': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tests'", 'to': u"orm['prospapp.Account']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'prospapp.testimage': {
            'Meta': {'object_name': 'TestImage', '_ormbases': [u'prospapp.BaseImage']},
            u'baseimage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['prospapp.BaseImage']", 'unique': 'True', 'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['prospapp.Account']"})
        },
        u'prospapp.testinstance': {
            'Meta': {'object_name': 'TestInstance'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': u"orm['prospapp.Account']"}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': u"orm['prospapp.Test']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['prospapp']