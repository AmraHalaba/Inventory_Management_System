# Generated by Django 3.2.15 on 2022-08-28 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front_web', '0005_auto_20220828_1901'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PricingPlanProperties',
            new_name='PricingPlanProperty',
        ),
        migrations.AlterModelOptions(
            name='pricingplanproperty',
            options={'verbose_name': 'pricingplanproperty', 'verbose_name_plural': 'pricingplanproperties'},
        ),
    ]
