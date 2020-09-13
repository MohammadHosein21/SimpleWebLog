# Generated by Django 3.0.9 on 2020-09-06 07:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blog', '0002_auto_20200905_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 6, 7, 48, 17, 170358, tzinfo=utc)),
        ),
    ]
