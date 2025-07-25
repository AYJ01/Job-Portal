# Generated by Django 4.2.2 on 2023-07-06 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_job_portal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job_portal',
            old_name='duration',
            new_name='ex_level',
        ),
        migrations.RenameField(
            model_name='job_portal',
            old_name='requirements',
            new_name='job_type',
        ),
        migrations.RemoveField(
            model_name='job_portal',
            name='loginid',
        ),
        migrations.AddField(
            model_name='job_portal',
            name='location',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='job_portal',
            name='qualification',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='job_portal',
            name='salary',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
