# Generated by Django 2.2.3 on 2019-08-12 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20190809_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='misinfo_urls',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
