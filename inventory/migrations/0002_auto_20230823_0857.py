# Generated by Django 3.2.5 on 2023-08-23 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='component',
            old_name='person_who_checkedout',
            new_name='person_who_checked_out',
        ),
        migrations.AlterField(
            model_name='component',
            name='upc',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
