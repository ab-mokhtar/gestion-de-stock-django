# Generated by Django 4.2.7 on 2023-12-03 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distinations',
            name='societe',
            field=models.CharField(blank=True, default='0', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='Society',
            field=models.CharField(blank=True, default='0', max_length=50, null=True),
        ),
    ]
