# Generated by Django 3.2.16 on 2023-01-25 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haven', '0002_whale_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='reposcan',
            name='runtime',
            field=models.CharField(default='standard', max_length=400),
        ),
    ]