# Generated by Django 5.1.5 on 2025-01-20 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_adminprofile_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminprofile',
            old_name='last_name',
            new_name='lastName',
        ),
        migrations.RemoveField(
            model_name='adminprofile',
            name='contact_number',
        ),
        migrations.RemoveField(
            model_name='professorprofile',
            name='contact_number',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='contact_number',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='email_optional',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='password',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='student_id',
        ),
        migrations.AddField(
            model_name='professorprofile',
            name='lastName',
            field=models.CharField(default='UnKnown', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='lastName',
            field=models.CharField(default='UnKnown', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='username',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='adminprofile',
            name='username',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]