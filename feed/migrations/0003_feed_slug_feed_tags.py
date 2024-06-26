# Generated by Django 5.0.4 on 2024-04-18 15:16

import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_remove_feed_likes_feed_likes'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='slug',
            field=models.SlugField(allow_unicode=True, help_text='one word for title alias', null=True, unique=True, verbose_name='SLUG'),
        ),
        migrations.AddField(
            model_name='feed',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
