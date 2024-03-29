# Generated by Django 5.0 on 2024-02-02 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_alter_tecnic_certificates_alter_tecnic_clients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tecnic',
            name='certificates',
            field=models.ManyToManyField(blank=True, to='API.certificate'),
        ),
        migrations.AlterField(
            model_name='tecnic',
            name='clients',
            field=models.ManyToManyField(blank=True, to='API.client'),
        ),
        migrations.AlterField(
            model_name='tecnic',
            name='comments',
            field=models.ManyToManyField(blank=True, to='API.comments'),
        ),
        migrations.AlterField(
            model_name='tecnic',
            name='stars',
            field=models.ManyToManyField(blank=True, to='API.stars'),
        ),
    ]
