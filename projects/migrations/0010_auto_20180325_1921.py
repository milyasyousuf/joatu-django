# Generated by Django 2.0.3 on 2018-03-25 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20180325_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_hub',
            name='hub',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hubs.Hub'),
        ),
    ]