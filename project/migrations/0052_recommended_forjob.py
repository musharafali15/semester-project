# Generated by Django 3.0.3 on 2020-02-27 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0051_auto_20200226_0438'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommended',
            name='forjob',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]