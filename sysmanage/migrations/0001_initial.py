# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=50, verbose_name='\u663e\u793a\u540d\u79f0', blank=True)),
                ('is_enable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528')),
                ('is_built_in', models.BooleanField(default=True, verbose_name='\u662f\u5426\u5185\u7f6e')),
                ('description', models.CharField(max_length=140, null=True, verbose_name='\u63cf\u8ff0', blank=True)),
                ('group', models.OneToOneField(verbose_name='\u7ec4', to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupToMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_by', models.CharField(max_length=50, verbose_name='\u521b\u5efa\u8005', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('remarks', models.TextField(verbose_name='\u5907\u6ce8\u4fe1\u606f', blank=True)),
                ('updated_by', models.CharField(max_length=50, verbose_name='\u4fee\u6539\u8005', blank=True)),
                ('updated_date', models.DateTimeField(null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', blank=True)),
                ('group', models.ForeignKey(verbose_name='\u89d2\u8272', to='auth.Group')),
            ],
            options={
                'verbose_name': '\u89d2\u8272\u83dc\u5355\u4e2d\u95f4\u8868',
                'verbose_name_plural': '\u89d2\u8272\u83dc\u5355\u4e2d\u95f4\u8868',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operator_date', models.DateTimeField(null=True, verbose_name='\u64cd\u4f5c\u65f6\u95f4', blank=True)),
                ('operator', models.CharField(max_length=50, verbose_name='\u64cd\u4f5c\u8005')),
                ('operated_object', models.CharField(max_length=50, verbose_name='\u64cd\u4f5c\u5bf9\u8c61')),
                ('operated_type', models.CharField(max_length=50, verbose_name='\u64cd\u4f5c\u7c7b\u578b')),
                ('content', models.TextField(verbose_name='\u64cd\u4f5c\u5185\u5bb9', blank=True)),
                ('ip_addr', models.CharField(max_length=50, null=True, verbose_name='IP\u5730\u5740', blank=True)),
                ('is_success', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6210\u529f')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'Log',
                'verbose_name_plural': 'Log',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('display_name', models.CharField(max_length=50, verbose_name='\u663e\u793a\u540d\u79f0', blank=True)),
                ('path', models.CharField(max_length=50, verbose_name='path\u5730\u5740', blank=True)),
                ('image_url', models.CharField(max_length=50, verbose_name='image\u5730\u5740', blank=True)),
                ('image_h_url', models.CharField(max_length=50, verbose_name='image\u9ad8\u4eae\u5730\u5740', blank=True)),
                ('icon', models.CharField(max_length=255, null=True, verbose_name='\u4e00\u7ea7\u83dc\u5355\u56fe\u6807', blank=True)),
                ('is_menu', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e3a\u83dc\u5355')),
                ('remarks', models.TextField(verbose_name='\u5907\u6ce8\u4fe1\u606f', blank=True)),
                ('created_by', models.CharField(max_length=50, verbose_name='\u521b\u5efa\u8005', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated_by', models.CharField(max_length=50, verbose_name='\u4fee\u6539\u8005', blank=True)),
                ('updated_date', models.DateTimeField(null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', blank=True)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='\u89d2\u8272', through='sysmanage.GroupToMenu', blank=True)),
                ('parent', models.ForeignKey(verbose_name='\u7236\u7ea7\u83dc\u5355', blank=True, to='sysmanage.Menu', null=True)),
            ],
            options={
                'verbose_name': '\u83dc\u5355',
                'verbose_name_plural': '\u83dc\u5355',
            },
        ),
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=50, verbose_name='\u663e\u793a\u540d\u79f0')),
                ('is_enable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528')),
            ],
            options={
                'verbose_name': '\u6743\u9650\u5206\u7ec4',
                'verbose_name_plural': '\u6743\u9650\u5206\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='PermissionProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=50, verbose_name='\u663e\u793a\u540d\u79f0', blank=True)),
                ('is_enable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528')),
                ('permission', models.OneToOneField(verbose_name='\u6743\u9650', to='auth.Permission')),
                ('permission_group', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u6743\u9650\u5206\u7ec4', blank=True, to='sysmanage.PermissionGroup', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='\u540d\u79f0')),
                ('description', models.CharField(max_length=254, verbose_name='\u63cf\u8ff0\u4fe1\u606f', blank=True)),
                ('value', models.TextField(verbose_name='\u503c', blank=True)),
                ('type', models.CharField(default=b'str', max_length=20, verbose_name='\u503c\u7c7b\u578b', choices=[(b'int', b'int'), (b'str', b'str'), (b'json', b'json')])),
                ('is_show', models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a')),
                ('created_by', models.CharField(max_length=50, verbose_name='\u521b\u5efa\u8005', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('remarks', models.TextField(verbose_name='\u5907\u6ce8\u4fe1\u606f', blank=True)),
                ('updated_by', models.CharField(max_length=50, verbose_name='\u4fee\u6539\u8005', blank=True)),
                ('updated_date', models.DateTimeField(null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', blank=True)),
            ],
            options={
                'verbose_name': '\u8bbe\u7f6e',
                'verbose_name_plural': '\u8bbe\u7f6e',
            },
        ),
        migrations.AddField(
            model_name='grouptomenu',
            name='menu',
            field=models.ForeignKey(verbose_name='\u83dc\u5355', to='sysmanage.Menu'),
        ),
    ]
