# Generated by Django 5.0.2 on 2024-06-06 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempotp',
            name='mobile_no',
        ),
    ]
