# Generated by Django 3.2.19 on 2023-08-29 09:58

from django.db import migrations, models
import django.db.models.deletion
import haven.storage
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('haven', '0003_deployment_original_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manifest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=400)),
                ('identifier', models.CharField(max_length=4000)),
                ('scopes', models.JSONField(default=list)),
                ('requirements', models.JSONField(default=list)),
                ('logo', models.ImageField(blank=True, max_length=1000, null=True, storage=haven.storage.PrivateMediaStorage(), upload_to='')),
                ('original_logo', models.CharField(blank=True, help_text='The original logo url', max_length=1000, null=True)),
                ('entrypoint', models.CharField(default='app', max_length=4000)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='deployment',
            name='unique_deployment for version',
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='command',
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='entrypoint',
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='identifier',
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='image',
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='original_logo',
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='requirements',
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='scopes',
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='version',
        ),
        migrations.AddField(
            model_name='deployment',
            name='build_id',
            field=models.CharField(default=uuid.uuid4, max_length=400),
        ),
        migrations.AddField(
            model_name='deployment',
            name='builder',
            field=models.CharField(default='arkitekt.builders.port', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deployment',
            name='definitions',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='deployment',
            name='deployment_id',
            field=models.CharField(default=uuid.uuid4, max_length=400),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='deployed_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddConstraint(
            model_name='manifest',
            constraint=models.UniqueConstraint(fields=('identifier', 'version'), name='unique_manifest for version'),
        ),
        migrations.AddField(
            model_name='deployment',
            name='manifest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deployments', to='haven.manifest'),
        ),
    ]
