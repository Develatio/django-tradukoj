# Generated by Django 2.0.4 on 2018-12-13 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tradukoj', '0007_bcp47_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetTextFile',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('file_type',
                 models.IntegerField(
                     choices=[(0, 'PO file'), (1, 'MO file')], default=0)),
                ('last_updated_date',
                 models.DateTimeField(
                     auto_now=True,
                     db_index=True,
                     verbose_name='Last updated date')),
                ('done', models.BooleanField(default=False)),
                ('done_with_errors', models.BooleanField(default=False)),
                ('log', models.TextField(max_length=1024, verbose_name='Log')),
                ('bcp47',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='get_text_files',
                     to='tradukoj.BCP47',
                     verbose_name='Lang')),
            ],
        ),
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('text',
                 models.CharField(
                     max_length=255, unique=True, verbose_name='text key')),
            ],
        ),
        migrations.AlterField(
            model_name='translationkey',
            name='namespace',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='translationkey',
            name='text',
            field=models.CharField(max_length=255, verbose_name='text key'),
        ),
        migrations.AddField(
            model_name='translationkey',
            name='new_namespace',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='translation_keys',
                to='tradukoj.Namespace'),
        ),
        migrations.AlterUniqueTogether(
            name='translationkey',
            unique_together={('namespace', 'text')},
        ),
        migrations.AddField(
            model_name='gettextfile',
            name='namespace',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='get_text_files',
                to='tradukoj.Namespace'),
        ),
    ]
