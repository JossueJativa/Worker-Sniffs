# Generated by Django 5.0.3 on 2024-03-14 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_alter_client_is_accepted_by_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='callcenter',
            name='token_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='manger',
            name='token_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='tecnic',
            name='token_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
