# Generated by Django 2.0.4 on 2018-05-15 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BCP47',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('langtag', models.CharField(max_length=255, verbose_name='IETF BCP 47 langtag')),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_largue', models.BooleanField(default=False)),
                ('small', models.CharField(blank=True, max_length=255, null=True, verbose_name='small')),
                ('largue', models.TextField(blank=True, null=True, verbose_name='largue')),
                ('bcp47', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='tradukoj.BCP47')),
            ],
        ),
        migrations.CreateModel(
            name='TranslationKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='text key')),
            ],
        ),
        migrations.AddField(
            model_name='translation',
            name='key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='tradukoj.TranslationKey'),
        ),
    ]
