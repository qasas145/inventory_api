# Generated by Django 4.0.6 on 2022-08-25 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_control', '0002_alter_inventorygroup_belongs_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]