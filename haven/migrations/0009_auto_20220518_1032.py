# Generated by Django 3.2.10 on 2022-05-18 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('haven', '0008_alter_githubrepo_whale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='githubrepo',
            name='backend',
        ),
        migrations.AddField(
            model_name='githubrepo',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
