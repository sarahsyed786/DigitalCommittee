# Generated by Django 5.0 on 2023-12-25 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fair_collection', '0005_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fair_collection.userprofile')),
            ],
        ),
    ]
