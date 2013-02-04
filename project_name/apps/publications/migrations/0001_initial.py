# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Monthly'
        db.create_table(u'publications_monthly', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateix', self.gf('django.db.models.fields.DateField')(unique=True)),
        ))
        db.send_create_signal(u'publications', ['Monthly'])

        # Adding model 'Publication'
        db.create_table(u'publications_publication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('date_stamp', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('publication_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publications.Monthly'], unique=True)),
        ))
        db.send_create_signal(u'publications', ['Publication'])


    def backwards(self, orm):
        # Deleting model 'Monthly'
        db.delete_table(u'publications_monthly')

        # Deleting model 'Publication'
        db.delete_table(u'publications_publication')


    models = {
        u'publications.monthly': {
            'Meta': {'ordering': "['dateix']", 'object_name': 'Monthly'},
            'dateix': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'publications.publication': {
            'Meta': {'ordering': "['-publication_date']", 'object_name': 'Publication'},
            'data_status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'date_stamp': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication_date': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['publications.Monthly']", 'unique': 'True'})
        }
    }

    complete_apps = ['publications']