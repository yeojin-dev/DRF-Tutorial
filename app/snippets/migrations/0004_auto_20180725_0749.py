# Generated by Django 2.0.7 on 2018-07-25 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_auto_20180725_0457'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='snippet',
            options={'ordering': ('-created',)},
        ),
    ]
