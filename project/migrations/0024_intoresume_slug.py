# Generated by Django 3.0.2 on 2020-02-09 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_auto_20200129_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='intoresume',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]