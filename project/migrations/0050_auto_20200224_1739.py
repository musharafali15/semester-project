# Generated by Django 3.0.3 on 2020-02-24 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0049_intoresume_d_resume_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intoresume',
            old_name='d_resume_fname',
            new_name='d_resume_email',
        ),
    ]