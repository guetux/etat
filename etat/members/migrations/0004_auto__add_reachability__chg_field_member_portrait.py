# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Reachability'
        db.create_table(u'members_reachability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reachabilities', to=orm['members.Member'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'members', ['Reachability'])


        # Changing field 'Member.portrait'
        db.alter_column(u'members_member', 'portrait', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True))

    def backwards(self, orm):
        # Deleting model 'Reachability'
        db.delete_table(u'members_reachability')


        # Changing field 'Member.portrait'
        db.alter_column(u'members_member', 'portrait', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

    models = {
        u'departments.department': {
            'Meta': {'object_name': 'Department'},
            'default_role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['members.RoleType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['departments.Department']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['departments.DepartmentType']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'departments.departmenttype': {
            'Meta': {'object_name': 'DepartmentType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'members.address': {
            'Meta': {'object_name': 'Address'},
            'addition': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django_countries.fields.CountryField', [], {'default': "'CH'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'to': u"orm['members.Member']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'members.member': {
            'Meta': {'object_name': 'Member'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'departments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'members'", 'symmetrical': 'False', 'through': u"orm['members.Role']", 'to': u"orm['departments.Department']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'portrait': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'scout_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'members.reachability': {
            'Meta': {'object_name': 'Reachability'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reachabilities'", 'to': u"orm['members.Member']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'members.role': {
            'Meta': {'object_name': 'Role'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['departments.Department']"}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['members.Member']"}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.RoleType']"})
        },
        u'members.roletype': {
            'Meta': {'ordering': "('order',)", 'object_name': 'RoleType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['members']