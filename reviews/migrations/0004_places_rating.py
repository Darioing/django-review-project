# Generated by Django 5.1.3 on 2025-01-06 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_votes_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='rating',
            field=models.FloatField(blank=True, null=True, verbose_name='Средний рейтинг заведения'),
        ),
    ]
