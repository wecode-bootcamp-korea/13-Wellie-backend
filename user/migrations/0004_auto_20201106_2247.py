# Generated by Django 3.1.2 on 2020-11-06 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20201106_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonecheck',
            name='check_id',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='phonecheck',
            name='check_number',
            field=models.CharField(max_length=20),
        ),
    ]
