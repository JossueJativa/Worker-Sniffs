# Generated by Django 5.0 on 2024-02-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_client_options_to_give_instalation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='status_instalation',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
