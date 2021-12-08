# Generated by Django 3.2.9 on 2021-11-17 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Whale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.CharField(help_text='The corresponding Template on the Arkitekt Instance', max_length=1000, unique=True)),
                ('namespace', models.CharField(help_text='Corresponds to docker hub user', max_length=100)),
                ('repo', models.CharField(help_text='Corresponds to docker repo name', max_length=100)),
                ('tag', models.CharField(help_text='Corresponds to docker hub user', max_length=100)),
                ('env', models.JSONField(help_text='Environment parameters for the Port', null=True)),
            ],
        ),
    ]
