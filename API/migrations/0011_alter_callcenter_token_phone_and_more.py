# Generated by Django 5.0.3 on 2024-03-14 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0010_alter_tecnic_token_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callcenter',
            name='token_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='manger',
            name='token_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]