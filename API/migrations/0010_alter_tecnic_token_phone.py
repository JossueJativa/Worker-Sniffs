# Generated by Django 5.0.3 on 2024-03-14 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0009_callcenter_token_phone_manger_token_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tecnic',
            name='token_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]