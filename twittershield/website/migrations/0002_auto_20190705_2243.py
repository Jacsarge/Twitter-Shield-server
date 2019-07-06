# Generated by Django 2.2.3 on 2019-07-05 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteraccount',
            name='flirtation_score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='twitteraccount',
            name='identity_attack_score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='twitteraccount',
            name='insult_score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='twitteraccount',
            name='profanity_score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='twitteraccount',
            name='sexually_explicit_score',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='twitteraccount',
            name='stored_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='twitteraccount',
            name='threat_score',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='twitteraccount',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tweet_time', models.DateTimeField(null=True)),
                ('cleaned_text', models.TextField()),
                ('original_text', models.TextField()),
                ('toxicity_score', models.FloatField(null=True)),
                ('identity_attack_score', models.FloatField(null=True)),
                ('insult_score', models.FloatField(null=True)),
                ('profanity_score', models.FloatField(null=True)),
                ('threat_score', models.FloatField(null=True)),
                ('sexually_explicit_score', models.FloatField(null=True)),
                ('flirtation_score', models.FloatField(null=True)),
                ('twitter_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.TwitterAccount')),
            ],
        ),
    ]