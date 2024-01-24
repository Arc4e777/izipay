# Generated by Django 5.0.1 on 2024-01-23 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchants', '0002_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceAPIKey',
            fields=[
                ('id', models.CharField(editable=False, max_length=150, primary_key=True, serialize=False, unique=True)),
                ('prefix', models.CharField(editable=False, max_length=8, unique=True)),
                ('hashed_key', models.CharField(editable=False, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('name', models.CharField(default=None, help_text='A free-form name for the API key. Need not be unique. 50 characters max.', max_length=50)),
                ('revoked', models.BooleanField(blank=True, default=False, help_text='If the API key is revoked, clients cannot use it anymore. (This cannot be undone.)')),
                ('expiry_date', models.DateTimeField(blank=True, help_text='Once API key expires, clients cannot use it anymore.', null=True, verbose_name='Expires')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_keys', to='merchants.service', verbose_name='Service')),
            ],
            options={
                'verbose_name': 'Service API key',
                'verbose_name_plural': 'Service API keys',
            },
        ),
    ]
