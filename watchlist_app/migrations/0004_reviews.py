# Generated by Django 3.2 on 2022-05-21 17:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0003_watchlist_platform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('description', models.CharField(max_length=20, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='watchlist_app.watchlist')),
            ],
        ),
    ]
