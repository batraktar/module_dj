# Generated by Django 4.2.1 on 2023-05-24 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='prodquan',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
    ]
