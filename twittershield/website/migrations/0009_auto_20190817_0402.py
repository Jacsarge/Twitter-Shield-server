# Generated by Django 2.2.3 on 2019-08-17 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20190817_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='cleaned_text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='original_text',
            field=models.TextField(),
        ),
    ]
