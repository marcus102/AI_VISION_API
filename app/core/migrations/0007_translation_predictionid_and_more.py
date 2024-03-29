# Generated by Django 4.0.10 on 2023-12-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_user_status_user_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='predictionId',
            field=models.CharField(default='None', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='predictions',
            name='user_experience',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='translation',
            name='chosen_language',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='translation',
            name='original_language',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='translation',
            name='text_id',
            field=models.CharField(default='None', max_length=1000, unique=True),
        ),
    ]
