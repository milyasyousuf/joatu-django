# Generated by Django 2.0.3 on 2018-03-26 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0002_auto_20180325_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand_hub',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='demand_hub',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]