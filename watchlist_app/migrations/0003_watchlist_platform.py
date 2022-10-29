# Generated by Django 3.2 on 2022-05-21 01:18

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0002_auto_20220520_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='platform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.fields.CharField, related_name='watchlist', to='watchlist_app.streamplatform'),
            preserve_default=False,
        ),
    ]