# Generated by Django 3.2.17 on 2023-02-28 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_profile_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='overtime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
