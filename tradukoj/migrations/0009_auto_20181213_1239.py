# Generated by Django 2.0.4 on 2018-12-13 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tradukoj', '0008_pre_switch_namespace_field'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='translationkey',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='translationkey',
            name='namespace',
        ),
    ]