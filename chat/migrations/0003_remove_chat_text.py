# Generated by Django 4.2.1 on 2023-05-17 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='text',
        ),
    ]
